from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_OAEP as pkcs1

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
			self.publicCrypt = pkcs1.new(self.keyU)
		if hasattr(self, "keyR"):
			self.privateCrypt = pkcs1.new(self.keyR)

	# Public Key Encrypt Method
	def encryptU(self, message):
		if not hasattr(self, "publicCrypt"):
			raise NotImplementedError("No public key found.")
		if type(message) is str:
			message = bytes(message, "ascii")
		return self.publicCrypt.encrypt(message)
	# Private Key Encrypt Method
	def encryptR(self, message):
		if not hasattr(self, "privateCrypt"):
			raise NotImplementedError("No private key found.")
		if type(message) is str:
			message = bytes(message, "ascii")
		return self.privateCrypt.encrypt(message)
	# Private Key Decrypt Method
	def decryptR(self, cipher):
		if not hasattr(self, "privateCrypt"):
			raise NotImplementedError("No private key found.")
		if type(cipher) is str:
			cipher = bytes(cipher, "ascii")
		return self.privateCrypt.decrypt(cipher)

class publicKey:
	def __init__(self, rawKeyData):
		self.key = keyObj(0, {"public": rawKeyData})
		self.encrypt = self.key.encryptU

class privateKey:
	def __init__(self, rawKeyData):
		self.key = keyObj(0, {"private": rawKeyData})
		self.encrypt = self.key.encryptR
		self.decrypt = self.key.decryptR
