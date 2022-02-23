## RSA

This is a pure python implementation of the RSA encryption algorithm. You can install the pip package with `pip install rsa_python`. Below is an example of how to use the module:

```py
from rsa_python import rsa
key_pair = rsa.generate_key_pair(1024)
cipher = rsa.encrypt("Hello World!", key_pair["public"], key_pair["modulus"])
decrypted_message = rsa.decrypt(cipher, key_pair["private"], key_pair["modulus"])
print(decrypted_message)
```

More information on [pypi.org/project/rsa-python](https://pypi.org/project/rsa-python/).
