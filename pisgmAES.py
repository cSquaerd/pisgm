from Crypto.Cipher import AES as aes
from Crypto.Random import get_random_bytes as grab

class aesEncrypter:
	def __init__(self, key, nonce, message):
		self.cipher = aes.new(key, aes.MODE_EAX, nonce)
		if type(message) is str:
			message = bytes(message, "ascii")
		self.output = self.cipher.encrypt(message)

class aesDecrypter:
	def __init__(self, key, nonce, ciphertext):
		self.cipher = aes.new(key, aes.MODE_EAX, nonce)
		if type(ciphertext) is str:
			message = bytes(ciphertext, "ascii")
		self.output = self.cipher.decrypt(ciphertext)

class aesRadio:
	def __init__(self, key, nonce=None):
		self.key = key
		if nonce == None:
			self.nonce = grab(32)
			# Use 256 bit keys by default
		else:
			self.nonce = nonce

	def encrypt(self, message):
		return aesEncrypter(self.key, self.nonce, message).output

	def decrypt(self, ciphertext):
		return aesDecrypter(self.key, self.nonce, ciphertext).output

def randomKey256():
	return grab(32)
