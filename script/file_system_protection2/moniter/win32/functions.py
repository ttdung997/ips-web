from datetime import datetime
import glob
import os
from win32.database import *
TYPE_FOLDER = 1
TYPE_FILE = 0

FILE_CREATE_MSG = "File created."
FILE_MODIFY_MSG = "File changed."
FILE_ACCESS_MSG = "File access."
FILE_DEL_MSG = "File deleted."
FOLDER_DEL_MSG = "Folder deleted."
def getReadableTime(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def getCurrentTime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getListFileInFolder(folderPath):
    ret = []
    for parent_dir, list_dir, list_file in os.walk(folderPath):
        for file in list_file:
            ret.append(os.path.join(parent_dir, file))
    return ret

def getTimeInfo(filePath):
    if not os.path.isfile(filePath):
        return None
    try:
        a_time = getReadableTime(os.path.getatime(filePath))
        c_time = getReadableTime(os.path.getctime(filePath))
        m_time = getReadableTime(os.path.getmtime(filePath))
        return (c_time, m_time, a_time)
    except:
        return None

def updateListFile(listFile, listfileDb, status):
    updateList = []
    insertList = []
    delList = []
    alertList = []
    currTime = getCurrentTime()
    for path in listFile:
        infoFile = listFile[path] #(c_time, m_time, a_time)
        if path not in listfileDb:
            #Insert
            insertList.append((None, path) + infoFile)
            if(status != 0):
                #Insert alert
                alertList.append((None, infoFile[0], FILE_CREATE_MSG, path))
                if infoFile[1] != infoFile[0]:
                    alertList.append((None, infoFile[1], FILE_MODIFY_MSG, path))
                if infoFile[2] != infoFile[1]:
                    alertList.append((None, infoFile[2], FILE_ACCESS_MSG, path))
            
        else:
            #Check
            infoDb = listfileDb[path]
            id = infoDb[0]
            infoDb = infoDb[1:]
           
            if infoDb != infoFile:
                if(infoDb[0]!= infoFile[0]):
                    #File remove and create new
                    alertList.append((None, infoFile[0], FILE_DEL_MSG, path))
                    alertList.append((None, infoFile[0], FILE_CREATE_MSG, path))
                else:
                    if infoFile[1] != infoDb[1]:
                        #Modify
                        alertList.append((None, infoFile[1], FILE_MODIFY_MSG, path))
                    elif infoFile[2] != infoDb[2]:
                        #Access
                        alertList.append((None, infoFile[2], FILE_ACCESS_MSG, path))
                updateList.append(infoFile + (id,))
            del listfileDb[path]
            #update
    for delFile in listfileDb:
        alertList.append((None, currTime, FILE_DEL_MSG, delFile))
        delList.append((listfileDb[delFile][0], ))

    reta = insert_many_moniter_alert(alertList)
    
    retd = delete_many_moniter_file(delList)

    retu = update_many_moniter_file(updateList)
   
    reti = insert_many_moniter_file(insertList)
    #update to db
    return {'total_file_scan': len(listFile),
            'insert_sts': reti == SUCCESS_CODE,
            'insert': len(insertList),
            'update_sts': retu == SUCCESS_CODE,
            'update': len(updateList),
            'delete_sts': retd == SUCCESS_CODE,
            'delete': len(delList)
            }




#returm dic as {file_path = (c_time, m_time, a_time)}
def getDicFileInfo(listFilePath):
    ret = {}
    for filePath in listFilePath:
        timeInfo = getTimeInfo(filePath)
        if timeInfo is None:
            continue
        ret[filePath] = timeInfo
    return ret

#from (id, path, c_time, m_time, a_time) to {path, (id, c_time, m_time, a_time)}
def fromListToDic(listInfo): 
    ret = {}
    for inf in listInfo:
        ret[inf[1]] = (inf[0],) + inf[2:]
    return ret    

def getFolderInfo(folderPath):
    listFile = getListFileInFolder(folderPath)
    return getDicFileInfo(listFile)

def doScanFile(filePath):
    moniterObj = get_moniter_object(filePath, TYPE_FILE)
    if moniterObj is None:
        return ERROR_CODE, 'File is not in moniter list.'
    status = moniterObj[-1]

    fileInfoDb = get_moniter_file(filePath)

    fileTimeInfo = getTimeInfo(filePath)
    if fileTimeInfo is None:
        return ERROR_CODE, 'Can not read file property.'
    if fileInfoDb is None:
        #New in db
        ret = insert_moniter_file(filePath, fileTimeInfo[0], fileTimeInfo[1], fileTimeInfo[2])
        if status == 0:
            update_first_add_sts(moniterObj[0])
        else:
            insert_moniter_alert(fileTimeInfo[0], FILE_CREATE_MSG, filePath)
            if(fileTimeInfo[1]!= fileTimeInfo[0]):
                insert_moniter_alert(fileTimeInfo[1], FILE_MODIFY_MSG, filePath)
            if(fileTimeInfo[1]!= fileTimeInfo[2]):
                insert_moniter_alert(fileTimeInfo[2], FILE_ACCESS_MSG, filePath)
    else:
        idFile = fileInfoDb[0]
        fileInfoDb = fileInfoDb[2:]
        #check update

        if fileTimeInfo != fileInfoDb:
            update_moniter_file(idFile, fileTimeInfo[0], fileTimeInfo[1], fileTimeInfo[2])
            if fileTimeInfo[0]!= fileInfoDb[0]:
                #file deleted and create new
                insert_moniter_alert(fileTimeInfo[0], FILE_DEL_MSG, filePath)
                insert_moniter_alert(fileTimeInfo[0], FILE_CREATE_MSG, filePath)
            if fileTimeInfo[1]!= fileTimeInfo[0]:
                insert_moniter_alert(fileTimeInfo[1], FILE_MODIFY_MSG, filePath)
            if fileInfoDb[2]!= fileInfoDb[1]:
                insert_moniter_alert(fileTimeInfo[2], FILE_ACCESS_MSG, filePath)
    return SUCCESS_CODE, "Scan file success."
    # updateScanFile(filePath, fileTimeInfo)

def doScanFolder(folderPath):
    moniter_obj = get_moniter_object(folderPath, TYPE_FOLDER)
    if moniter_obj is None:
        return ERROR_CODE, 'Folder is not in moniter list'
    if not os.path.isdir(folderPath):
        remove_moniter_obj(folderPath, TYPE_FOLDER)
        return ERROR_CODE, 'Object is not folder'
    status = moniter_obj[-1]
    listFilePath = getListFileInFolder(folderPath)
    dicInfo = getDicFileInfo(listFilePath)
   
    listInfoDb = get_list_file_from_dir_path_and_child(folderPath)
    dicInfoDb = fromListToDic(listInfoDb)
    del(listInfoDb)
    #Update chang to db
    ret = updateListFile(dicInfo, dicInfoDb, status)
    if(status == 0):
        update_first_add_sts(moniter_obj[0])
    return SUCCESS_CODE, ret
  
def scan(path, t):
    if t == TYPE_FOLDER or str(t) == str(TYPE_FOLDER):
        ret, data = doScanFolder(path)
        return ret, data
    elif t == TYPE_FILE or str(t) == str(TYPE_FILE):
        ret, msg = doScanFile(path)
        return ret, msg
    else:
        return ERROR_CODE, 'Type not found.'

def insert_moniter_obj(path, t):
    if str(t) != str(TYPE_FILE) and str(t) != str(TYPE_FOLDER):
        return 'Type not found.'
    if not os.path.isfile(path) and not os.path.isdir(path):
        return 'Object is not file or folder.'
    
    ret = get_moniter_object(path, t)
    
    if ret is None:
        return insert_moniter_object(t, path)
    else:
        return 'Object already in moniter list.'

def remove_moniter_obj(path, t):

    record = get_moniter_object(path, t)
    if record is None:
        return 'Objec is not in moniter list.'
    ret = remove_moniter_object(path, t)
    if ret == ERROR_CODE:
        return 'Can not remove moniter object.'

    #Clean data in moniter_file table
    if str(t) == str(TYPE_FILE):
        rec = get_moniter_file(path)
        if rec is not None:
            del_moniter_file_by_id(rec[0])
    elif str(t) == TYPE_FOLDER:
        listFile = get_list_file_from_dir_path_and_child(path)
        listId = []
        for file in listFile:
            listId.append(file[0])
        
        delete_many_moniter_file(listId)

    return SUCCESS_CODE


def getLastAlertId():
    ret = db_get_last_alert_id()
    if ret == ERROR_CODE:
        ret = 0
    else:
        ret = ret[0]
    return ret

def getAlertListFromId(id):
    ret = get_list_alert_from_id(id)
    if ret == ERROR_CODE:
        ret =[]
    else:
        return ret




# def test():
    # print(getListFileInFolder(r'F:\BKCS\z_More\File-Audit-Script-1.25\python'))
    # print(getFolderInfo(r'F:\BKCS\z_More\File-Audit-Script-1.25\python'))

    # doScanFile(r"F:\BKCS\z_More\File-Audit-Script-1.25\python\admin.py")
    # insert_moniter_obj(r'F:\BKCS\z_More\File-Audit-Script-1.25\python', 1)
    # scan(r'F:\BKCS\z_More\File-Audit-Script-1.25\python', 1)
    # print(getListFileInFolder(r'F:\BKCS\z_More\File-Audit-Script-1.25\python'))
    # pass

if __name__ == "__main__":
    pass
    # test()
