import rsa
import re
# generate public and private keys with
# rsa.newkeys method,this method accepts
# key length as its parameter
# key length should be atleast 16
def generate_keys():
    key1, key2 = rsa.newkeys(512)
    return key1, key2

# rsa.encrypt method is used to encrypt
# string with public key string should be
# encode to byte string before encryption
# with encode method
def encrypt_message(msg, pub_key):
    arr = pub_key.split(',')
    key1 = rsa.PublicKey( int(arr[0][10::]), int(arr[1][1:-1:]) )
    enc_message = rsa.encrypt(msg.encode(), key1)
    return enc_message

# the encrypted message can be decrypted
# with ras.decrypt method and private key
# decrypt method returns encoded byte string,
# use decode method to convert it to string
# public key cannot be used for decryption
def decrypt_message(msg, priv_key):
    arr = priv_key.split(',')
    key2 = rsa.PrivateKey(int(arr[0][11::]), int(arr[1]), int(arr[2]), int(arr[3]), int(arr[4][1:-1:]) )
    dec_message = rsa.decrypt(msg, key2).decode()
    return dec_message

if __name__ == '__main__':
    public_key1, private_key2 = rsa.newkeys(512)
    message = 'testing'
    
    enc1 = encrypt_message(message, str(public_key1))
    enc2 = decrypt_message(enc1, str(private_key2))
    print("encrypted message:", enc1, "\n")
    print("decrypted message:", enc2)
    
    # public_key1 = str(public_key1)
    # print(public_key1)
    # print(public_key1.split(',')[0][10::])
    # print(public_key1.split(',')[1][:-1:])