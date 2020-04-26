#!/usr/bin/python3
# Import modules for CGI handling 
import cgi, cgitb 
import random, base64
import pisgmdb
import pisgmRSA as rsa
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


#Set the HTTP header required for all responses
print ("Content-type: text/key\r\n\r");

# Create instance of FieldStorage 
request = cgi.FieldStorage() 

# Get data from fields
if request.getvalue('id'):
    uid = int(request.getvalue('id'))
else:
    print("Invalid Request", end="")
    exit()

if request.getvalue('group'):
    gid = int(request.getvalue('group'))
else:
    print("Invalid Request", end="")
    exit()

if request.getvalue('poster'):
    pid= int(request.getvalue('poster'))
else:
    print("Invalid Request", end="")
    exit()


if request.getvalue('timestamp'):
    timestamp = int(request.getvalue('timestamp'))
else:
    print("Invalid Request", end="")
    exit()

if request.getvalue('nonce'):
    nonce = int(request.getvalue('nonce'))
else:
    print("Invalid Request", end="")
    exit()

if request.getvalue('sig'):
    sig = request.getvalue('sig')
else:
    print("Invalid Request", end="")
    exit()

#Check for the database to confirm user group combo and returns  keys 
database = r"./data/pisgm.db"
conn = pisgmdb.create_connection(database)
userkey, masterkey = pisgmdb.get_keys(conn, gid, uid)
print('1')
#convert masterkey from Base64 as stored if DB
masterkey = base64.b64decode(masterkey)
#generate the key for permutation from the request information
permutekey = gid.to_bytes(8, byteorder='big') \
        + pid.to_bytes(8, byteorder='big') \
        + timestamp.to_bytes(8, byteorder='big') \
        + nonce.to_bytes(8, byteorder='big')

# generate the image key by encrypting the master key with the permutation key
keyChanger = AES.new(permutekey, AES.MODE_ECB)
imagekey = keyChanger.encrypt(masterkey)

# encrypt the image key with the requester public key
userPublic = RSA.import_key(userkey)
cipher_rsa = PKCS1_OAEP.new(userPublic)
enc_imagekey = cipher_rsa.encrypt(imagekey)
print(base64.b64encode(enc_imagekey).decode(), end="")

