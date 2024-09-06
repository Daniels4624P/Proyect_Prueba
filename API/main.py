from fastapi import FastAPI
from routers import products,users,jwt_auth_users,basic_auth_user,users_db
from fastapi.staticfiles import StaticFiles
app = FastAPI()

#Routers

app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
#app.include_router(basic_auth_user.router)
app.mount("/static", StaticFiles(directory="static"),name="static")
app.include_router(users_db.router)

@app.get("/")#estara en la raiz
#Asincronia o async es un pocreso asincrono que es un proceso que no tiene la necesidad de esperar a que termine otro proceso para iniciar esto nos ayuda a mejorar algunos recursos y tambien para que nuestras funciones sean independientes
async def root():
    return "Hola FastApi"

@app.get("/url")
async def url():
    return { "url_curso":"https://mouredev.com/python" }

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc