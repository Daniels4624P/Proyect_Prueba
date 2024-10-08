from fastapi import APIRouter, HTTPException, status
from pydantic import *
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter()

# ENTIDAD USER

users_list = []

@router.get("/usersclassdb")
async def usersclass():
    return users_schema(db_client.users.find())

#Path
@router.get("/userclassdb/{id}")
async def users(id: str):
    try:
        return search_user("_id", ObjectId(id))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el usuario")
    
@router.post("/userdb/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    existing_user = search_user("email", user.email)
    
    if isinstance(existing_user, User):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")
    
    user_dict = user.dict()  # Convertimos el objeto Pydantic a dict
    del user_dict["id"]  # Eliminamos el campo "id" si es necesario
    
    id = db_client.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    
    return User(**new_user)

@router.put("/userdb/")
async def user(user: User):
    try:
        user_dict = dict(user)
        del user_dict["id"]
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)},user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return search_user("_id", ObjectId(user.id))
#Query
@router.delete("/userclassquerydb/")
async def users(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo eliminar el usuario")
    
def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}