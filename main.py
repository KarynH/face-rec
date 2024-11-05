from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import collection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import cv2
import face_recognition
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

class FaceEncoding(BaseModel):
    student_name: str
    student_id: str
    face_encoding: List[float]
    
@app.post("/store-face")
async def store_face_data(data: FaceEncoding):
      # Insert the encoding data into MongoDB
    collection.insert_one(data.dict())
    return {"message": "Face encoding stored successfully."}

@app.get("/get-face")
async def get_all_faces():
    faces = collection.find()
    all_faces = [{"student_name": face["student_name"], "face_encoding": face["face_encoding"]} for face in faces]
    
    if all_faces:
        return all_faces
    else:
        raise HTTPException(status_code=404, detail="No face data found.")
'''
run server locally:
uvicorn main:app --reload

link:
#http://localhost:8000/docs
'''

def store_face(name, student_id, img):
    image = face_recognition.load_image_file(img)
    encoding = face_recognition.face_encodings(image)[0]

    face_data = {
        "student_name": name,
        "student_id": str(student_id),
        "face_encoding": encoding.tolist()
    }

    response = requests.post("https://ai-innovation-challenge-8fc8a252d8c5.herokuapp.com/store-face", json=face_data)
    if response.status_code == 200:
            print(f"Successfully stored data for {name}")
    else:
        print(f"Failed to store data for {name}: {response.json()}")

def face_recog():
    video_capture = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video_capture.read()
        
        #detect and encode
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

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

def find_best_match(current_encoding, threshold = .8):
    print(current_encoding)
    response = requests.get("https://ai-innovation-challenge-8fc8a252d8c5.herokuapp.com/get-face")
    if response.status_code != 200:
        print("Error fetching face data:", response.json())
        return ""
    
    all_faces = response.json()  # Parse JSON response

    best_match = "unknown"
    highest_similarity = 0

    for face in all_faces:
        stored_embedding = np.array(face['face_encoding'])
        similarity = cosine_similarity([current_encoding], [stored_embedding])[0][0]

        if similarity > highest_similarity and similarity >= threshold:
            highest_similarity = similarity
            best_match = face['student_name']

    if highest_similarity < threshold:
        return "unknown"
    
    return best_match


def main():
    # store_face("riley", 24460450, "images/head.jpg")
    # store_face("eshaan", 2889034, "images/enair.jpg")
    # store_face("alex", 28943, "images/alex.jpg")
    # store_face("dip", 55583893, "images/dip.jpg")
    # store_face("sam", 24243834, "images/sam.jpg")
    # store_face("alan", 24517782, "images/alan.jpg")
    # store_face("karyn", 24242778, "images/karyn.jpg")

    face_recog()

if __name__ == "__main__":
    main()
    # This will print None if the connection fails or is misconfigured