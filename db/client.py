from pymongo import MongoClient

#Base de datos local
#db_client = MongoClient() #por defecto MongoClient se conecta a la base de datos en local

URL_CONNECT = "mongodb+srv://user:Gravityfalls@proyect.hcvxo.mongodb.net/?retryWrites=true&w=majority&appName=Proyect"

#Base de datos remota
db_client = MongoClient(URL_CONNECT).test