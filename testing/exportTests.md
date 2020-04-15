```
Python 3.8.2 (default, Apr  8 2020, 14:31:25) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pisgmRSA
>>> k = pisgmRSA.keyObj()
>>> u = pisgmRSA.publicKey(k.exportU())
>>> r = pisgmRSA.privateKey(k.exportR())
>>> u
<pisgmRSA.publicKey object at 0x7fb7f640fe80>
>>> r
<pisgmRSA.privateKey object at 0x7fb7f5d19c10>
>>> r.decrypt(u.encrypt("Hello World!!!"))
b'Hello World!!!'
>>> m = "A long time ago, in a galaxy far, far away..."
>>> u.verify(m, r.sign(m))
True
>>> u.verify(m[:len(m) - 1], r.sign(m))
False
>>> m[:len(m) - 1]
'A long time ago, in a galaxy far, far away..'
>>> u.export()
b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3CQPZU9td+RpVbRoHDEE\nzKIhGj9NTrY0TmwAWS42OUsnD5vg0ikXMmazqlAwsAvpLrK1IPv6sb53OWtBlYM0\nm6G3iZpXXqA/9pqd2znj4XyHcAh2VuJ3Wj5hbYOV1ArH39xUEAk6WuOhsaFTSrql\n2qE6VfS7h40zsysQO8Jjo6reCunWHcuiINyXChCd50kPx2Dl0AnPLXLddwxCm3Kx\nV6xTzwUpBlSnSGiBt9OEUmng5pVVswtmrFtVePX360F/tjWv1Gcb/Ph6dkP+x7Og\nPGsV6Kzy8bGNxcUT6RSH7kyktmYw3sQUDqe+Ba7cmnFUrY3pgZtuSixl7Iq1i2zE\nIwIDAQAB\n-----END PUBLIC KEY-----'
>>> r.export()
b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA3CQPZU9td+RpVbRoHDEEzKIhGj9NTrY0TmwAWS42OUsnD5vg\n0ikXMmazqlAwsAvpLrK1IPv6sb53OWtBlYM0m6G3iZpXXqA/9pqd2znj4XyHcAh2\nVuJ3Wj5hbYOV1ArH39xUEAk6WuOhsaFTSrql2qE6VfS7h40zsysQO8Jjo6reCunW\nHcuiINyXChCd50kPx2Dl0AnPLXLddwxCm3KxV6xTzwUpBlSnSGiBt9OEUmng5pVV\nswtmrFtVePX360F/tjWv1Gcb/Ph6dkP+x7OgPGsV6Kzy8bGNxcUT6RSH7kyktmYw\n3sQUDqe+Ba7cmnFUrY3pgZtuSixl7Iq1i2zEIwIDAQABAoIBADMdtmt2TXtc0K6j\nZNdC9JPVg602DKvdt/iLsGsExXd5QVko/0OdYfMEkOxXkW6XXW5H9bHygIwcJ0/w\nXTqrzB/lJZpweaARwrhuv3/Diev2P/aeKGhVTpRoTrQgrT4ewLl0zhopImEvYQC/\nbnk4LMG+1S5XVOINQfd05OCTaxJ58KyhPpamikCKxJJLfxsgh+d7z2oC2Rdc4Bv9\nEwYdDQDFfKGiaI9OVHzulTLYI+jZVQHfo3YC0o8XYID2YkMN7y5wlA13ibryY09D\nWvfg3tFJE1IcFFSg4/4SbSJ6MflviW6GfgVJzqBFLOKoy+ZZK14XPNL4zAYYaQUy\nXb1mbWECgYEA56+7qH6ck1dMoD6s6IjwyRMqFMvYyX21HnjrAijVnOc9rchkFseg\nArrZ85GrZgA7wkGBsuKKvgzD3oYN8niYS1bH/iikC4nMZh6Py52Cpm4RajMS3H7S\nWKLw3nBV3HLOQU8uXpyn6QBCNakhVn9FavFJrI1lZU921LFB01wIbyECgYEA8z4n\ndC/Bmi3eGo7+pcWTQ7wIeLeCUP1rteCG9jj+lRxi0Lyd7BIPWJXiBwnYxQ0k3HgZ\nQfAu9TgBuU8QLGKZsKchi8kOp2aLc5/AvuhIVLSBAkjT6I+rMItIXcwhKvRZGllz\nLfiY+j5nVH/0BhdRZhwlXqvuHjHSVzVKD+vyXsMCgYEAhTPs0UfR34hOfsbqBFtP\nDFvfUsuMHPQQIK/mdXxiq+3q8TIIEWy+GzOwQTAb+e3ibaHZ3q4OlIukRRiPhjs9\nW/tNyls1TYjxIjkp9SfeyK75hjRNAMZNSzaLA2hUhQTgfn32q+CnTPegGVfe2esc\nTwrgj7tPc3rHWCt9K/Z6xuECgYEAuQcChAL/xgQ1+wXi9r5/8vpJh2owGuNq14Lf\nptRb85kQIbAYgMaMHdqFgM0gs2P4Miy5KctGLQpZZVia+OhX+GRpxCdAml4Knf1b\nZNzUiHp12AMGDtWaZubMOW1ZnY8ZaE26q7F6zIBDoadjPG7oYD/wvT8Tdqx3UBcd\nK1dTmnkCgYB9xmDnTAVDMJQnQMRMGuAcIh2ISkhV4R+Ovq/kqhKRosl9+/59jlkV\nlrw2vhXd01RHll0jqwfsV8hTYaJJWk1cOng/9oW3QYukMgc+p0GcFF8jdOrwRfNX\nZ4vvzwPR1k6oaXIprgZhDzhGPfbY+YsyxDa2hI2Nyu6vn+3hEf/EqQ==\n-----END RSA PRIVATE KEY-----'
>>> exit()
```
