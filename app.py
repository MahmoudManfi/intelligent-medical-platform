from fastapi import FastAPI, UploadFile, Form, File, Depends,HTTPException,status
import os
import re
from datetime import timedelta
import random, string
from fastapi.responses import JSONResponse,FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwtTokens
import doctorCRUD
import doctorModel
import doctorSchema
import patientCRUD
import PatientMedicalDataCRUD
import patientSchema
import patientMedicalDataSchema
from typing import Annotated
from database import SessionLocal, engine
from cancers.cancer import BaseCancer

doctorModel.Base.metadata.create_all(bind=engine)
# token:server.doctorSchema.Token=Depends(server.jwtTokens.decode_access_token)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# lungCancer = LungCancer()
# cervicalCancer = CervicalCancer()
# brainCancer = BrainCancer()

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/doctors/login')
app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def predict():
    return "Hello World From Reserve Officers College!!"

@app.post("/doctors", response_model=doctorSchema.Doctor)
async def create_doctor(doctor: doctorSchema.DoctorCreate, db: Session = Depends(get_db)):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    db_user = doctorCRUD.get_user_by_email(db, email=doctor.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if((not doctor.email or doctor.email.isspace())or (not doctor.password or doctor.password.isspace())or(not doctor.displayName or doctor.displayName.isspace())):
        raise HTTPException(status_code=400, detail="Empty Fields")
    doctor.email=doctor.email.rstrip()
    doctor.password=doctor.password.rstrip()
    doctor.displayName=doctor.displayName.rstrip()

    if(len(doctor.password)<8 or  not re.fullmatch(regex, doctor.email)):
        raise HTTPException(status_code=400, detail="password less than 8 or not email address")

    return doctorCRUD.create_doctor(db=db, doctor=doctor)

@app.get("/doctors/tokencheck")
async def tokenchecker(token:doctorSchema.Token=Depends(jwtTokens.decode_access_token)):
    return {"message":"ok"}

@app.post("/doctors/login",response_model=doctorSchema.Token)
async def login(doctor: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(doctor.username)
    print(doctor.password)
    doctor=doctorCRUD.authenticate_user(db, doctor.username, doctor.password)

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=jwtTokens.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwtTokens.create_access_token(
        data={"sub": str(doctor.id),"displayName":doctor.displayName,"type":"doctor"}, expires_delta=access_token_expires
    )
    return {"token": access_token,"token_type":"bearer"}

@app.get("/doctors/profile",response_model=doctorSchema.Doctor)
async def getProfile(token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    doctor=doctorCRUD.get_user_by_id(db, token.id)
    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )
    return doctor

@app.put("/doctors/profile",response_model=doctorSchema.Doctor)
async def getProfile(doctorUpdated:doctorSchema.DoctorBase,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    doctor=doctorCRUD.get_user_by_id(db, token.id)
    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )
    doctor=doctorCRUD.update_user(db, doctorUpdated, doctor)
    return doctor

@app.post("/doctors/profile/picture")
async def upload_file(file: UploadFile = File(...),token:doctorSchema.Token=Depends(jwtTokens.decode_access_token)):
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if (file.filename):
        letters = string.ascii_lowercase
        filename = ''.join(random.choice(letters) for i in range(12))+os.path.splitext(file.filename)[1]
        #os.path.join(os.path.abspath(os.path.dirname(__file__)),UPLOAD_FOLDER,filename)
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),UPLOAD_FOLDER,filename),'wb') as img:
            content = await file.read()
            img.write(content)
            img.close()
    return  JSONResponse(content={"url":filename},
status_code=200)

@app.delete("/doctors/logout")
async def logout(token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    return {"message":"logout success"}

@app.post("/doctors/patients",response_model=patientSchema.Patient)
async def add_new_patient(patient:patientSchema.PatientBase,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    print(patient)
    db_patient = patientCRUD.get_user_by_fullName(db, fullName=patient.fullName,token=token.id)
    print(db_patient)
    if db_patient :
        raise HTTPException(status_code=400, detail="FullName already registered")
    return patientCRUD.create_patient(db=db, patient=patient,token=token)

@app.put("/doctors/patients/{patient_id}",response_model=patientSchema.Patient)
async def update_patient(patient_id,patientUpdated:patientSchema.PatientBase,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    patient=patientCRUD.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="patient not found",
        )
    if patient.doctor_id != token.id:
        raise HTTPException(status_code=404,detail="patient not found")
    patient=patientCRUD.update_patient(db, patientUpdated, patient)
    return patient

@app.get("/doctors/patients/getallpatients")
async def getallpatients(token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    print("aaaaaa")
    return doctorCRUD.get_patients_by_doctor_id(db, token.id)
@app.get("/doctors/patients/{patient_id}")
async def get_patient(patient_id,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    patient=patientCRUD.get_patient_by_id(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="patient not found",
        )
    print(patient.doctor_id)
    print(token.id)
    print(patient.doctor_id == token.id)
    if patient.doctor_id != token.id:
        raise HTTPException(
            status_code=404,
            detail="patient not found",
        )
    return patient

@app.delete("/doctors/patients/{patient_id}")
async def delete_patient(patient_id,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    return patientCRUD.delete_patient(db, patient_id, token)

@app.post("/doctors/patients/{patient_id}/medicaldata",response_model=patientMedicalDataSchema.PatientMedicalData)
async def addmedicaldata(patientMedicalData:patientMedicalDataSchema.PatientMedicalDataBase,patient_id,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    patient=patientCRUD.get_patient_by_id(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="patient not found",
        )
    if patient.doctor_id != token.id:
        raise HTTPException(
            status_code=404,
            detail="patient not found",
        )
    patientMedicalData=PatientMedicalDataCRUD.create_patient_Medical_Data(db, patient_id, patientMedicalData)
    return patientMedicalData

@app.get("doctors/patients/{patient_id}/medicaldata/getallmedicaldata")
async def getallmedicaldataofpatient(patient_id,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    return patientCRUD.get_medical_data_of_patient(db, patient_id,token.id)

@app.get("/doctors/patients/{patient_id}/medicaldata/{medicaldata_id}")
async def getmedicaldata(patient_id,medicaldata_id,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    if(medicaldata_id =="getallmedicaldata"):
        return patientCRUD.get_medical_data_of_patient(db, patient_id,token.id)
    medicaldata=PatientMedicalDataCRUD.get_patient_Medical_Data_by_id(db, medicaldata_id)
    if not medicaldata:
            raise HTTPException(
            status_code=404,
            detail="patient medical data not found",
        )
    print(medicaldata.patientdata.doctor_id,token.id,medicaldata.patientdata.doctor_id!=token.id)
    if medicaldata.patient_id == patient_id or medicaldata.patientdata.doctor_id!=token.id:
        raise HTTPException(
            status_code=404,
            detail="patient medical data not found 1",
        )
    return medicaldata

@app.put("/doctors/patients/{patient_id}/medicaldata/{medicaldata_id}",response_model=patientMedicalDataSchema.PatientMedicalData)
async def update_patient_Medical_Data(patient_id,medicaldata_id,patientMedicalDataUpdated:patientMedicalDataSchema.PatientMedicalDataBase,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    patientMedicalData=PatientMedicalDataCRUD.get_patient_Medical_Data_by_id(db, medicaldata_id)
    if not patientMedicalData:
        raise HTTPException(
            status_code=404,
            detail="patientMedicalData not found",
        )
    if patientMedicalData.patient_id == patient_id or medicaldata.patientdata.doctor_id!=token.id:
        raise HTTPException(status_code=404,detail="patientMedicalData not found")
    patient=PatientMedicalDataCRUD.update_patient_Medical_Data(db, patientMedicalDataUpdated, patientMedicalData)
    return patient

@app.delete("/doctors/patients/{patient_id}/medicaldata/{medicaldata_id}")
async def delete(patient_id,medicaldata_id,token:doctorSchema.Token=Depends(jwtTokens.decode_access_token), db: Session = Depends(get_db)):
    return PatientMedicalDataCRUD.delete_patient_Medical_Data(db, medicaldata_id, patient_id,token)

# def get_predict(cancerModel: BaseCancer, filename):
#     path = os.path.join(os.path.abspath(os.path.dirname(__file__)),UPLOAD_FOLDER,filename);
#     if type(cancerModel) == type(BrainCancer()):
#         img = cv2.imread(path)
#         opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#         img = cv2.resize(opencvImage,(150,150))
#     else:
#         img  = load_img(path, target_size=cancerModel.get_target_size())
#     return cancerModel.predict(img)

@app.post('/uploader/')
async def upload_file(cancerType: Annotated[str, Form()], file: UploadFile = File(...)):
        # check if the post request has the file part
       # If the user does not select a file, the browser submits an
        # empty file without a filename.
    # if file.filename == '':
    #     flash('No selected file')
    #     return redirect(request.url)

    # if (file.filename):
    #     letters = string.ascii_lowercase
    #     filename = ''.join(random.choice(letters) for i in range(12))+os.path.splitext(file.filename)[1]
    #     #os.path.join(os.path.abspath(os.path.dirname(__file__)),UPLOAD_FOLDER,filename)
    #     with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),UPLOAD_FOLDER,filename),'wb') as img:
    #         content = await file.read()
    #         img.write(content)
    #         img.close()

        result = 'unknown cancer type'

        # if cancerType == 'lungCancer':
        #     result = get_predict(lungCancer, filename)
        # elif cancerType == 'cervicalCancer':
        #     result = get_predict(cervicalCancer, filename)
        # elif cancerType == 'brainCancer':
        #     result = get_predict(brainCancer, filename)


        return  JSONResponse(content={"result": result}, status_code=200)

@app.get("/uploads/{filename}")
async def read_item( filename: str):
    return FileResponse("uploads/"+filename)
