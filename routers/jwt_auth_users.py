from datetime import datetime, timedelta, timezone
from typing import Annotated

from jose import jwt, JWTError
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET = "2b7aa0b9a39b82bbe7d4dbfa53693fa6a61bcb4083e4fee340d4640c42a5b284"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")

class User(BaseModel):
    username: str
    full_name: str 
    disabled: bool 
    email: str 

class UserDB(User):
    password: str

db = {
    "mouredev":{
        "username": "mouredev",
        "full_name": "Brais Moure",
        "disabled": False,
        "email": "braismoure@mouredev.com",
        "password": "$2a$12$0Mg5e2cFMn2GSnBrvQfs/O2pd9NxkH75f3gNyuAXrcwHRClgNQew6"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "disabled": True,
        "email": "braismoure2@mouredev.com",
        "password": "$2a$12$gDoVeJbErN/nceZpd0qzZewyYmPIlhzdbGmPzXNgQ47HnX69Vozra"
    },
}

# Función para crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default a 15 minutos
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

# Función para autenticar usuarios
def authenticate_user(username: str, password: str):
    user = db.get(username)
    if not user or not verify_password(password, user['password']):
        return False
    return user

# Endpoint para obtener el token
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint protegido que requiere autenticación
@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.get(username)
    user_return = user.pop("password"),user.pop("disabled")
    if user is None:
        raise credentials_exception
    return user
