from fastapi import APIRouter, HTTPException
from pydantic import *

router = APIRouter()

# ENTIDAD USER

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str

users_list = [User(id= 1,name="Daniel",surname="Saenz",age=14,url="https://moure.dev"),
         User(id= 2,name="Santiago",surname="Lemus",age=14,url="https://mouredev.dev"),
         User(id= 3,name="Juan",surname= "Sanchez",age=14,url="https://moure.com")]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Daniel","Surname": "Saenz","url":"https://moure.dev"},
            {"name": "Santiago","Surname": "Lemus","url":"https://mouredev.dev"},
            {"name": "Juan","Surname": "Sanchez","url":"https://moure.com"}]

@router.get("/usersclass")
async def usersclass():
    return users_list
#Path
@router.get("/userclass/{id}")
async def users(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        raise HTTPException(status_code=404, detail="No se encontro el usuario")
    
@router.post("/user/", response_model= User ,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=304,detail="El usuario ya existe")
    else:
        users_list.append(user)

@router.put("/user/")
async def user(user: User):
    found = False
    for e,i in enumerate(users_list):
        if i.id == user.id:
            users_list[e] = user
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="No se encontro el usuario")


#Query
@router.get("/userclassquery/")
async def users(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        raise HTTPException(404)
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(404)
