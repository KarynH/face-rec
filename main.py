from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import collection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:3000"] for local React app, or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class FaceEncoding(BaseModel):
    student_id: str
    face_encoding: List[float]
    
@app.post("/store-face")
async def store_face_data(data: FaceEncoding):
      # Insert the encoding data into MongoDB
    collection.insert_one(data.dict())
    return {"message": "Face encoding stored successfully."}

@app.get("/get-face/{student_id}")
async def get_face_data(student_id: str):
    # Fetch the encoding by student ID
    face_data = collection.find_one({"student_id": student_id})
    if face_data:
        return {"student_id": face_data["student_id"], "face_encoding": face_data["face_encoding"]}
    raise HTTPException(status_code=404, detail="Face data not found")

'''
run server locally:
uvicorn main:app --reload

link:
#http://localhost:8000/docs
'''
