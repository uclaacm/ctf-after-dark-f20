# file signature for png
key = [137, 80, 78, 71, 13, 10, 26, 10]

def xor(s1, key):
    res = [chr(0)]*8
    for i in range(len(res)):
        q = ord(s1[i])
        d = key[i]
        k = q ^ d
        res[i] = chr(k)
    res = ''.join(res)
    return res
with open('encrypted.png') as f:
    res = f.read()

# decrypt the file
enc_data = ''
for i in range(0, len(res), 8):
    enc = xor(res[i:i+8], key)
    enc_data += enc

# write the decrypted image out
with open('decrypt.png', 'wb') as f:
    f.write(enc_data)
