#!/usr/bin/python3
# Import modules for CGI handling
import cgi
import pisgmdb
#Respond with the key (content type required by server)
print ("Content-type: text/key\r\n\r");

# Create instance of FieldStorage
request = cgi.FieldStorage()

# Get data from fields
if request.getvalue('id'):
    #Get the key from request
    uid = request.getvalue('id')
    #add public key to database and get user_id
    database = r"./data/pigsm.db"
    conn = pisgmdb.create_connection(database)
    #add search for user here
    print(new_user_id) 

else:
    print("ERROR - USER ID PROVIDED", end="")


