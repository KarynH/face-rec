#uvicorn is an ASGI web server implementation for python
#fast api is a framework used to build apis with python

# os built-in python module to access environment var mongo_uri
import os
from pymongo import MongoClient
from dotenv import load_dotenv

#loads environment vars from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") #fetches the mongodb uri from env var
client = MongoClient(MONGO_URI) #connects to the mongo db wit uri
db = client["face_recognition_db"]
collection = db["face_encodings"]

#python database.py
if __name__ == "__main__":
    # This will print None if the connection fails or is misconfigured
    print(f"Mongo URI: {MONGO_URI}")
    print("Collections in database:", db.list_collection_names())