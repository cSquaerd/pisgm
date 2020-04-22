import pisgmRSA as rsa
import pisgmAES as aes
import pisgmImaging as img
from time import time
from PIL.Image import Image
from base64 import b64decode, b64encode

class Reply:
	def __init__(self, sig, nonce, key):
		self.sig = sig
		self.nonce = nonce
		self.aesKey = key

def IDToB64(id : int) -> bytes:
	return b64encode(id.to_bytes(9, "big"))

def B64ToID(id : bytes) -> int:
	return int.from_bytes(b64decode(id), "big")

def makeRequest( \
	# User's private key for signing/decrypting
	keyR : rsa.privateKey, \
	# Server's public key for encryption
	keyU : rsa.publicKey, \
	# User ID (who's making the message)
	uid : int, \
	# Group ID (who's reading the message)
	gid : int
) -> tuple:
	# Number of seconds since the epoch, raw bytes, big endian
	timestamp = round(time()).to_bytes(4, "big")

	# Random 16 bytes for the nonce
	nonce = aes.grab(16)

	# Encode the uid (9 * 8 / 6 = 12 b64 symbols, each is a byte, 12 bytes)
	uidE = IDToB64(uid)

	# Combine the ts and nonce with the encoded uid for
	# a 4 + 16 + 12 = 32 byte request
	request = timestamp + nonce + uidE

	# Sign the request
	sig = keyR.sign(request)

	# Encode the gid (12 b64 symbols like before with the uid)
	gidE = IDToB64(gid)

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



