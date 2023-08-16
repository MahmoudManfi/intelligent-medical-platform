from sqlalchemy.orm import Session
import server.patientModel
import server.patientMedicalDataModel
from . import patientMedicalDataSchema
from fastapi import HTTPException

def create_patient_Medical_Data(db:Session,patient_id:int ,patientMedicalData:patientMedicalDataSchema.PatientMedicalDataBase):
    try:
        
        db_patient_medical_data=server.patientMedicalDataModel.PatientMedicalData(
            Course = patientMedicalData.Course,
    DecreaseBy = patientMedicalData.DecreaseBy,
    Duration = patientMedicalData.Duration,
    IncreaseBy = patientMedicalData.IncreaseBy,
    comments = patientMedicalData.comments,
    diagnosis = patientMedicalData.diagnosis,
    onSet = patientMedicalData.onSet,
    symptoms = patientMedicalData.symptoms,
    prescription = patientMedicalData.prescription,
    patient_id = patient_id
        )
        db.add(db_patient_medical_data)
        db.commit()
        db.refresh(db_patient_medical_data)
        return db_patient_medical_data

    except:
        raise HTTPException(
            status_code=500,
            detail="error",
        )

def get_patient_Medical_Data_by_id(db: Session, id: str):
    return db.query(server.patientMedicalDataModel.PatientMedicalData).filter(server.patientMedicalDataModel.PatientMedicalData.id == id).first()

def update_patient_Medical_Data(db:Session,patientMedicalDataModelUpdated,patientMedicalDataModel):
    try:
        patientMedicalDataModel.Course=patientMedicalDataModelUpdated.Course
        patientMedicalDataModel.DecreaseBy=patientMedicalDataModelUpdated.DecreaseBy
        patientMedicalDataModel.Duration=patientMedicalDataModelUpdated.Duration
        patientMedicalDataModel.IncreaseBy=patientMedicalDataModelUpdated.IncreaseBy
        patientMedicalDataModel.comments=patientMedicalDataModelUpdated.comments
        patientMedicalDataModel.diagnosis=patientMedicalDataModelUpdated.diagnosis
        patientMedicalDataModel.onSet=patientMedicalDataModelUpdated.onSet
        patientMedicalDataModel.symptoms=patientMedicalDataModelUpdated.symptoms
        patientMedicalDataModel.prescription=patientMedicalDataModelUpdated.prescription
        db.commit() 
    except:
        raise HTTPException(
            status_code=500,
            detail="error",
        )
    print(patientMedicalDataModel)
    return patientMedicalDataModel

def delete_patient_Medical_Data(db:Session,patient_Medical_Data_id,patient_id,token):
        patient_Medical_Data = db.get(server.patientMedicalDataModel.PatientMedicalData, patient_Medical_Data_id)
        if not patient_Medical_Data:
            raise HTTPException(status_code=404, detail="patient_Medical_Data not found")
        if patient_Medical_Data.patient_id==patient_id or patient_Medical_Data.patientdata.doctor_id!=token.id:
            raise HTTPException(status_code=404, detail="patient_Medical_Data not found 1")
        
        db.delete(patient_Medical_Data)
        db.commit()
        return {"message":"patient medical data deleted"}

