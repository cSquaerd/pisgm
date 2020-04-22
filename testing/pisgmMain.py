import pisgmRSA as rsa
import pisgmAES as aes
import pisgmImaging as img
from time import time
from PIL.Image import Image

class Reply:
	def __init__(self, sig, nonce, key):
		self.sig = sig
		self.nonce = nonce
		self.aesKey = key

def makeRequest( \
	# User's private key for signing/decrypting
	keyR : rsa.privateKey, \
	# Server's public key for encryption
	keyU : rsa.publicKey, \
	# User ID (who's making the message)
	uid : str, \
	# Group ID (who's reading the message)
	gid : str
) -> tuple:
	# Number of seconds since the epoch, raw bytes, big endian
	timestamp = round(time()).to_bytes(4, "big")

	# Random 16 bytes for the nonce
	nonce = aes.grab(16)

	# Combine the ts and nonce with the uid for a 30 byte request
	request = timestamp + nonce + bytes(uid, "ascii") #uid.to_bytes(4, "big")

	# Sign the request
	sig = keyR.sign(request)

	print( \
		"Timestamp: ", len(timestamp), timestamp, \
		"\nNonce: ",  len(nonce), nonce, \
		"\nRequest: ", len(request), request, \
		"\nSignature: ", len(sig), sig \
	) #REMOVE AFTER TESTING

	# Encrypt then Transmit the gid, request, and sig to the server using keyU
	# TODO
	
	# Receive a reply, decrypt it to retrieve an AES key
	#aesKey = keyR.decrypt(replyRaw) # ADD IN AFTER TESTING
	aesKey = aes.grab(32) # REMOVE AFTER TESTING

	return Reply(sig, nonce, aesKey)

def makeImage( \
	message : str, \
	reply : Reply, \
) -> Image:
	# Pad the message with an extra newline if it's of odd length
	if (len(message) % 2 == 1):
		message += "\n"

	# Make a radio with the key and encrypt the message
	myRadio = aes.aesRadio(reply.aesKey, reply.nonce)
	ciphertext = myRadio.encrypt(message)

	# Reuse the request sig as the header for the image
	imageData = reply.sig + ciphertext
	print(len(imageData))

	# Generate the image
	image = img.bytesToGrayImage(imageData)

	# Finished
	return image



