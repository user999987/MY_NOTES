'''
key =2 xyz->zab
ord变成数字取余数操作
'''


def caesarCipherEncryptor(string, key):
    new_string = ''
    a_code = ord('a')
    for s in string:
        new_string += chr((ord(s)-a_code+key) % 26+a_code)
    return new_string
