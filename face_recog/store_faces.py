# import cv2
# import face_recognition
# import os

# from dotenv import load_dotenv
# from pymongo import MongoClient

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# client = MongoClient(MONGO_URI)
# db = client['face_recognition_db']
# collection = db['face_encodings']

# def store_face(name, student_id, img):
#     image = face_recognition.load_image_file(img)
#     encoding = face_recognition.face_encodings(image)[0]

#     face_data = {
#         "name": name,
#         "student_id": student_id,
#         "face_encodings": encoding[0].tolist()
#     }
#     collection.insert_one(face_data)
#     print(f"stored data for {name}")


# try:
#     client.admin.command('ping')
#     print("MongoDB connection successful.")
# except Exception as e:
#     print("Error connecting to MongoDB:", e)
    
# store_face("riley", 24460450, "images/head.jpg")
# store_face("alex", 2994850, "images/alex.jpg")
# store_face("eshaan", 999999, "images/enair.jpg")
# store_face("dip", 39485334, "images/dip.jpg")