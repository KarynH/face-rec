#uvicorn is an ASGI web server implementation for python
#fast api is a framework used to build apis with python

import cv2
import face_recognition

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


def store_face(name, student_id, img):
    image = face_recognition.load_image_file(img)
    encoding = face_recognition.face_encodings(image)[0]

    face_data = {
        "name": name,
        "student_id": student_id,
        "face_encodings": encoding[0].tolist()
    }
    collection.insert_one(face_data)
    print(f"stored data for {name}")


#python database.py
if __name__ == "__main__":
    store_face("riley", 24460450, "images/head.jpg")
    store_face("alex", 2994850, "images/alex.jpg")
    store_face("eshaan", 999999, "images/enair.jpg")
    store_face("dip", 39485334, "images/dip.jpg")
    # This will print None if the connection fails or is misconfigured
    print(f"Mongo URI: {MONGO_URI}")
    print("Collections in database:", db.list_collection_names())