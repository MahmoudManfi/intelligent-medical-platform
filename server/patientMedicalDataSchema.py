from pydantic import BaseModel
from typing import Optional,Union
#import server.patientModel
class PatientMedicalDataBase(BaseModel):
    Course : str
    DecreaseBy : str
    Duration : str
    IncreaseBy : str
    comments : str
    diagnosis : str
    onSet : str
    symptoms : str
    prescription : str

class PatientMedicalDataCreate(PatientMedicalDataBase):
    patient_id: int

class PatientMedicalData(PatientMedicalDataBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True

