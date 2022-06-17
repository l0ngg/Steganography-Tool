from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

from itsdangerous import base64_encode

def generate_key_pair():
    key_pair = RSA.generate(1024)
    private_key = key_pair.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key_pair.publickey().export_key()
    file_out = open("public.pem", "wb")
    file_out.write(public_key)
    file_out.close()
    return key_pair

def encrypt_dome(msg, public_key):
    # do this outside
    # public_key = RSA.import_key(open("receiver.pem").read()
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted = encryptor.encrypt(msg)
    return encrypted

def decrypt_dome(msg, private_key):
    # do this outside
    # private_key = RSA.import_key(open("private.pem").read())
    # private key pem is BOTH private key and public key
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(msg)
    return decrypted

def main():
    # keyPair = RSA.generate(3072)
    # pubKey = keyPair.publickey()
    # print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
    # pubKeyPEM = pubKey.exportKey()
    # generate_key_pair()

    msg = 'secret'
    recipient_key = RSA.import_key(open("D:/github repos/Steganography-Tool/public.pem").read())
    print(f"Public key:  (n={hex(recipient_key.n)}, e={hex(recipient_key.e)})")
    # print(recipient_key.decode('ascii'))
    # encrypted = encrypt_dome(msg, recipient_key)
    encryptor = PKCS1_OAEP.new(recipient_key)
    encrypted = encryptor.encrypt(msg.encode('utf-8'))

    privKeyPEM = RSA.import_key(open("private.pem").read())
    print(f"Private key: (n={hex(privKeyPEM.n)}, d={hex(privKeyPEM.d)})")
    # print(privKeyPEM.decode('ascii'))
    # print(encrypted)
    decrypted = decrypt_dome(encrypted, privKeyPEM)
    # decryptor = PKCS1_OAEP.new(privKeyPEM)
    # decrypted = decryptor.decrypt(encrypted)
    print("Encrypted:", binascii.hexlify(encrypted))
    print('Decrypted:', decrypted.decode('utf-8'))
if __name__ == '__main__':
    main()