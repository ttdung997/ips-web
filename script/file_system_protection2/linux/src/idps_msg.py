#
# Define messages and constants used in file system protection module.
#
#
# Define operating system platform
UNKNOWN_PLATFORM = -1
WINDOWS_PLATFORM = 0
LINUX_PLATFORM = 1
#
# Define size data_block encrypt/decrypt
DATA_BLOCK_SIZE = 32768
#
# Define return error code
DIR_NOT_FOUND = -3
FILE_NOT_FOUND = -2
ERROR_CODE = -1
SUCCESS_CODE = 0
SKIP_CODE = 1
CONFIRM_DEL = 2
OVERRIDE_CODE = 3


FILE_EXIST = 2
DIR_EXIST = 3

PASSWORD_INCORRECT_CODE = -3

ERROR_CREATE_DB = -4
ERROR_INSERT_RECORD = -5
ERROR_DELETE_RECORD = -6
ERROR_UPDATE_RECORD = -7

FILE_TYPE = 0
DIR_TYPE = 1
REGISTRY_TYPE = 2

IGNORE_OBJECT = 1

FILE_NOT_FOUND_MSG = "File not exist."
DIR_NOT_FOUND_MSG = "Directory not exist."

FILE_EXIST_MSG = "File exist."

# Define message for check integrity system
ERROR_CREATE_DB_MSG = "There was an error creating the database."
SUCCESS_CREATE_DB_MSG = "Create success database: "
ADD_FILE_MSG = "The new file add to folder."
CHANGE_FILE_MSG = "File is changed."
DEL_FILE_MSG = "File is deleted."
NOT_CHANGE_FILE_MSG = "FIle not changed."

ERROR_HASH_FILE_MSG = "Error in generate hash string for file."
ERROR_QUERY_DB = "Da co loi khi ket noi CSDL"

# Define format encrypt file
TYPE_ENCRYPT_FILE = ".enc"

# Define message encrypt/decrypt file, directory
SUCCESS_ENCRYPT_FILE = "Done encrypt file."
ERROR_ENCRYPT_FILE = "#Error in process encrypt file!"
SUCCESS_DECRYPT_FILE = "Done decrypt file."
ERROR_DECRYPT_FILE = "#Error in process decrypt file!"
PASSWORD_INCORRECT_MSG = "Error. Password incorrect"
SUCCESS_ENCRYPT_DIR = "Done encrypt directory."
SUCCESS_DECRYPT_DIR = "Done decrypt directory."

CONFIRM_DEL_MSG = "Confirm override file."
SKIP_CONRIFM_DEL_MSG = "Skip override file."
