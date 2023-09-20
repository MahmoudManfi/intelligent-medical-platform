from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    displayName = Column(String)
    firstName = Column(String,nullable=True)
    lastName = Column(String,nullable=True)
    phoneNumber = Column(String,nullable=True)
    specializedIn = Column(String,nullable=True)
    specialty = Column(String,nullable=True)
    degree = Column(String,nullable=True)
    country = Column(String,nullable=True)
    url = Column(String,nullable=True)
    address = Column(String,nullable=True)
    contactNumber = Column(String,nullable=True)
    fees = Column(String,nullable=True)

    patients = relationship("Patient", back_populates="doctor")
