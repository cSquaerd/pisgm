#!/usr/bin/python3
# Import modules for CGI handling
import cgi, cgitb
import  base64
import pisgmdb
#Respond with the key (content type required by server)
print ("Content-type: text/key\r\n\r");

# Create instance of FieldStorage
request = cgi.FieldStorage()

# Get data from fields
if request.getvalue('public_key'):
    #Get the key from request
    public_key = request.getvalue('public_key')
    #add public key to database and get user_id
    database = r"./data/pigsm.db"
    conn = pisgmdb.create_connection(database)
    new_user_id = pisgmdb.create_user(conn, public_key )
    print(new_user_id) 

else:
    print("ERROR - NO PUBLIC KEY PROVIDED")


