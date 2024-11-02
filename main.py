from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import collection

app = FastAPI()

class FaceEncoding(BaseModel):
    student_name: str
    student_id: int
    face_encoding: List[float]
    
@app.post("/store-face")
async def store_face_data(data: FaceEncoding):
      # Insert the encoding data into MongoDB
    collection.insert_one(data.dict())
    return {"message": "Face encoding stored successfully."}

'''
async def get_all_faces():
    faces = collection.find()
    all_faces = [{"student_name": face["student_name"], "face_encoding": face["face_encoding"]} for face in faces]
   
    if all_faces:
        return all_faces
    else:
        raise HTTPException(status_code=404, detail="No face data found.")


'''

@app.get("/get-face/")
async def get_face_data():
    # Fetch the encoding by student ID
    face_data = collection.find([{"student_name": face["student_name"], "face_encoding": face["face_encoding"]} for face in faces])
    if face_data:
        return face_data
    else:
        raise HTTPException(status_code=404, detail="No face data found.")

'''
run server locally:
uvicorn main:app --reload

link:
#http://localhost:8000/docs
'''
