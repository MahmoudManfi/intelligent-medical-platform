from sqlalchemy.orm import Session
from passlib.context import CryptContext
import doctorModel
import doctorSchema
from fastapi import HTTPException
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str):
    return db.query(doctorModel.Doctor).filter(doctorModel.Doctor.email == email).first()

def get_user_by_id(db: Session, id: str):
    return db.query(doctorModel.Doctor).filter(doctorModel.Doctor.id == id).first()

def create_doctor(db: Session, doctor: doctorSchema.DoctorCreate):
    try:
        db_doctor = doctorModel.Doctor(email=doctor.email, password=get_password_hash(doctor.password),displayName=doctor.displayName)
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except:
        raise HTTPException(
            status_code=500,
            detail="error",
        )

def authenticate_user( db: Session,email: str, password: str):
    user=get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def update_user(db:Session(),doctorUpdated,doctor):
    try:
        doctor.displayName=doctorUpdated.displayName
        doctor.email=doctorUpdated.email
        doctor.url=doctorUpdated.url
        doctor.firstName=doctorUpdated.firstName
        doctor.lastName=doctorUpdated.lastName
        doctor.phoneNumber=doctorUpdated.phoneNumber
        doctor.specializedIn=doctorUpdated.specializedIn
        doctor.specialty=doctorUpdated.specialty
        doctor.degree=doctorUpdated.degree
        doctor.country=doctorUpdated.country
        doctor.address=doctorUpdated.address
        doctor.contactNumber=doctorUpdated.contactNumber
        doctor.fees=doctorUpdated.fees
        doctor.url=doctorUpdated.url

        db.commit()
    except:
        raise HTTPException(
            status_code=500,
            detail="error",
        )
    print(doctor)
    return doctor

def get_patients_by_doctor_id(db:Session,id):
    doctor=get_user_by_id(db, id)
    print(doctor.patients)
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    if not doctor.patients:
        raise HTTPException(status_code=404, detail="patients not found")
    else:
        return doctor.patients
