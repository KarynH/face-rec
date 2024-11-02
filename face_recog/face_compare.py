from pymongo import MongoClient
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import face_recognition
import cv2
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['face_recognition_db']
collection = db['face_encodings']

def find_best_match(current_encoding, threshold = .6):
    all_faces = collection.find()

    best_match = "unknown"
    highest_similarity = 0

    for face in all_faces:
        stored_embedding = np.array(face['embedding'])
        similarity = cosine_similarity([current_encoding], [stored_embedding])[0][0]

        if similarity > highest_similarity and similarity >= threshold:
            highest_similarity = similarity
            best_match = face['name']

        return best_match




def face_recog():
    video_capture = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video_capture.read()
        
        #detect and encode
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_encodings)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            match = find_best_match(face_encoding)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            if match:
                label = match
            else:
                label = "unknown"
            cv2.putText(frame, label, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 1)

        #display
        cv2.imshow('video', frame)

        #break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #close
    video_capture.release()
    cv2.destroyAllWindows()

face_recog()
