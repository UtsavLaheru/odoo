from fastapi import FastAPI, Path, HTTPException, Query, Depends, status,Response
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,computed_field, Field, EmailStr
from typing import Annotated,Literal,Optional
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session
import models, database
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

models.Base.metadata.create_all(bind=database.engine)

SECRET_KEY = "SecretCodethatcantbebreak"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

class Signup(BaseModel):
    name: Annotated[str,Field(...,description='Name Of User',examples= ['Ajit Chauhan',"Utsav Laheru"])]
    email: Annotated[EmailStr,Field(...,description='Email of User',examples=['Ajit@gmail.com',"Utsav@gmail.com"])]
    password: Annotated[str,Field(...,description='Password Of User',examples=['Ajit@1234'])]

class Login(BaseModel):
    email: Annotated[EmailStr,Field(...,description='Email of User',examples=['Ajit@gmail.com',"Utsav@gmail.com"])]
    password: Annotated[str,Field(...,description='Password Of User',examples=['Ajit@1234'])]


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app= FastAPI()

@app.post('/signup/')
def create_user(sign:Signup, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == sign.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(name=sign.name, email=sign.email, password=sign.password) 
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User created successfully"
    }


@app.post('/login/')
def fetch_user(login:Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User does not exist"
        )

    if user.password != login.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )

    token = create_access_token(data={"sub": user.email})
    # response.set_cookie(key="access_token", value=token, httponly=True)
    
    return {
        "access_token": token, 
        "token_type": "bearer",
        "name": user.name,
        "email": user.email,
        "message": "Login successful"
    }
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
@app.get("/dashboard")
def get_dashboard(token: str = Depends(oauth2_scheme)):
    try:
        # Verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": f"Welcome, {email}!"}
    except:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    
@app.get('/view/')
def view(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user
    
@app.post("/request/")
def create_request(equipment_id: int, subject: str, db: Session = Depends(get_db)):
    # 1. Fetch Equipment details to auto-fill [cite: 43]
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
        
    new_request = models.MaintenanceRequest(
        subject=subject,
        equipment_id=equipment_id,
        team_id=equipment.team_id, # Auto-fill [cite: 43]
        request_type="Corrective",
        stage="New" # Starts in New stage [cite: 44]
    )
    db.add(new_request)
    db.commit()
    return new_request

@app.patch("/request/{request_id}/move")
def move_request_stage(request_id: int, new_stage: str, db: Session = Depends(get_db)):
    request = db.query(models.MaintenanceRequest).filter(models.MaintenanceRequest.id == request_id).first()
    
    # Execution logic: Update stage and handle Scrap [cite: 46, 72]
    request.stage = new_stage
    
    if new_stage == "Scrap":
        equipment = db.query(models.Equipment).filter(models.Equipment.id == request.equipment_id).first()
        equipment.is_usable = False # Mark as no longer usable [cite: 72]
        
    db.commit()
    return {"message": f"Moved to {new_stage}"}

@app.get("/equipment/{equipment_id}/stats")
def get_equipment_stats(equipment_id: int, db: Session = Depends(get_db)):
    # Badge: Display count of open requests [cite: 70]
    request_count = db.query(models.MaintenanceRequest).filter(
        models.MaintenanceRequest.equipment_id == equipment_id,
        models.MaintenanceRequest.stage != "Repaired"
    ).count()
    
    return {"open_requests": request_count}
