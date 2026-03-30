from fastapi import APIRouter, Depends
from datetime import datetime, date, time
from models import Attendance, User
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dependencies import get_current_user
from dependencies import require_role
from sqlalchemy import extract 
from pydantic import BaseModel
from typing import Optional
from schemas import AttendanceUpdate

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_status(check_time):
    if check_time < time(9, 15):
        return "Present"
    elif check_time < time(11, 0):
        return "Late"
    elif check_time < time(14, 0):
        return "Half Day"
    else:
        return "Absent"
    
def parse_time(time_str):
    time_str = time_str.strip()
    formats = [
        "%H:%M:%S",        
        "%I:%M:%S %p",     
        "%H:%M",           
        "%I:%M %p"         
    ]
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue

    raise ValueError(f"Invalid time format: {time_str}")
    
def check_in(user_id: int, db: Session = Depends(get_db)):
    today = date.today()

    exists = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.date == today
    ).first()

    if exists:
        return {"msg": "Already checked in"}
    now = datetime.now().time()
    status = get_status(now)
    record = Attendance(
        user_id=user_id,
        date=today,
        check_in_time=now,
        status=status
    )
    db.add(record)
    db.commit()
    return {"status": status}


@router.post("/check-in/{user_id}")
def check_in(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    #Security check
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Token does not belong to this user"
        )
    today = date.today()
    exists = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.date == today
    ).first()

    if exists:
        return {"msg": "Already checked in"}

    now = datetime.now().time()
    status = get_status(now)

    record = Attendance(
        user_id=user_id,
        date=today,
        check_in_time=now,
        status=status
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "msg": "Checked in successfully",
        "check_in_time": now.strftime("%I:%M:%S %p"),
        "status": status
    }

@router.get("/secure-data")
def secure_data(current_user: User = Depends(get_current_user)):
    return {
        "msg": f"Welcome {current_user.username}"
    }

@router.post("/check-out")
def check_out(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    today = date.today()
    record = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        Attendance.date == today
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="No check-in found for today")
    if record.check_out_time:
        return {"msg": "Already checked out"}
    # set checkout time
    record.check_out_time = datetime.now().time()
    # calculate working hours
    check_in_datetime = datetime.combine(today, record.check_in_time)
    check_out_datetime = datetime.combine(today, record.check_out_time)
    working_hours = check_out_datetime - check_in_datetime
    db.commit()    
    db.refresh(record)
    return {
        "msg": "Checked out successfully",
        "check_in_time": record.check_in_time.strftime("%I:%M:%S %p"),
        "check_out_time": record.check_out_time.strftime("%I:%M:%S %p"),
        "working_hours": str(working_hours),
        "msg1":"Thank you"   
    }

@router.get("/my-attendance")
def my_attendance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).filter(
        Attendance.user_id == current_user.id
    ).all()
    return [ 
        {
            "id": r.id,
            "date": r.date.isoformat(),
            "check_in_time": r.check_in_time.strftime("%I:%M:%S %p") 
            if r.check_in_time else None,
            "check_out_time": r.check_out_time.strftime("%I:%M:%S %p") 
            if r.check_out_time else None,
            "status": r.status
        }
        for r in records
    ]

@router.get("/all-attendance")
def all_attendance(
    current_user: User = Depends(require_role(["admin", "hr"])),
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).all() 
    return [
        {
            "user_id": r.user_id,
            "date": r.date.isoformat(),
            "check_in": r.check_in_time.strftime("%I:%M %p") if r.check_in_time else None,
            "check_out": r.check_out_time.strftime("%I:%M %p") if r.check_out_time else None,
            "status": r.status
        }
        for r in records
    ]

# # Request Body Model
# class AttendanceUpdate(BaseModel):
#     attendance_id: int 
#     check_in_time: Optional[datetime] = None
#     check_out_time: Optional[datetime] = None
#     status: Optional[str] = None

@router.put("/update-attendance")
def update_attendance(
    data: AttendanceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    #  Admin check
    if current_user.role != ["admin","hr"]:
        raise HTTPException(
            status_code=403,
            detail="Only admin can update attendance"
        )

    # Find record
    record = db.query(Attendance).filter(
        Attendance.id == data.attendance_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )
    # Update fields
    if data.check_in_time:
        record.check_in_time = data.check_in_time

    if data.check_out_time:
        record.check_out_time = data.check_out_time

    if data.status:
        record.status = data.status
    db.commit()
    db.refresh(record)
    return {
        "msg": "Attendance updated successfully",
        "attendance_id": record.id
    }

@router.get("/report/monthly")
def monthly_report(
    user_id: int,   #  NEW PARAM
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ROLE CHECK
    if current_user.role not in ["admin", "hr"]:
        raise HTTPException(
            status_code=403,
            detail="Only HR and admin can access monthly report"
        )

    today = date.today()
    current_month = today.month
    current_year = today.year

    # FILTER BY GIVEN USER_ID
    records = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        extract('month', Attendance.date) == current_month,
        extract('year', Attendance.date) == current_year
    ).all()

    total_present = sum(1 for r in records if r.status == "Present")
    total_absent = sum(1 for r in records if r.status == "Absent")
    late_days = sum(1 for r in records if r.status == "Late")

    return {
        "requested_by": current_user.id,
        "user_id": user_id,
        "month": current_month,
        "year": current_year,
        "total_present": total_present,
        "total_absent": total_absent,
        "late_days": late_days
    }