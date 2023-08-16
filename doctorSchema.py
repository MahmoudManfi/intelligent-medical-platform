from pydantic import BaseModel
from typing import Optional,Union,List
import patientSchema
class Token(BaseModel):
    token: str
    token_type:str
class TokenData(BaseModel):
    displayName: Union[str, None] = None
    id: Union[int, None] = None,
    type: Union[str, None] = None

class PersonalInfo(BaseModel):
    firstName: Optional[str]=None
    lastName: Optional[str]=None
    phoneNumber: Optional[str]=None
    specializedIn: Optional[str]=None
    specialty: Optional[str]=None
    degree: Optional[str]=None
    country: Optional[str]=None
class DoctorBase(BaseModel):
    email:  str
    displayName: str
    firstName: Optional[str]=None
    lastName: Optional[str]=None
    phoneNumber: Optional[str]=None
    specializedIn: Optional[str]=None
    specialty: Optional[str]=None
    degree: Optional[str]=None
    country: Optional[str]=None
    address: Optional[str]=None
    contactNumber: Optional[str]=None
    fees: Optional[str]=None
    url: Optional[str]=None
class DoctorCreate(DoctorBase):
    password: str

class Doctor(DoctorBase):
    id: int
    class Config:
        orm_mode = True


class DoctorPatients(DoctorBase):
    id: int
    patients: List[patientSchema.Patient] = []

    class Config:
        orm_mode = True