from fastapi import APIRouter, Depends,HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

class User(BaseModel):
    username: str
    full_name: str
    disabled: bool
    email: str

class UserDB(User):
    password: str

db = {
    "mouredev":{
        "username": "Mouredev",
        "full_name": "Brais Moure",
        "disabled": False,
        "email": "braismoure@mouredev.com",
        "password": "123456"
    },
    "mouredev2":{
        "username": "Mouredev2",
        "full_name": "Brais Moure 2",
        "disabled": True,
        "email": "braismoure2@mouredev.com",
        "password": "654321"
    },
}

def search_user_db(username:str):
    if username in db:
        return UserDB(**db[username])

def search_user(username:str):
    if username in db:
        return User(**db[username])

async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciales de autorizacion invalidas", headers={"WWW-Authenticate":"Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    dbs = db.get(form.username)
    if not dbs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta")
    
    return {"acces token": user.username, "token type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user