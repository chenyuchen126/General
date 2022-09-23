# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import base64

def get_key():
    return "badfdfeatretq44315u3iu8aut8471409754ut94q8718495984utq94qutq984t"

# enctry 
def enctry(s):
    k = get_key()
    encry_str = ""
    for i,j in zip(s,k): 
        temp = str(ord(i)+ord(j))+'_' 
        encry_str = encry_str + temp
    s1 = base64.b64encode(encry_str.encode("utf-8"))
    return s1

# dectry
def dectry(s2):
    p = base64.b64decode(s2).decode("utf-8")
    k = get_key()
    dec_str = ""
    for i,j in zip(p.split("_")[:-1],k): 
        temp = chr(int(i) - ord(j)) 
        dec_str = dec_str+temp
    return dec_str

a1 = enctry("AAA123456786")
a2 = dectry(a1)
print(a2)
