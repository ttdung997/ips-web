import sys
import json

from win32.src.integrity.integrity_func import *

def ussage():
    print("")
    print("-i [path] [type]: insert check object to db")
    print("-d [path] [type]: insert check object from db")
    print("\t type: 0-file, 1-folder, 2-registry")
    return 1

def removeFromDb():
    return removeDb()

def main():
    create_integrity_db()
    argv = sys.argv
    if len(argv) != 4:
        if len(argv) == 3:
            if argv[1] == '-x':
                res = add_sys_check_from_xml(argv[2])
                checkList = get_check_list()
                print(json.dumps({'result': res == 0, 'check_list': checkList}))
                return 0

            if argv[1] == '-m':
                res, msg = do_hash_file(argv[2])
                if res == 0:
                    print(json.dumps({'result': True, 'hash_str': msg}))
                else:
                    print(json.dumps({'result': False, 'error_msg': msg}))
                return 0

            if argv[1] == '-a':
                res= getAlertListFromId(argv[2])
                print(json.dumps({'alert_list': res}))
                return 0


        elif len(argv) == 2:
            if(argv[1] == '-l'):
                print(json.dumps({'check_list':get_list_sys_check()}))
                return 0
            elif argv[1]  == '-a':
                print(json.dumps({'alert_list':get_list_alert()}))
                return 0
            elif argv[1] == '-e':
                print(json.dumps({'last_alert_id':getLastAlertId()}))
                return 0
            elif argv[1]  == '-h':
                print(json.dumps({'hash_file_list':get_list_hash_file()}))
                return 0
            elif argv[1]  == '-g':
                print(json.dumps({'hash_register_list':get_list_hash_registry()}))
                return 0
        return ussage()

    if argv[1] == '-i':
        res = add_check_object_to_db(argv[2], argv[3])
        checkList = get_check_list()
        print(json.dumps({'result': res == 0, 'check_list': checkList}))
        return 0
    elif argv[1] == '-r':
        res = remove_check_object_from_db(argv[2], argv[3])
        checkList = get_check_list()
        print(json.dumps({'result': res == 0, 'check_list': checkList}))
        return 0

    elif argv[1] == '-s':
        res, msg = scan(argv[2], argv[3])
        # alertList = get_alert_list()
        succ = res == 0
        if res != 0:
            print(json.dumps({'result': succ, 'error_msg': msg}))
        else:
            print(json.dumps({'result': succ, 'message': msg}))
        return 0
   
if __name__ == '__main__':
    # removeDb()
    # print(get_list_sys_check())
    main()
    # resetDb()
    # checkList = get_check_list()
    # print({'result': res == 0, 'check_list': checkList})

