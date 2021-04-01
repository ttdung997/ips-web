import argparse
import struct
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from linux.src.system.file_func import *


# Get key from password
# return 32 byte (SHA-256)
def get_key_from_password(password):
    salt = b'bkcs'
    iteration = 4096
    len_key = 32

    # Generate key from password using HMAC-PBKDF2
    key_hex = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iteration, len_key)
    return key_hex


# Handle process encrypt file
# return ERROR_CODE or SUCCESS_CODE
def process_encrypt(path_file, key):
    tmp_path_file, ext_file = os.path.splitext(path_file)
    i = 0

    # a.txt -> a_001.enc
    path_file_enc = tmp_path_file + "_" + '{:03d}'.format(i) + TYPE_ENCRYPT_FILE

    while True:
        if os.path.isfile(path_file_enc):
            i += 1
            path_file_enc = tmp_path_file + "_" + '{:03d}'.format(i) + TYPE_ENCRYPT_FILE
        else:
            break

    file_size = os.path.getsize(path_file)
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    try:
        with open(path_file, 'rb') as f_in:
            with open(path_file_enc, 'wb') as f_out:
                f_out.write(struct.pack('<Q', file_size))
                f_out.write(iv)
                # Pack 16 byte -> encrypt info of old file with AES
                f_out.write(encryptor.encrypt(struct.pack('16s', ext_file.encode('utf-8'))))

                # Encrypt file by data block
                while True:
                    data_block = f_in.read(DATA_BLOCK_SIZE)
                    len_block = len(data_block)
                    if len_block == 0:
                        f_in.close()
                        os.remove(path_file)
                        print(SUCCESS_ENCRYPT_FILE)
                        return SUCCESS_CODE
                    elif len_block % 16 != 0:
                        data_block += b' ' * (16 - len_block % 16)  # padding with spaces
                    f_out.write(encryptor.encrypt(data_block))
    except Exception as e:
        print(e)
        return ERROR_CODE


# Encrypt a single file
# return ERROR_CODE or SUCCESS_CODE
def encrypt_file(path_file, password):
    result = check_file_exist(0, path_file)
    if result == FILE_NOT_FOUND:
        return FILE_NOT_FOUND

    print('### \nStarting encrypt file ...')
    key_enc = get_key_from_password(password)
    return process_encrypt(path_file, key_enc)


# Handle process decrypt file
# return ERROR_CODE or SUCCESS_CODE
def process_decrypt(path_file, key, popup):
    try:
        with open(path_file, 'rb') as f_in:
            file_size = struct.unpack('<Q', f_in.read(struct.calcsize('Q')))[0]
            iv = f_in.read(AES.block_size)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            #  Unpack 16 byte -> Decrypt info of old file with AES
            pack_ext_old_file = decryptor.decrypt(f_in.read(16))
            try:
                ext_old_file = struct.unpack('16s', pack_ext_old_file)[0].decode('utf-8').replace("\x00", "")
            except (ValueError, Exception):
                # print(PASSWORD_INCORRECT_MSG)
                return PASSWORD_INCORRECT_CODE

            # a_001.enc -> a.txt
            # Get path file decryption
            temp_path_file, name_file_dec = os.path.split(path_file)
            if len(name_file_dec) > 8:
                path_file_dec = path_file[:-8] + ext_old_file
            else:   # a.enc -> a.txt
                path_file_dec = os.path.splitext(path_file)[0] + ext_old_file

            if os.path.isfile(path_file_dec):
                print(FILE_EXIST_MSG)
                if popup == CONFIRM_DEL:
                    print(CONFIRM_DEL_MSG)
                    os.remove(path_file_dec)  # Remove file decryption exist
                else:
                    print(SKIP_CONRIFM_DEL_MSG)
                    return SUCCESS_CODE
            # Decrypt file by data block
            with open(path_file_dec, 'wb') as f_out:
                while True:
                    data_block = f_in.read(DATA_BLOCK_SIZE)
                    len_block = len(data_block)
                    if len_block == 0:
                        print(SUCCESS_DECRYPT_FILE)
                        return SUCCESS_CODE

                    decode_data_block = decryptor.decrypt(data_block)
                    n = len(decode_data_block)
                    if file_size > n:
                        f_out.write(decode_data_block)
                    else:
                        f_out.write(decode_data_block[:file_size])  # Remove padding on last block
                    file_size -= n

    except Exception as e:
        print(e)
        return ERROR_CODE


# Decrypt a single file
# return ERROR_CODE, PASSWORD_INCORRECT_CODE or SUCCESS_CODE
def decrypt_file(path_file, password, popup):
    result = check_file_exist(0, path_file)
    if result == FILE_NOT_FOUND:
        return FILE_NOT_FOUND

    print('### \nStarting decrypt file ...')
    key_dec = get_key_from_password(password)
    result = process_decrypt(path_file, key_dec, popup)
    if result == SUCCESS_CODE:
        os.remove(path_file)
    return SUCCESS_CODE

# Encrypt all file in directory and sub-directory
# return ERROR_CODE or SUCCESS_CODE
def encrypt_dir(path_dir, password):
    result = check_file_exist(1, path_dir)
    if result == DIR_NOT_FOUND:
        return ERROR_CODE

    print('### \nStarting encrypt directory ...')
    key_enc = get_key_from_password(password)

    # Scan directory
    # type<list_dir, list_file> = list
    # type<parent_dir> = string
    for parent_dir, list_dir, list_file in os.walk(path_dir):
        for file in list_file:
            process_encrypt(os.path.join(parent_dir, file), key_enc)

    print(SUCCESS_ENCRYPT_DIR)
    return SUCCESS_CODE


def check_decrypt_file(path_file, password):
    result = check_file_exist(0, path_file)
    if result == FILE_NOT_FOUND:
        return FILE_NOT_FOUND

    print('### \nStarting check decrypt file exist...')
    key_dec = get_key_from_password(password)

    try:
        with open(path_file, 'rb') as f_in:
            file_size = struct.unpack('<Q', f_in.read(struct.calcsize('Q')))[0]
            iv = f_in.read(AES.block_size)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            #  Unpack 16 byte -> Decrypt info of old file with AES
            pack_ext_old_file = decryptor.decrypt(f_in.read(16))
            try:
                ext_old_file = struct.unpack('16s', pack_ext_old_file)[0].decode('utf-8').replace("\x00", "")
            except (ValueError, Exception):
                # print(PASSWORD_INCORRECT_MSG)
                return PASSWORD_INCORRECT_CODE

            # a_001.enc -> a.txt
            # Get path file decryption
            temp_path_file, name_file_dec = os.path.split(path_file)
            if len(name_file_dec) > 8:
                path_file_dec = path_file[:-8] + ext_old_file
            else:   # a.enc -> a.txt
                path_file_dec = os.path.splitext(path_file)[0] + ext_old_file

            if os.path.isfile(path_file_dec):
                print(FILE_EXIST_MSG)
                return FILE_EXIST
            else:
                return SUCCESS_CODE
    except (ValueError, Exception):
        print(ERROR_DECRYPT_FILE)
        return ERROR_CODE



    result = process_decrypt(path_file, key_dec, popup)
    if result == SUCCESS_CODE:
        os.remove(path_file)
    return SUCCESS_CODE


# Decrypt all file in directory and sub-directory
def decrypt_dir(path_dir, password, popup):
    result = check_file_exist(1, path_dir)
    if result == DIR_NOT_FOUND:
        return ERROR_CODE

    print('### \nStarting decrypt directory ...')
    key_dec = get_key_from_password(password)

    # Scan directory
    # type<list_dir, list_files> = list
    # type<parent_dir> = string
    for parent_dir, list_dir, list_file in os.walk(path_dir):
        for file in list_file:
            path_file = os.path.join(parent_dir, file)
            ext_file = os.path.splitext(path_file)
            if ext_file[1] == TYPE_ENCRYPT_FILE:  # ext = ".enc"
                result = process_decrypt(path_file, key_dec, popup)
                if result == PASSWORD_INCORRECT_CODE:
                    print(PASSWORD_INCORRECT_MSG)
                    return PASSWORD_INCORRECT_CODE
                if result == SUCCESS_CODE:
                    os.remove(path_file)
    print(SUCCESS_DECRYPT_DIR)
    return SUCCESS_CODE


def main_crypto():
    try:
        parser = argparse.ArgumentParser(description="Add argument to HOST_based IPS crypto function.")
        parser.add_argument('-f', '--file', dest='file', action='store_true', help="Option: Handle file.")
        parser.add_argument('-e', '--encrypt', dest='encrypt_args', action='append', nargs=2,
                            help="Encrypt file/directory.")
        parser.add_argument('-d', '--decrypt', dest='decrypt_args', action='append', nargs=2,
                            help="Decrypt file/directory.")
        parser.add_argument('-p', '--popup', dest='popup_confirm', action='append', type=int)
        # Example: python demo.py [-f] -p 1 -e "C:\Users\Cu Lee\Desktop\Test\a.txt" "abc"

        # Example: python demo.py [-f] -p CONFIRM_DEL -d "C:\Users\Cu Lee\Desktop\Test" "abc"

        args = parser.parse_args()
        encrypt_args = args.encrypt_args
        decrypt_args = args.decrypt_args
        if args.file:
            if encrypt_args is not None:
                return encrypt_file(encrypt_args[0][0], encrypt_args[0][1])
            if decrypt_args is not None:
                if args.popup_confirm[0] == CONFIRM_DEL:
                    return decrypt_file(decrypt_args[0][0], decrypt_args[0][1], CONFIRM_DEL)
                else:
                    return decrypt_file(decrypt_args[0][0], decrypt_args[0][1], SKIP_CODE)
            else:
                return check_decrypt_file(decrypt_args[0][0], decrypt_args[0][1])
        else:
            if encrypt_args is not None:
                return encrypt_dir(encrypt_args[0][0], encrypt_args[0][1])
            if decrypt_args is not None:
                if args.popup_confirm[0] == CONFIRM_DEL:
                    return decrypt_dir(decrypt_args[0][0], decrypt_args[0][1], CONFIRM_DEL)
                else:
                    return decrypt_dir(decrypt_args[0][0], decrypt_args[0][1], SKIP_CODE)
    except (ValueError, Exception):
        print("Da co loi khi su dung tinh nang ma hoa/giai ma file/thu muc.")
        return ERROR_CODE
