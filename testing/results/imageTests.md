```Python
Python 3.8.2 (default, Apr  8 2020, 14:31:25) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> m = "I've seen things you people wouldn't believe. Attack ships on fire off the Shoulder of Orion. I watched C-Beams, glitter in the dark off a Tannhause gate. All those moments will be losted, in time, like tears, in rain. Time, to die."
>>> import pisgmImaging as img
>>> import pisgmAES as aes
>>> myradio = aes.
aes.aes            aes.aesDecrypter(  aes.aesEncrypter(  aes.aesRadio(      aes.grab(          
>>> myradio = aes.aesRadio(aes.grab(16))
>>> c = myradio.encrypt(m)
>>> i = img.bytesToGrayImage(c)
>>> img.grayImageToBytes(i) == c
True
>>> img.grayImageToBytes(i)
b'e\xbfX\xd8\xf7I\x1e2\xc4\x83\x9a\xa3\x05\xcb/P\xb7\xc1\r\x96\x92r\xf65\xfa(ZI\xdfY\xc8\xeeB\xbb/\xf2\xaa\xe1\xc0\x02\xe5x\x9a\xd5\x89\x18LKI\xe9\xd5\xc2c"#vDO#\xb5z4ob\x91\x8do8\x1d\x12tW\x17\xd5W\xc3\t\xfe(\xe371s\xd6W\xb2\x80f\xf4\x89!\xe3\x16\xdd\xc0\x82\xdc\x12\x8c}\xe2\xb5D\x08SQ\'\xcaUF\xdcH\x07\xa91v2Jc\x127\xd6\x1d_\x01O\x81\xb7\x8a\xf1GL\x94\xa1\xccAc\x0cXP\xf5\xc1)zD`\xebHZ\xe9Z\xb4\xd0>\x93@"\xf7:\xc8ews>w\xcau\x0f7\x17G\x834\xf0[<\xfb`\x93\xd0i\x054N/8\xf1*\x9e\xee\xe1\xbe\x8f\x8f\x02A\n#\xd7\xc3\xb7o\xea\xddR\xad\xad\xf4\xf4\xbaL\xe0OQ\xb8\x126\x84\xb4\xbf\xc9k\x7f\xdf\xde\xf1\\\xfc\x10Z\xbf\xfc'
>>> i.show()
>>> m2 = "It's too bad she won't live, but then again who does?"
>>> i2 = img.bytesToGrayImage(myradio.encrypt(m + " " + m2))
>>> i2.show()
>>> myradio.decrypt(img.grayImageToBytes(i2))
b"I've seen things you people wouldn't believe. Attack ships on fire off the Shoulder of Orion. I watched C-Beams, glitter in the dark off a Tannhause gate. All those moments will be losted, in time, like tears, in rain. Time, to die. It's too bad she won't live, but then again who does?"
```
