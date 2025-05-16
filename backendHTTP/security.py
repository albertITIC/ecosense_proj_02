from passlib.context import CryptContext

# Configuración para bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Converteix una contrasenya plana en text hash"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contrasenyaa en text pla amb la versió hashejada"""
    return pwd_context.verify(plain_password, hashed_password)