```
 charlie  ~  Desktop  pisgm  testing  python                           master 
```

```Python
Python 3.8.2 (default, Apr  8 2020, 14:31:25) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pisgmMain as pisgm
>>> myID = 8270950596653088861
>>> myKeyU = pisgm.rsa.publicKey("../server/testingData/8270950596653088861-U.pem")
>>> myKeyR = pisgm.rsa.privateKey("../server/testingData/8270950596653088861-R.pem")
>>> gid = 3911253593270387734
>>> altID = 4994496195162594573
>>> altKeyU = pisgm.rsa.publicKey("../server/testingData/4994496195162594573-U.pem")
>>> altKeyR = pisgm.rsa.privateKey("../server/testingData/4994496195162594573-R.pem")
>>> reply = pisgm.makeRequest(myKeyR, myID, gid)
Timestamp:  1588100168 
Nonce:  17861839315266020418490476056865978920 
Request:  32 b'^\xa8|H\rp\x10\xab\xb2\xcd\x7f\xca!u\x9fq<\x1c\xba(AHLIUb8MUABd' 
Signature:  256 b"\x8e\xf5([\xc3\xa8\xa8j\xf76A\xfd\xe4\xd9\xb6\x1d\xea\xb8r\xfd\xaa\xa95\xdd\x91\x99\xd3K2&\x19\xc2l\xb4\xc4@\x81:\xd5\xd1\xde\xac\xe9\xb4\xdc\x08\xe9\xf4j\xbf\xb0\xcf\x00N\xfa'8\x1b\xbe\xea\x0b\xf45\x87\x05\xe8!\x8d\xd0v \xd7Z\xad\x86V\x9d\x1en\xdb\x91Ui@;\xd7]\xd6\x0c?\xeal\xa3\x8cABc\x15\x7f2*V\xcc2\x95\x9av\xd4C(D\xfd_`\xe7\xdb\x8bFz\x8e\xc7;,\xbd\xe9\xe7W\x86f\x1bh{\xa6q4\x9f\xea\x05~\x02YH\xbf\x82\x81\xc2\xa9\xd2*\x1fJk\xac\xf2\xed\xeb\xd4\xad\xa5\xa2\xdbh\xc9\x8d\x04\x80jgR,x\x02\xd4n4\xc7oT \xe1P|4\xfdI\xe7\xd91mIg\x03\xe8v\xd1\xd0e\xe9\xee0\x96\x94\xfcH\r\x93\xac\x9a6\x9e\xd2\x80\x92\xd5\xac\x949<{SVH\xaf\xaa\x1c\xafOD\xe1\xaeOh$\xfb\xa3\xd9QO\xc7\x07\x1aa\xf3\xca\xfc\x05\xbd\xca\xf8\x98?\xe2\xfa\xe3,Q"
b'kmzlqsykURr2sR73vvCO9gz1I7zxNOXt8wVMKn+Hmqe9aFQkO0laPUJEz0KDL1/Tc+fYp38bK+LP/2pQ7Tl+5p0dXnDv66CoNnko93AK9Dt0h5Eqg8+7f+Mta15eyfSRczOSwN+ACyPCkdzOWNssV3NcvYicPCo46CkUbDEqpoc5Jvy8HvgbXr/OX+KhyIhm2RIDihInEqM016ORWykJ0bJu+rqSwsj5i8a+qIKK2YaaJjMQyvjJN8bxKFrf1tk6lWPncZyRfSZd65cDmQrD8PMVBLzOKh9JQ96NhlX/EWL0xycWxd+IdzopHh1u5w/FqeVMlMDVkhvQOiHFIF0fpw=='
>>> message = "I've seen things you people wouldn't believe. Attack ships on fire off the Shoulder of Orion. I watched C-Beams, glitter in the dark off a Tannhauser gate. All those, moments, will be lost, in time, like tears... in rain. Time... to die."
>>> image = pisgm.makeImage(message, myID, reply)
526
>>> pisgm.decodeImage(image, myKeyR, myID, gid)
"I've seen things you people wouldn't believe. Attack ships on fire off the Shoulder of Orion. I watched C-Beams, glitter in the dark off a Tannhauser gate. All those, moments, will be lost, in time, like tears... in rain. Time... to die.\n"
>>> pisgm.decodeImage(image, altKeyR, altID, gid)
Decode error: image key not provided.
''
>>> 
```
