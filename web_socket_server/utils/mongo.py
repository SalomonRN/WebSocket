from typing import Union, Any
import pymongo
from pymongo.results import	InsertOneResult
import pymongo.database
import pymongo.errors
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys
from os import getenv

import pymongo.synchronous
import pymongo.synchronous.mongo_client
from dotenv import load_dotenv
 
load_dotenv()
URI = getenv("URI_MONGO")
CLIENT: pymongo.synchronous.mongo_client.MongoClient = None
DATABASE: pymongo.database.Database = None

def init_connection():
    global CLIENT, DATABASE
    try:
        if not URI:
            raise Exception("No hay URI para Mongo")
        CLIENT = MongoClient(URI, server_api=ServerApi("1"))
        CLIENT.admin.command("ping")
        DATABASE = CLIENT.get_database("chat_web")
        print("CONEXION CON LA BD")
    except Exception as e:
        print("ERROR", e)
        sys.exit()

def get_all(database, collection):
    database = CLIENT.get_database(database)
    collection = database.get_collection(collection)
    cursor = collection.find({})
    for element in cursor:
        print(element)

def create_user(querry: dict) -> Union[InsertOneResult, dict]:
    try:
        return DATABASE.get_collection("users").insert_one(querry)
    except pymongo.errors.DuplicateKeyError as e:
        return e.details

def get_user(username: str) -> dict:
    return DATABASE.get_collection("users").find_one({"username": username})  

def update_user(username: str, update_querry: dict) -> dict:
    return DATABASE.get_collection("users").find_one_and_update(
        {"username": username}, update_querry, 
        return_document=pymongo.ReturnDocument.AFTER)

def delete_user(id: int):
    return DATABASE.get_collection("servers").find_one_and_delete({"id": id})

def create_index():
    DATABASE.get_collection("users") \
    .create_indexes([pymongo.IndexModel("username", unique=True), pymongo.IndexModel("email", unique=True)])

if __name__ == "__main__":
    init_connection() 
    a = create_user({
        "username": "usernamea",
        "password": "password",
        "email": "sasalos@salo.com"
    })
    print(a)
    print(type(a))
    CLIENT.close()
