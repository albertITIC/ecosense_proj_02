# Fitxer per protegir les contrasenyes
import bcrypt

def hash_contrasenya(contrasenya: str) -> str:
    return bcrypt.hashpw(contrasenya.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_contrasenya(contrasenya: str, hashed: str) -> bool:
    return bcrypt.checkpw(contrasenya.encode('utf-8'), hashed.encode('utf-8'))