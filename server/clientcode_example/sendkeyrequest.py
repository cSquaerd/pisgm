import requests, time

# Making a PUT request
keySystemURL = 'https://keys.pisgm.net:5610/keyrequest.py'
#imageKeyRequest = [ ('id', 668992155698351813), ('group', 4319117392286701914), ('request', 'Base64Encoded RSA encrypted with requestor private key timetamp and nonce') ]
imageKeyRequest = [ ('id', 8270950596653088861), \
                    ('group', 3911253593270387734), \
                    ('poster', 8270950596653088861), \
                    ('timestamp', 1587787599), \
                    ('nonce', 2999193110279765663), \
                    ('sig', 'Base64Encoded RSA signature') ]
serverResponse = requests.put(keySystemURL, data = imageKeyRequest)

# print content of request
print(serverResponse.content)

