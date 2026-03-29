from fastapi import FastAPI
from database import Base, engine
from models import User, Attendance
from users import router as user_router
from attendance import router as attendance_router
from fastapi.middleware.cors import CORSMiddleware
from leave import router as leave_router

Base.metadata.create_all(bind=engine)
app = FastAPI( title="Attendance Management System",
    description="""
A role-based Attendance Management System built using FastAPI and PostgreSQL. 
This system manages user registration, authentication, and daily attendance tracking.
""")
app.include_router(attendance_router)
app.include_router(user_router)
app.include_router(leave_router)

@app.get("/")
def root():
    return {"msg": "Attendance system running"}
  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  

from fastapi.staticfiles import StaticFiles
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
