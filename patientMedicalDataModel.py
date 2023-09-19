from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
class PatientMedicalData(Base):
    __tablename__ = "patientsMedicalData"

    id = Column(Integer, primary_key=True, index=True)
    Course = Column(String)
    DecreaseBy = Column(String)
    Duration = Column(String)
    IncreaseBy = Column(String)
    comments = Column(String)
    diagnosis = Column(String)
    onSet = Column(String)
    symptoms = Column(String)
    prescription = Column(String)
    patient_id = Column(Integer, ForeignKey("patients.id"))

    patientdata = relationship("Patient", back_populates="patientMedicalData")
