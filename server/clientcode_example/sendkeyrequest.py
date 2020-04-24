import requests

# Making a PUT request
keySystemURL = 'https://keys.pisgm.net:5610/keyrequest.py'
#imageKeyRequest = [ ('id', 668992155698351813), ('group', 4319117392286701914), ('request', 'Base64Encoded RSA encrypted with requestor private key timetamp and nonce') ]
imageKeyRequest = [ ('id', 6689092155698351813), ('group', 4319117392286701914), ('request', 'Base64Encoded RSA encrypted with requestor private key timetamp and nonce') ]
serverResponse = requests.put(keySystemURL, data = imageKeyRequest)

# print content of request
print(serverResponse.content)

