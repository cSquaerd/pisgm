#!/usr/bin/python3
# Import modules for CGI handling 
import cgi, cgitb 
import random, base64
import pisgmdb

# Create instance of FieldStorage 
request = cgi.FieldStorage() 

# Get data from fields
if request.getvalue('id'):
  requester_id = request.getvalue('id')
else:
  requester_id = 0

if request.getvalue('group'):
  group_id = request.getvalue('group')
else:
  group_id = 0

#Check for the database to confirm user group combo and returns  keys 
database = r"./data/pigsm.db"
conn = pisgmdb.create_connection(database)
keys = pisgmdb.get_keys(conn, group_id, requester_id )
if keys != []:
    print('keys: ',keys)
 # encrypted_request = keys[1]
else:
    # Return a nonsense result to obscure that the combo does not match
#  encrypted_request = base64.b64encode(str(random.getrandbits(256)).encode('ascii'))
  fake_request = (str(group_id) + str(requester_id) + str(requester_id) + str(group_id))
  fake_request = fake_request.ljust(77, '0').encode('ascii')
  encrypted_request = base64.b64encode(fake_request) 

   
#Respond with the key (content type required by server)
print ("Content-type: text/key\r\n\r");
print (encrypted_request.decode('ascii'), end="");
