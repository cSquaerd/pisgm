#!/usr/bin/python3
# Import modules for CGI handling 
import cgi, cgitb 
import random
import string

# ---------------
def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
# ------------------------------

# Create instance of FieldStorage 
request = cgi.FieldStorage() 

# Get data from fields
if request.getvalue('id'):
  requester_id = request.getvalue('id')
else:
  requester_id = 'NONE'

if request.getvalue('group'):
  group_id = request.getvalue('group')
else:
  group_id = 'NONE'

if request.getvalue('request'):
  encrypted_request = request.getvalue('request') + (randomString(100))
else:
  encrypted_request = randomString(160)

   
#Do Stuff

#Respond with the key (content type required by server)
print ("Content-type: text/key\r\n\r");
print (encrypted_request, end="");
