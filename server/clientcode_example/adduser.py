import requests

# Making a PUT request
addSystemURL = 'https://keys.pisgm.net:5610/adduser.py'
addKeyRequest = [ ('public_key',  'Base64Encoded RSA public key for this user without any encryption') ]
serverResponse = requests.put(addSystemURL, data = addKeyRequest)

# print content of request
print(serverResponse.content)
