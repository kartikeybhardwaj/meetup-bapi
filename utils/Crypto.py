import hashlib
import base64

class Crypto:
    
    def __init__(self, value):
        self.__value = value

    def SHA256(self):
        return base64.b64encode(hashlib.sha256(self.__value.encode('utf-8')).digest()).decode("utf-8")
