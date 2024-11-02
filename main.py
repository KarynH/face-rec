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

@app.get("/get-face")
async def get_all_faces():
    try:
        faces = list(collection.find({}, {"_id": 0}))  # Exclude _id for JSON serialization
        all_faces = [
            {
                "student_name": face.get("student_name", "Unknown"), 
                "face_encoding": face.get("face_encoding", [])
            }
            for face in faces
        ]
        
        if all_faces:
            return all_faces
        else:
            raise HTTPException(status_code=404, detail="No face data found.")
    
    except PyMongoError as e:
        print(f"Error fetching face data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching face data from the database.")

'''
run server locally:
uvicorn main:app --reload

link:
#http://localhost:8000/docs
'''
