# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción: clase test para generar password en caso de no recordarlo


import hashlib
import crypt
# To encrypt the password. This creates a password hash with a random salt.
password_hash = crypt.crypt("darwin12")
print(password_hash)

# To check the password.
##valid_password = crypt.crypt(cleartext, password_hash) == password_hash

def make_password(password):
    hash = hashlib.md5(str.encode(password)).hexdigest()
    return hash

def check_password(hash, password):
    """Generates the hash for a password and compares it."""
    generated_hash = make_password(password)
    return hash == generated_hash

hash=make_password('darwin12')
print(hash)

#secret key qsjr==@6$x$vle50^d7l99vcyel1tr^=_s4z01v2xpo#pbr$n3
#pbkdf2_sha256$100000$4S9gioAaDi6E$2vER4RqoZdg9tQhwauSqwbJdJXczU8V/CYsXTkhZHmo=