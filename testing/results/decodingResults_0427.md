```Python
Python 3.8.2 (default, Apr  8 2020, 14:31:25) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pisgmMain as pisgm
>>> k = pisgm.rsa.keyObj()
>>> u = pisgm.rsa.publicKey(k.exportU())
>>> r = pisgm.rsa.privateKey(k.exportR())
>>> uid = 13
>>> gid = 1999
>>> reply = pisgm.makeRequest(r, u, uid, gid)
Timestamp:  1588005015 
Nonce:  331525483944465031077080877142910428073 
Request:  32 b'^\xa7\x08\x97\xf9i|U\xe4i\x86\xa5\xaa\x88\xae\xb6=\x13\xe3\xa9AAAAAAAAAAAN' 
Signature:  256 b'\x01Z\x0bX\n\xee\xed\xc3>\x15\xa1\xe4N\xaah\x1e\xab\x10\xc0UBG\x04\xe4\x12\xa2\x8dT\xcev\x95\xf2\xc6\t\x9b\xfa\xc1\x9d\xee\xad\x91\xf7\xdcv`\xfc\x17\x90HE\xb2\x1eH\xf0S\x11\xe6U\xa3m\xa5?\xf1\x90)W0J\x95\xcf\'e\x991o\x1b\x11o \xa3\x96\x99c"x\x84<\x91\xbb,4fu\xd5\t\x16bG\xc7h\xfb\x9c\x97Lia\x0f\xc7\xc0.\x8b\xe4\xb6J\xdd\xc7"\xe3w\xc9\xff\x8e\xb6\x03\x84\xf7\xa6\xfc\x97\x9ez\x1e\xe6\x81\xa4\xbe\xd8jcv\x1c\x8c$\xc4h\x16\xcc\xd7\xc9\x8d\x10zw&\x8a\x10\xc1\xean\x13\x00\x07\xae:]\x82\x12i\xa1\x82\xf9Vb\x86\xb1\xb6\x9f)\xf4i9\xdf+\xedL\xc5\xf4}\xfe\x190\xb4\xe38\x96L\x9b@\xd45\x1d\xb3\xde9\x9bO\xfa\x89\xdf9Q"\nn\n\x1by\xe6 \x82\xe6\x0c9O\xafCF\x9cD\xe2\xdf\x14f\x96\x1d\xb8\x89\n\xff\x8f\xdd\xf7\xcf\xfa\x1d\xc7\xf0\xd46\xe2\x05\x8f\xf9G\xf6"'
b''
>>> message = "I've seen things you people wouldn't believe. Attack ships on fire off the Shoulder of Orion. I watched C-Beams, glitter in the dark off a Tannhauser gate. All those, moments, will be lost, in time, like tears... in rain. Time... to die."
>>> image = pisgm.makeImage(message, uid, reply)
526
>>> decoded = pisgm.decodeImage(image, uid, u)
UIDs match.
Signature verified.
>>> deciphered = pisgm.decodeRequest(decoded, r)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/charlie/Desktop/pisgm/testing/pisgmMain.py", line 153, in decodeRequest
    return decrypter.decrypt(imageData.ciphertext).decode("ascii")
UnicodeDecodeError: 'ascii' codec can't decode byte 0xa9 in position 1: ordinal not in range(128)
>>> decoded
<pisgmMain.DecodedImage object at 0x7ff9759f2b80>
>>> decoded.
decoded.ciphertext  decoded.nonce       decoded.timestamp   decoded.uid         
>>> decoded.ciphertext
b'\x03\xba\x95f\xa0\x95ei\x0c\xefq\xfc\xc5\xba\xb6\xd2\x97\xc5>\xc0\x87\x11R\x9b\xcd\xe4\xb0K\xac%L\x19\xab\x9f\xd9K\xf6i\x13\n\xd0J$\xc0\x7f|\xccH\x18\xbd\xcb\x9f\x13gG6\xde\xf3hk\xedI\xa4zf+\xef7N\xdd%x\xc5\x12\xde\xbfV\x07\x83\xda\x94"le\x98\xb7n)2@\xc2@\x99\x8bn\xdf\x16\x04`\xa2\x1d\x86\xf9\xbe\xf1\x08\x87\x890\n^\xe4!\xb5\xadRc\xe0\x1d]\xfeFM;\x01\xba[\xbe2S\xcd.*:d\x89m\xc9X1M\xa9\xc4\xfa1\x91g1Jj}l\xf8\xa5\xd8r%o!nW\xcc\xf1\xa7/\xcb\xf7\xc0eE(\x96lE\xc2\xfd\x99\xf1\x17\x8c{\xbe4R\x00Y\x02\xcb\xc9\xa2q?\xc86n\x07o\x084\xe5\x8d\xa0\xd3.\xdf\xd6\xccQD\xc9\xfci\xf9\xc4\xae\x8d\xa2\x8fq\xe1\xc7\x10!\xd1\xb6\x1a\x90?\x91\x94\xc9M&\x81\x85\x18\xf0\x1d'
>>> pisgm.aes.aesRadio(reply.aesKey, decoded.nonce).decrypt(decoded.ciphertext).decode("ascii")
"I've seen things you people wouldn't believe. Attack ships on fire off the Shoulder of Orion. I watched C-Beams, glitter in the dark off a Tannhauser gate. All those, moments, will be lost, in time, like tears... in rain. Time... to die.\n"
>>> len(message)
237
```
