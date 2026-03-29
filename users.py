from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from schemas import UserCreate, UserLogin
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing_user=db.query(User).filter(User.username==data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )     
    user = User(
        username=data.username.strip(),
        password=hash_password(data.password.strip()),
        # role=data.role 
    )
    db.add(user)
    db.commit()
    db.refresh(user)   
    return {
        "msg": "User registered successfully",
        "user_id": user.id,
        "username": user.username
    }

# @router.post("/login")
# def login(data: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == data.username).first()
#     if not user or not verify_password(data.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid username or password")
#     token = create_access_token(user.id, user.role)
#     return {
#         "msg": "Login successful",
#         "access_token": token,
#         "token_type": "bearer"
#     }  

# @router.post("/login")
# def login(data: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == data.username).first()

#     if not user or not verify_password(data.password, user.password):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )

#     token = create_access_token({"sub":user.id})  

#     return {
#         "msg": "Login successful",
#         "access_token": token,
#         "token_type": "bearer"
#     }

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    token = create_access_token(user.id, user.role)
    return {
        "msg": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }    