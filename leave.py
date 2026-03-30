from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Leave  
from database import SessionLocal
from dependencies import get_current_user, require_role
from schemas import LeaveCreate

router = APIRouter(prefix="/leave", tags=["Leave"])

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# APPLY LEAVE
@router.post("/apply")
def apply_leave(
    data: LeaveCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    leave = Leave(   
        user_id=current_user.id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return {"msg": "Leave applied successfully",
            "leave_id": leave.id}


# MY LEAVES
@router.get("/my-leaves")
def my_leaves(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    leaves = db.query(Leave).filter(  
        Leave.user_id == current_user.id
    ).all()

    return leaves


# APPROVE LEAVE
@router.put("/approve/{leave_id}")
def approve_leave(
    leave_id: int,
    current_user=Depends(require_role(["TL", "hr"])),  # optional fix
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.status = "Approved"
    db.commit()

    return {"msg": "Leave approved"}


# REJECT LEAVE
@router.put("/reject/{leave_id}")
def reject_leave(
    leave_id: int,
    current_user=Depends(require_role(["TL", "hr"])),
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.status = "Rejected"
    db.commit()

    return {"msg": "Leave rejected"}


# ALL LEAVES
@router.get("/all")
def all_leaves(
    current_user=Depends(require_role(["TL", "hr"])),
    db: Session = Depends(get_db)
):
    leaves = db.query(Leave).all()
    result = []
    for leave in leaves:
        result.append({
            "id": leave.id,
            "user_name": leave.user.username,   
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "status": leave.status
        })
    return result