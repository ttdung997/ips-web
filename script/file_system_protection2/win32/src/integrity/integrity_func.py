import hashlib
from win32.src.system.file_func import *
from win32.src.database.sqlite3_func import *
from win32.src.integrity.integrity_msg import *
from win32.src.integrity.regcontroller import *
import xml.etree.ElementTree as ET
from datetime import datetime

def hash_file(result, path_file):
    try:
        with open(path_file, 'rb') as f_in:
            while True:
                data_block = f_in.read(DATA_BLOCK_SIZE)
                if not data_block:
                    break
                result.update(data_block)
        return result.hexdigest()
    except (ValueError, Exception):
        db_print(ERROR_HASH_FILE_MSG)
        return ERROR_CODE


# Generate hash string (SHA1) for file
# return hash value (string) or ERROR_CODE
def hash_sha1(path_file):
    result_sha1 = hashlib.sha1()
    return hash_file(result_sha1, path_file)


# Generate hash string (SHA-256) for file
# return hash value (string) or ERROR_CODE
def hash_sha256(path_file):
    result_sha256 = hashlib.sha256()
    return hash_file(result_sha256, path_file)


def add_check_object_to_db(filePath, type):
    return insert_or_update_sys_check(filePath, type)

def remove_check_object_from_db(filePath, type):
    return remove_sys_check(filePath, type)

def get_check_list():
    return get_list_sys_check()

def get_alert_list():
    return get_list_alert()

def get_hash_file_lis():
    return get_list_hash_file()

def add_sys_check_from_xml(path):
    db_print(path)
    ret = ERROR_CODE
    try:
        cList = []
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            if child.tag == TAG_FILE_CHECK:
                cList.append((child.text, FILE_TYPE))
            elif child.tag == TAG_FOLDER_CHECK:
                cList.append((child.text, DIR_TYPE))
            elif child.tag == TAG_REGISTRY_CHECK:
                cList.append((child.text, REGISTRY_TYPE))
        print(list)
        for c in cList:
            add_check_object_to_db(c[0], c[1])
        ret = SUCCESS_CODE
    except Exception as e:
        db_print(e)
    return ret


def check_integrity_file(current_time, path_file):
    db_print('### \nStarting check integrity for file ...')

    check_obj = get_sys_check_object(path_file, FILE_TYPE)
    if check_obj is None:
        db_print("File is not in check list")
        return ERROR_CODE
    isFile = os.path.isfile(path_file)
    if isFile == False:
        # file was remove
        #get hash_record in hash file
        hash_rec = get_hash_record_db(FILE_TYPE, path_file)
        if hash_rec != ERROR_CODE:
            if hash_rec is not None:
                ret = del_hash_by_id(FILE_TYPE, path_file)
                if ret == ERROR_CODE:
                    return ERROR_CODE
            ret = remove_check_object_from_db(path_file, FILE_TYPE)
            if ret == ERROR_CODE:
                return ERROR_CODE
            ret = insert_integrity_alert(current_time, DEL_FILE_MSG, path_file)
            if ret == ERROR_CODE:
                return ERROR_CODE
        return SUCCESS_CODE

    #Case file exist
    
    alert = check_obj[3] != 0

    hash_record = get_hash_record_db(FILE_TYPE, path_file)  # type <hash_record> = list
    # Cannot connect to database
    if hash_record == ERROR_CODE:
        return ERROR_CODE
    hash_str = hash_sha256(path_file)

    if hash_record:
        if hash_record[2] != hash_str:
            result = update_hash_by_id(FILE_TYPE, hash_record[0], hash_str)
            if result == ERROR_CODE:
                return ERROR_CODE

            result = insert_integrity_alert(current_time, CHANGE_FILE_MSG, path_file)
            if result == ERROR_CODE:
                return ERROR_CODE

            print(CHANGE_FILE_MSG)
        else:
            print(NOT_CHANGE_FILE_MSG)
    else:  # Cannot find data of file in database
        db_print("Insert hash file")
        result = insert_hash_to_db(FILE_TYPE, path_file, hash_str)
        if result == ERROR_CODE:
            return ERROR_CODE
        if alert == True:
            result = insert_integrity_alert(current_time, ADD_FILE_MSG, path_file)
            if result == ERROR_CODE:
                return ERROR_CODE
        if alert == False:
            update_first_add_sts(check_obj[0])
        db_print(ADD_FILE_MSG)
        return SUCCESS_CODE


def compare_state(allFile, parent_dir, list_file, current_time, insert_alert = True):
    # db_print("Record: {}".format(old_hash))
    # db_print("List file: {}".format(list_file))
    # for record in old_hash:
    #     #check fie exits
    #     if os.path.isfile(record[1]) is False:
    #         result = insert_integrity_alert(current_time, DEL_FILE_MSG, record[2])
    #         if result == ERROR_CODE:
    #             return ERROR_CODE

    #         result = del_hash_by_id(FILE_TYPE, record[0])
    #         if result == ERROR_CODE:
    #             return ERROR_CODE
    #         db_print(record[1])
    #         db_print(DEL_FILE_MSG)
    addU = 0
    addI = 0
    addS = 0
    for file in list_file:
        addS = addS + 1
        path_file = os.path.join(parent_dir, file)
        record = get_hash_record_db(FILE_TYPE, path_file)
        # Cannot connect to database
        if record == ERROR_CODE:
            continue

        hash_str = hash_sha256(path_file)
        if record is not None:
            if record[2] != hash_str:
                addU = addU + 1
                result = update_hash_by_id(FILE_TYPE, record[0], hash_str)
                if result == SUCCESS_CODE:
                    result = insert_integrity_alert(current_time, CHANGE_FILE_MSG, path_file)
                db_print(record[1])
                db_print(CHANGE_FILE_MSG)
            if path_file in allFile:
                del allFile[path_file]
                
        else:  # Cannot find data of file in database
            addI = addI + 1
            result = insert_hash_to_db(FILE_TYPE, path_file, hash_str)
           
            if insert_alert and result == SUCCESS_CODE:
                result = insert_integrity_alert(current_time, ADD_FILE_MSG, path_file)
               
            if path_file in allFile: #return false
                del allFile[path_file]
            db_print(path_file)
            db_print(ADD_FILE_MSG)
    return allFile, addS, addI, addU
    
#(id, path, hash_str) -> {path: (id, hash_str)}
def convertToDic(dList):
    res = {}
    for i in dList:
        res[i[1]] = (i[0], i[2])
    return res


def check_integrity_dir(path_dir, current_time):
    db_print('### \nStarting check integrity for directory ...')
    objectRec = get_sys_check_object(path_dir, DIR_TYPE)
    if objectRec is None:
        return ERROR_CODE #in not in check list

    all_hash_record = get_list_file_from_curr_dir_db_and_child(path_dir)
    all_hash_dic = convertToDic(all_hash_record)

    insert_alert = True
    insert_alert = objectRec[3] != 0
    fileScan =0
    fileUpdate = 0
    fileDel = 0
    fileAdd = 0
    if os.path.isdir(path_dir):
        
        for parent_dir, list_dir, list_file in os.walk(path_dir):
            # Cannot connect to database
            # old_hash_record = get_list_file_from_curr_dir_db(parent_dir + "\\%")
            all_hash_dic, addS, addI, addU = compare_state(all_hash_dic, parent_dir, list_file, current_time, insert_alert)
            
            fileScan = fileScan + addS
            fileAdd = fileAdd + addI
            fileUpdate = fileUpdate + addU
        
        for path in all_hash_dic:
            fileDel = fileDel + 1
            insert_integrity_alert(current_time, DEL_FILE_MSG, path)
            del_hash_by_id(FILE_TYPE, all_hash_dic[path][0])

        if insert_alert == False:
            update_first_add_sts(objectRec[0])
    else:
        #dir deleted
        for oh in all_hash_record:
            fileDel = fileDel +1
            insert_integrity_alert(current_time, DEL_FILE_MSG, oh[1])
            del_hash_by_id(FILE_TYPE, oh[0])
            #remove in check list
        remove_check_object_from_db(path_dir, DIR_TYPE)
    db_print("Done check dir: {}".format(path_dir))
    return {'scan_file': fileScan, 'add_file': fileAdd, 'change_file': fileUpdate, 'del_file':fileDel}
   

def scanFile(path):
    current_time =  datetime.now()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return check_integrity_file(current_time, path)


def scanFolder(path):
    current_time =  datetime.now()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return check_integrity_dir(path, current_time)


def scanRegistry(path):
    current_time =  datetime.now()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return scanRegistryKey(path, current_time)

def do_hash_file(path):
    ret = hash_sha256(path)
    if ret == ERROR_CODE:
        return ret, 'Can not hash file'
    return SUCCESS_CODE, ret

def scan(path, t):

    if t == FILE_TYPE or str(t) == str(FILE_TYPE):
        ret = scanFile(path)
        err_msg = ''
        if ret == ERROR_CODE:
            err_msg = "File was not in check list."
        return ret, err_msg

    elif t == DIR_TYPE or str(t) == str(DIR_TYPE):
        ret = scanFolder(path)
        if ret == ERROR_CODE:
            err_msg = "Folder was not in check list."
        else:
            err_msg = ret
            ret = SUCCESS_CODE
        return ret, err_msg
    
    elif t == REGISTRY_TYPE or str(t) == str(REGISTRY_TYPE):
        ret = scanRegistry(path)
    err_msg = 'Registry key was not in check list.'
    if ret != ERROR_CODE:
        err_msg = ret
        ret = SUCCESS_CODE
    return ret, err_msg

# def get_all_alert():
#     print(get_list_alert())

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



# def get_all_sys_check():
#     print(get_list_sys_check())

def removeDb():
    remove_alert_integrity()
    remove_hash_file()
    remove_hash_registry()
    remove_hash_syscheck_object()
