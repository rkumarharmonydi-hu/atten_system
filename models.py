from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")
    access_token = Column(String, nullable=True)
    attendances = relationship(
        "Attendance",
        back_populates="user",
        cascade="all, delete"
    )

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )
    date = Column(Date)
    check_in_time = Column(Time)
    check_out_time = Column(Time, nullable=True)
    status = Column(String)
    user = relationship("User", back_populates="attendances")

class Leave(Base):
    __tablename__ = "leaves" 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(Date)
    end_date = Column(Date)   
    reason = Column(String)
    status = Column(String, default="Pending")
    user=relationship("User")    