import ctypes.wintypes
from datetime import datetime
from logging import getLogger, INFO, Formatter, StreamHandler, FileHandler
import os
import re
import threading

LOG_DIR = 'log'
LOG_FILE_NAME = LOG_DIR + os.sep + datetime.now().strftime('%F_%H-%M-%S.log')
LOG_FILE_PATH = (os.path.dirname(os.path.abspath(__file__))
                 + os.sep
                 + LOG_FILE_NAME).casefold()

if os.path.exists(LOG_DIR):
    if os.path.isfile(LOG_DIR):
        raise RuntimeError('cannot create directory "log"')
else:
    os.mkdir(LOG_DIR)

logger = getLogger(__name__)
logger.setLevel(INFO)
formatter = Formatter(fmt='[%(asctime)s.%(msecs)03d]%(message)s',
                      datefmt='%Y/%m/%d %X')

stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(INFO)
logger.addHandler(stream_handler)

file_handler = FileHandler(LOG_FILE_NAME)
file_handler.setFormatter(formatter)
file_handler.setLevel(INFO)
logger.addHandler(file_handler)


kernel32 = ctypes.windll.kernel32

FILE_NOTIFY_CHANGE_FILE_NAME = 0x01
FILE_NOTIFY_CHANGE_DIR_NAME = 0x02
FILE_NOTIFY_CHANGE_ATTRIBUTES = 0x04
FILE_NOTIFY_CHANGE_SIZE = 0x08
FILE_NOTIFY_CHANGE_LAST_WRITE = 0x010
FILE_NOTIFY_CHANGE_LAST_ACCESS = 0x020
FILE_NOTIFY_CHANGE_CREATION = 0x040
FILE_NOTIFY_CHANGE_SECURITY = 0x0100

FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OVERLAPPED = 0x40000000
FILE_LIST_DIRECTORY = 1
FILE_SHARE_READ = 0x01
FILE_SHARE_WRITE = 0x02
FILE_SHARE_DELETE = 0x04
OPEN_EXISTING = 3

FILE_ACTION_CREATED = 1
FILE_ACTION_DELETED = 2
FILE_ACTION_MODIFIED = 3
FILE_ACTION_RENAMED_OLD_NAME = 4
FILE_ACTION_RENAMED_NEW_NAME = 5

FILE_NOTIFY_FLAGS = \
  FILE_NOTIFY_CHANGE_FILE_NAME \
  | FILE_NOTIFY_CHANGE_DIR_NAME \
  | FILE_NOTIFY_CHANGE_ATTRIBUTES \
  | FILE_NOTIFY_CHANGE_SIZE \
  | FILE_NOTIFY_CHANGE_LAST_WRITE \
  | FILE_NOTIFY_CHANGE_LAST_ACCESS \
  | FILE_NOTIFY_CHANGE_CREATION \
  | FILE_NOTIFY_CHANGE_SECURITY


class FileNotifyInformation(ctypes.Structure):
    _fields_ = [('NextEntryOffset', ctypes.wintypes.DWORD),
                ('Action', ctypes.wintypes.DWORD),
                ('FileNameLength', ctypes.wintypes.DWORD),
                ('FileName', (ctypes.c_char * 1))]


LPFNI = ctypes.POINTER(FileNotifyInformation)


def get_handle(path_obj):
    handle = kernel32.CreateFileW(
        path_obj,
        FILE_LIST_DIRECTORY,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    return handle


def parse_event_buffer(buffer, nbytes):
    results = []
    while nbytes.value > 0:
        fni = ctypes.cast(buffer, LPFNI)[0]
        ptr = ctypes.addressof(fni) + FileNotifyInformation.FileName.offset
        filename = ctypes.string_at(ptr, fni.FileNameLength)
        results.append((fni.Action, filename.decode('utf-16')))
        offset = fni.NextEntryOffset
        if offset == 0:
            break
        buffer = buffer[offset:]
        nbytes.value -= offset
    return results


def watch_directory(directory_path, recursive=True, dump=True,
                    match=None, exclude=None):
    handle = get_handle(directory_path)
    event_buffer = ctypes.create_string_buffer(2048)
    nbytes = ctypes.wintypes.DWORD()

    while True:
        kernel32.ReadDirectoryChangesW(
            handle,
            ctypes.byref(event_buffer),
            len(event_buffer),
            recursive,
            FILE_NOTIFY_FLAGS,
            ctypes.byref(nbytes),
            None,
            None
        )

        results = parse_event_buffer(event_buffer, nbytes)
        for action, filename in results:
            fullpath = os.path.join(directory_path, filename)
            if fullpath.casefold() == LOG_FILE_PATH:
                continue
            if match is not None and not re.search(match, fullpath):
                continue
            if exclude is not None and re.search(exclude, fullpath):
                continue

            if action == FILE_ACTION_CREATED:
                logger.info('[ + ] %s', fullpath)
            elif action == FILE_ACTION_DELETED:
                logger.info('[ - ] %s', fullpath)
            elif action == FILE_ACTION_MODIFIED:
                if os.path.isdir(fullpath):
                    continue
                log_messages = []
                log_messages.append('[ * ] ' + fullpath)

                if dump:
                    log_messages.append('[vvv] Dumping contents...')
                    try:
                        f = open(fullpath, "rb")
                        contents = f.read()
                        f.close()
                        log_messages.append(contents.decode('sjis'))
                        log_messages.append('[^^^] Dump complete.')
                    except Exception as e:
                        log_messages.append('[!!!] <%s> %s' % (e.__class__.__name__, e))
                        log_messages.append('[!!!] Dump failed.')

                logger.info('\n'.join(log_messages))

            elif action == FILE_ACTION_RENAMED_OLD_NAME:
                logger.info('[ < ] %s', fullpath)
            elif action == FILE_ACTION_RENAMED_NEW_NAME:
                logger.info('[ > ] %s', fullpath)
            else:
                logger.info('[???] %s', fullpath)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*', default=['.'])
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('-d', '--dump', action='store_true')
    parser.add_argument('-m', '--match')
    parser.add_argument('-e', '--exclude')
    args = parser.parse_args()

    for path in args.paths:
        abspath = os.path.abspath(path)
        monitor_thread = threading.Thread(
            target=watch_directory,
            args=(abspath, args.recursive, args.dump, args.match, args.exclude)
        )
        logger.info('Spawning monitoring thread for path: %s', abspath)
        monitor_thread.start()
