from sqlalchemy.orm import Session
import patientModel
import patientSchema
import doctorSchema
from fastapi import HTTPException

def get_user_by_fullName(db: Session, fullName: str,token:int):
    return db.query(patientModel.Patient).filter(patientModel.Patient.fullName == fullName,patientModel.Patient.doctor_id==token).first()

def create_patient(db: Session,patient: patientSchema.PatientBase,token:doctorSchema.Token):
    try:
        db_patient=patientModel.Patient(fullName=patient.fullName,age=patient.age,gender=patient.gender,mariedStatus=patient.mariedStatus,
        offspring=patient.offspring,phoneNumber=patient.phoneNumber,relation=patient.relation,emergencyFullName=patient.emergencyFullName,
        emergencyPhoneNumber=patient.emergencyPhoneNumber,address=patient.address,
        allergic=patient.allergic,familialDiseases=patient.familialDiseases,patientGeneralMedicalHistory=patient.patientGeneralMedicalHistory,
        smokeAlcohol=patient.smokeAlcohol,surgical=patient.surgical,women=patient.women,doctor_id=token.id)
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="error",
        )

def get_patient_by_id(db: Session, id: str):
    return db.query(patientModel.Patient).filter(patientModel.Patient.id == id).first()

def update_patient(db:Session,patientUpdated,patient):
    try:
        patient.fullName=patientUpdated.fullName
        patient.age=patientUpdated.age
        patient.gender=patientUpdated.gender
        patient.mariedStatus=patientUpdated.mariedStatus
        patient.offspring=patientUpdated.offspring
        patient.phoneNumber=patientUpdated.phoneNumber
        patient.relation=patientUpdated.relation
        patient.emergencyFullName=patientUpdated.emergencyFullName
        patient.emergencyPhoneNumber=patientUpdated.emergencyPhoneNumber
        patient.address=patientUpdated.address
        patient.allergic=patientUpdated.allergic
        patient.familialDiseases=patientUpdated.familialDiseases
        patient.patientGeneralMedicalHistory=patientUpdated.patientGeneralMedicalHistory
        patient.smokeAlcohol=patientUpdated.smokeAlcohol
        patient.surgical=patientUpdated.surgical
        patient.women=patientUpdated.women

        db.commit()
    except:
        raise HTTPException(
            status_code=500,
            detail="error",
        )
    print(patient)
    return patient

def delete_patient(db:Session,patient_id,token):
    patient = db.get(patientModel.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")
    print(patient.doctor_id,token.id)
    if patient.doctor_id!=token.id:
        raise HTTPException(status_code=404, detail="patient not found")
    db.delete(patient)
    db.commit()
    return {"message":"patient deleted"}

def get_medical_data_of_patient(db:Session,patient_id,token):
    patient = db.get(patientModel.Patient, patient_id)
    if not patient:

        raise HTTPException(status_code=404, detail="patient not found")
    if patient.doctor_id!=token:
        raise HTTPException(status_code=404, detail="patient not found")
    return patient.patientMedicalData




