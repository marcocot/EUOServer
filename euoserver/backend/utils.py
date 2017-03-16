import base64


def encrypt(message, key):
    return base64.urlsafe_b64encode(message)

def decrypt(message, key):
    return base64.urlsafe_b64decode(message)