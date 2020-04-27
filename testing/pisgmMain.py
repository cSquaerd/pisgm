import pisgmRSA as rsa
import pisgmAES as aes
import pisgmImaging as img
from time import time
from requests import put
from PIL.Image import Image
from base64 import b64decode, b64encode

class Reply:
	def __init__(self, sig, nonce, ts, key):
		self.sig = sig
		self.nonce = nonce
		self.timestamp = ts
		self.aesKey = key

def IDToB64(id : int) -> bytes:
	return b64encode(id.to_bytes(9, "big"))

def B64ToID(id : bytes) -> int:
	return int.from_bytes(b64decode(id), "big")

serverURL = "https://keys.pisgm.net:5610/"

def makeRequest( \
	# User's private key for signing/decrypting
	keyR : rsa.privateKey, \
	# Server's public key for encryption
	keyU : rsa.publicKey, \
	# User ID (who's making the message)
	uid : int, \
	# Group ID (who's reading the message)
	gid : int
) -> Reply:
	# Number of seconds since the epoch, raw bytes, big endian
	timestamp = round(time())

	# Random 16 bytes for the nonce
	nonce = int.from_bytes(aes.grab(16), "big")

	# Encode the uid (9 * 8 / 6 = 12 b64 symbols, each is a byte, 12 bytes)
	uidE = IDToB64(uid)

	# Combine the ts and nonce with the encoded uid for
	# a 4 + 16 + 12 = 32 byte request
	request = timestamp.to_bytes(4, "big") + nonce.to_bytes(16, "big") + uidE

	# Sign the request
	sig = keyR.sign(request)

	# Encode the gid (12 b64 symbols like before with the uid)
	#gidE = IDToB64(gid)

	print( \
		"Timestamp: ", timestamp, \
		"\nNonce: ",  nonce, \
		"\nRequest: ", len(request), request, \
		"\nSignature: ", len(sig), sig \
	) #REMOVE AFTER TESTING

	# Encrypt then Transmit the gid, request, and sig to the server using keyU
	# TODO
	request = [ \
		("id", uid), \
		("group", gid), \
		("poster", uid), \
		("timestamp", timestamp), \
		("nonce", nonce), \
		("sig", b64encode(sig).decode("ascii")) \
	]

	replyRaw = put(serverURL + "keyrequest.py", data = request)
	print(replyRaw.content)
	
	# Receive a reply, decrypt it to retrieve an AES key
	#aesKey = keyR.decrypt(replyRaw) # ADD IN AFTER TESTING
	aesKey = aes.grab(32) # REMOVE AFTER TESTING

	return Reply(sig, nonce.to_bytes(16, "big"), timestamp.to_bytes(4, "big"), aesKey)

def makeImage( \
	message : str, \
	uid : int, \
	reply : Reply, \
) -> Image:
	# Pad the message with an extra newline if it's of odd length
	if (len(message) % 2 == 1):
		message += "\n"

	# Make a radio with the key and encrypt the message
	myRadio = aes.aesRadio(reply.aesKey, reply.nonce)
	ciphertext = myRadio.encrypt(message)

	# Reuse the request sig as the header for the image
	imageData = reply.timestamp + reply.nonce + IDToB64(uid) + reply.sig + ciphertext
	print(len(imageData))

	# Generate the image
	image = img.bytesToGrayImage(imageData)

	# Finished
	return image

def decodeImage( \
	image : Image, \
	uid : int, \
	keyU : rsa.publicKey \
) -> bytes:
	raw = img.grayImageToBytes(image)

	timestamp = raw[:4]
	nonce = raw[4:20]
	uide = raw[20:32]
	sig = raw[32:288]
	
	if B64ToID(uide) == uid:
		print("UIDs match.")
		if keyU.verify(timestamp + nonce + uide, sig):
			print("Signature verified.")
			return raw[4 + 16 + 12 + 256 : ]
		else:
			print("Bad signature...")
	else:
		print("UIDs do not match...")
