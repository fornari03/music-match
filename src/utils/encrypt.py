import hashlib

# criptografa uma senha
def encrypt_password(password: str):
        if password == None:
                return None
      
        hash_object = hashlib.sha256()
        hash_object.update(password.encode())
        hash_password = hash_object.hexdigest()
        
        return hash_password