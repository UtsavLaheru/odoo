from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, database

# This line creates the database file and tables automatically
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency to get a database session for each request
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    new_user = models.User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user