import base64

def encrypt(message, key):
    """ Encrypt a message using a key """
    return base64.urlsafe_b64encode(message)

def decrypt(content, key):
    """ Decrypt a message using a key """
    return base64.urlsafe_b64decode(content)

