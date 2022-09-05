import base64
import getpass
# enctry 
def enctry(s):
    k = 'abcdefg1234567890'
    encry_str = ""
    for i,j in zip(s,k): # i為字符，j為秘鑰字符
        temp = str(ord(i)+ord(j))+'_' # 加密字符 = 字符的Unicode碼 + 秘鑰的Unicode碼
        encry_str = encry_str + temp
    s1 = base64.b64encode(encry_str.encode("utf-8"))
    return s1

# dectry
def dectry(s2):
    p = base64.b64decode(s2).decode("utf-8")
    k = 'abcdefg1234567890'
    dec_str = ""
    for i,j in zip(p.split("_")[:-1],k): # i 為加密字符，j為秘鑰字符
        temp = chr(int(i) - ord(j)) # 解密字符 = (加密Unicode碼字符 - 秘鑰字符的Unicode碼)的單字節字符
        dec_str = dec_str+temp
    return dec_str

a1 = enctry("AAA123456786")
a2 = dectry(a1)
print(a2)