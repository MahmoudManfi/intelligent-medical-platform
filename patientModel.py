from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,JSON
from sqlalchemy.orm import relationship

from database import Base
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String)
    age = Column(Integer)
    gender = Column(String)
    mariedStatus = Column(String)
    offspring = Column(Integer)
    phoneNumber = Column(String)
    relation = Column(String,nullable=True)
    emergncyFullName = Column(String,nullable=True)
    emergncyPhoneNumber= Column(String,nullable=True)
    address = Column(String)
    allergic=Column(JSON,nullable=True)
    familialDiseases=Column(JSON,nullable=True)
    patientGeneralMedicalHistory=Column(JSON,nullable=True)
    smokeAlcohol=Column(JSON,nullable=True)
    surgical=Column(JSON,nullable=True)
    women=Column(JSON,nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    patientMedicalData  = relationship("PatientMedicalData", back_populates="patientdata")
    doctor = relationship("Doctor", back_populates="patients")
