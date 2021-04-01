#
# Define messages and constants used in cryptography module.
#
# Define return error code
ERROR_CODE = -1
SUCCESS_CODE = 0
SKIP_CODE = 1
FILE_NOT_FOUND = -2
PASSWORD_INCORRECT_CODE = -3


ERROR_CREATE_DB = -4
ERROR_INSERT_RECORD = -5
ERROR_DELETE_RECORD = -6
ERROR_UPDATE_RECORD = -7

# Define size data_block encrypt/decrypt
DATA_BLOCK_SIZE = 32768

# Define message for check integrity system
ERROR_CREATE_DB_MSG = "There was an error creating the database."
SUCCESS_CREATE_DB_MSG = "Create success database: "
ADD_FILE_MSG = "The new file add to folder."
CHANGE_FILE_MSG = "File is changed."
DEL_FILE_MSG = "File is deleted."
NOT_CHANGE_FILE_MSG = "FIle not changed."

ERROR_HASH_FILE_MSG = "Error in generate hash string for file."
ERROR_QUERY_DB = "Da co loi khi ket noi CSDL"

FILE_TYPE = 0
DIR_TYPE = 1
REGISTRY_TYPE = 2

IGNORE_OBJECT = 1

# VALUE_CHANGE = 'Registry value change.'
# VALUE_ADD = 'Registry value add.'
# VALUE_DEL = 'Registry value deleted.'
# KEY_ADD = 'Registry key add.'
# KEY_DEL = 'Registry key deleted.'

TAG_FILE_CHECK = 'file_check'
TAG_FOLDER_CHECK = 'folder_check'
# TAG_REGISTRY_CHECK = 'windows_registry'
