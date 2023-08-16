from pydantic import BaseModel
from typing import Optional,Union,List
import server.patientMedicalDataSchema
class PatientBase(BaseModel):
    fullName: str
    age: str
    gender: str
    phoneNumber: str
    mariedStatus: str
    offspring: str
    phoneNumber: str
    relation: Optional[str]=None
    emergncyFullName: Optional[str]=None
    emergncyPhoneNumber: Optional[str]=None
    address: str
    allergic:Optional[dict]=None
    familialDiseases: Optional[dict]=None
    patientGeneralMedicalHistory: Optional[dict]=None
    smokeAlcohol: Optional[dict]=None
    surgical: Optional[dict]=None
    women: Optional[dict]=None

class PatientCreate(PatientBase):
    doctor_id: int

class Patient(PatientBase):
    id: int
    doctor_id: int

    class Config:
        orm_mode = True

class PatientPatientMedicalData(PatientBase):
    id: int
    patientsMedicalData: List[server.patientMedicalDataSchema.PatientMedicalData] = []

    class Config:
        orm_mode = True

