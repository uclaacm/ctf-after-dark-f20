#!/usr/bin/env python

def xor(s1, key):
    res = [chr(0)]*8
    for i in range(len(res)):
        q = ord(s1[i])
        d = key[i]
        k = q ^ d
        res[i] = chr(k)
    res = ''.join(res)
    return res

def add_pad(msg):
    l = 8-len(msg)%8
    msg += chr(0)*l
    return msg

with open('flag.png') as f:
    data = f.read()

data = add_pad(data)

encrypted = ''
for i in range(0, len(data), 8):
    enc = xor(data[i:i+8], key)
    encrypted += enc

with open('encrypted.png', 'wb') as f:
    f.write(encrypted)