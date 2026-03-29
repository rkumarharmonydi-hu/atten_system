from pydantic import BaseModel
from datetime import time, date
from typing import Optional
from datetime import datetime, date, time

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int
    role: str
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    # role: str 

class UserResponse(BaseModel):
    id: int
    username: str
    # role: str
    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    check_in_time: Optional[time] = None

class AttendanceResponse(BaseModel):
    date: date
    check_in_time: time
    check_out_time: Optional[time] = None
    status: str

    class Config:
        from_attributes = True

#For leave
class LeaveCreate(BaseModel):
    start_date:date
    end_date:date
    reason:str

# Request Body Model
class AttendanceUpdate(BaseModel):
    attendance_id: int 
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    status: Optional[str] = None

