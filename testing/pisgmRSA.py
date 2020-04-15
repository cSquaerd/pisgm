from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_OAEP as pkcs1_c
from Crypto.Signature import pkcs1_15 as pkcs1_s
from Crypto.Hash import SHA256 as sha

class keyObj:
	# Constructor
	# Arguments: int keySize, dict keyImport
	# keyImport entries: "public" and "private",
	# either bytes objects with the key data
	# or strings of the key filenames
	def __init__(self, keySize = 2048, keyImport = None):
		if keyImport == None: # Make a new key
			key = rsa.generate(keySize)
			self.keyU = rsa.import_key(key.publickey().export_key())
			self.keyR = rsa.import_key(key.export_key())

		else: # Import the keys if they exist
			if "public" in keyImport.keys(): # Do we have a public key?
				if type(keyImport["public"]) is str: # Is it just the filename?
					try: # Read the key file if so
						keyImport["public"] = open( \
							keyImport["public"], "rb" \
						).read()
					except FileNotFoundError:
						print("Public key file not found...")
						return None
				# Assign the key
				self.keyU = rsa.import_key(keyImport["public"])

			if "private" in keyImport.keys(): # Do we have a private key?
				if type(keyImport["private"]) is str: # Is it just the filename?
					try: # Read the key file if so
						keyImport["private"] = open( \
							keyImport["private"], "rb" \
						).read()
					except FileNotFoundError:
						print("Private key file not found...")
						return None
				# Assign the key
				self.keyR = rsa.import_key(keyImport["private"])

		# See what keys are assigned and create crypt objects for them
		if hasattr(self, "keyU"):
			self.publicCrypt = pkcs1_c.new(self.keyU)
			self.publicSign = pkcs1_s.new(self.keyU)
		if hasattr(self, "keyR"):
			self.privateCrypt = pkcs1_c.new(self.keyR)
			self.privateSign = pkcs1_s.new(self.keyR)

	# Public Key Encrypt Method
	def encryptU(self, message):
		if not hasattr(self, "publicCrypt"):
			raise NotImplementedError("No public key found.")
		if type(message) is str:
			message = bytes(message, "ascii")
		return self.publicCrypt.encrypt(message)
	# Private Key Decrypt Method
	def decryptR(self, cipher):
		if not hasattr(self, "privateCrypt"):
			raise NotImplementedError("No private key found.")
		if type(cipher) is str:
			cipher = bytes(cipher, "ascii")
		return self.privateCrypt.decrypt(cipher)
	
	# Public Key Verify (Decrypt) Method
	def verifyU(self, message, signature):
		if not hasattr(self, "publicSign"):
			raise NotImplementedError("No public key found.")
		if type(message) is str:
			message = bytes(message, "ascii")
		hash = sha.new(message)
		try:
			self.publicSign.verify(hash, signature)
			return True
		except ValueError:
			return False
	# Private Key Sign (Encrypt) Method
	def signR(self, message):
		if not hasattr(self, "privateSign"):
			raise NotImplementedError("No private key found.")
		if type(message) is str:
			message = bytes(message, "ascii")
		hash = sha.new(message)
		return self.privateSign.sign(hash)

class publicKey:
	def __init__(self, rawKeyOrFilename):
		self.key = keyObj(0, {"public": rawKeyOrFilename})
		self.encrypt = self.key.encryptU
		self.verify = self.key.verifyU

class privateKey:
	def __init__(self, rawKeyOrFilename):
		self.key = keyObj(0, {"private": rawKeyOrFilename})
		self.sign = self.key.signR
		self.decrypt = self.key.decryptR
