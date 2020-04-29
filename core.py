# My wrapper object files for PyCryptoDome routines
import pisgmRSA as rsa
import pisgmAES as aes
import pisgmImaging as img

# For timestamps
from time import time
# For server key requests
from requests import put
from base64 import b64decode, b64encode
# For type-hint in decodeImage()
from PIL.Image import Image

# Storage object with new image data to pass to makeImage()
class Reply:
	def __init__(self, sig, nonce, ts, key):
		self.sig = sig
		self.nonce = nonce
		self.timestamp = ts
		self.aesKey = key

# UID encode/decode functions for signature generation 
def IDToB64(id : int) -> bytes:
	return b64encode(id.to_bytes(9, "big"))

def B64ToID(id : bytes) -> int:
	return int.from_bytes(b64decode(id), "big")

serverURL = "https://keys.pisgm.net:5610/"

# Request a new key to make a new encrypted image with
def makeRequest( \
	# User's private key for signing/decrypting
	keyR : rsa.privateKey, \
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
	requestBytes = timestamp.to_bytes(4, "big") + nonce.to_bytes(16, "big") + uidE

	# Sign the request
	sig = keyR.sign(requestBytes)

	# Encode the gid (12 b64 symbols like before with the uid)
	#gidE = IDToB64(gid)

	print( \
		"Timestamp: ", timestamp, \
		"\nNonce: ",  nonce, \
		"\nRequest: ", len(requestBytes), requestBytes, \
		"\nSignature: ", len(sig), sig \
	) #REMOVE AFTER TESTING

	request = [ \
		("id", uid), \
		("group", gid), \
		("poster", uid), \
		("timestamp", timestamp), \
		("nonce", nonce), \
		("sig", b64encode(sig).decode("ascii")) \
	]

	# Receive a reply, decrypt it to retrieve an AES key
	replyRaw = put(serverURL + "keyrequest.py", data = request)
	print(replyRaw.content)

	try:
		aesKey = keyR.decrypt(b64decode(replyRaw.content))
	except ValueError:
		print("Request error: no key issued.")
		return None

	# Return the binary data necessary for the image header and the new key	
	return Reply(sig, nonce.to_bytes(16, "big"), timestamp.to_bytes(4, "big"), aesKey)

# With a new key and its signature data in a Reply object, encrypt a message and
# create an image with the ciphertext as the pixel values
def makeImage( \
	# The message to encrypt
	message : str, \
	# UID for the message author
	uid : int, \
	# Object containing header data and an AES Key for this message
	reply : Reply \
) -> Image:
	# Pad the message with an extra newline if it's of odd length
	if (len(message) % 2 == 1):
		message += "\n"

	# Make a radio with the key and encrypt the message
	myRadio = aes.aesRadio(reply.aesKey, reply.nonce)
	ciphertext = myRadio.encrypt(message)

	# Reuse the request sig as the header for the image
	# along with the data that made the sig in the first place
	imageData = reply.timestamp + reply.nonce + IDToB64(uid) + reply.sig + ciphertext
	print(len(imageData))

	# Generate the image
	image = img.bytesToGrayImage(imageData)

	# Finished
	return image

# Given an image, extract its header data,
# ask the server for the image's key,
# then potentially decrypt the ciphertext in the image
# to retrieve the original message
def decodeImage( \
	# The image containing a message to be decoded
	image : Image, \
	# The private key of the decoder user
	keyR : rsa.privateKey, \
	# The uid of the decoder user
	uid : int, \
	# The gid of the decoder user (should match the encoder user)
	gid : int \
) -> str:
	# Extract the image data
	raw = img.grayImageToBytes(image)

	# Extract the data that made the original signature
	timestamp = raw[:4]
	nonce = raw[4:20]
	uidEncoder = raw[20:32]

	# Recreate the signature for the key but with the decoder's key
	sig = keyR.sign(timestamp + nonce + uidEncoder)

	# Extract the ciphertext
	ciphertext = raw[288:]

	# Create a key retrieval request
	request = [ \
		("id", uid), \
		("group", gid), \
		("poster", B64ToID(uidEncoder)), \
		("timestamp", int.from_bytes(timestamp, "big")), \
		("nonce", int.from_bytes(nonce, "big")), \
		("sig", b64encode(sig).decode("ascii")) \
	]

	# Request the key	
	replyRaw = put(serverURL + "keyrequest.py", data = request)

	# See if the key was granted
	try:
		aesKey = keyR.decrypt(b64decode(replyRaw.content))
	except ValueError:
		print("Decode error: image key not provided.")
		return ""

	# With the key granted, decrypt the ciphertext and return the original message
	decrypter = aes.aesRadio(aesKey, nonce)
	return decrypter.decrypt(ciphertext).decode("ascii")

