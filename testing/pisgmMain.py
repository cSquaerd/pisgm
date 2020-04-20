import pisgmRSA as rsa
import pisgmAES as aes
import pisgmImaging as img
from time import time
from PIL.Image import Image 

def makeRequest( \
	# User's private key for signing/decrypting
	keyR : rsa.privateKey, \
	# Server's public key for encryption
	keyU : rsa.publicKey, \
	# User ID
	uid : int \
) -> tuple:
	# Number of seconds since the epoch, raw bytes, big endian
	timestamp = round(time()).to_bytes(4, "big")

	# Random 16 bytes for the nonce
	nonce = aes.grab(16)

	# Combine the ts and nonce with the uid for a 24 byte request
	request = timestamp + nonce + uid.to_bytes(4, "big")

	# Sign the request
	sig = keyR.sign(request)

	print( \
		"Timestamp: ", len(timestamp), timestamp, \
		"\nNonce: ",  len(nonce), nonce, \
		"\nRequest: ", len(request), request, \
		"\nSignature: ", len(sig), sig \
	) #REMOVE AFTER TESTING

	# Encrypt then Transmit the uid, request, and sig to the server using keyU
	# TODO
	
	# Receive a reply, decrypt it to retrieve an AES key
	#aesKey = keyR.decrypt(replyRaw) # ADD IN AFTER TESTING
	aesKey = aes.grab(16) # REMOVE AFTER TESTING

	return (sig, nonce, aesKey)

def makeImage( \
	message: str, \
	sig: bytes, \
	nonce: bytes, \
	aesKey: bytes, \
) -> Image:
	# Pad the message with an extra newline if it's of odd length
	if (len(message) % 2 == 1):
		message += "\n"

	# Make a radio with the key and encrypt the message
	myRadio = aes.aesRadio(aesKey, nonce)
	ciphertext = myRadio.encrypt(message)

	# Reuse the request sig as the header for the image
	imageData = sig + ciphertext
	print(len(imageData))

	# Generate the image
	image = img.bytesToGrayImage(imageData)

	# Finished
	return image



