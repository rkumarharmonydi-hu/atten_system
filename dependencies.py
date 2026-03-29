from jose import jwt, JWTError,ExpiredSignatureError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import SECRET_KEY, ALGORITHM
from models import User
from database import SessionLocal
from sqlalchemy.orm import Session
 
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):    
    token = credentials.credentials
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  
        role=payload.get("role") 
        if user_id is None: 
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_role(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied: insufficient permissions"
            )
        return current_user
    return role_checker


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db)
# ):
#     token = credentials.credentials

#     try:
#         # Decode JWT token
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         user_id = payload.get("sub")

#         # Token payload missing
#         if user_id is None:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Token payload missing user id"
#             )

#         # Convert user_id to integer
#         try:
#             user_id = int(user_id)
#         except ValueError:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Invalid user id format in token"
#             )

#         # Check if user exists in DB
#         user = db.query(User).filter(User.id == user_id).first()

#         if user is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail="User associated with this token does not exist"
#             )

#         return user

#     # Token expired
#     except ExpiredSignatureError:
#         raise HTTPException(
#             status_code=401,
#             detail="Token expired. Please login again."
#         )

#     # Invalid token / signature
#     except JWTError:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid authentication token"
#         )

#     # # Unexpected error
#     # except Exception as e:
#     #     raise HTTPException(
#     #         status_code=500,
#     #         detail=f"Authentication error: {str(e)}"
#     #     )