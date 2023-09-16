from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import crud
import schemas
# from . import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/panamas/", response_model=schemas.PanamaCreate)
def create_panama(panama: schemas.PanamaCreate, db: Session = Depends(get_db)):
    db_panama = crud.get_panama_by_url(db, mileage=panama.mileage)
    if db_panama and db_panama.price == panama.price:
        raise HTTPException(status_code=400, detail="Car already exist")
    return crud.create_panama(db=db, panama=panama)


@app.get("/panamas/", response_model=list[schemas.Panama])
def read_panama(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    panamas = crud.get_panamas(db, skip=skip, limit=limit)
    return panamas


@app.get("/panamas/{panama_id}", response_model=schemas.Panama)
def read_panama(panama_id: int, db: Session = Depends(get_db)):
    db_panama = crud.get_panama(db, panama_id=panama_id)
    if db_panama is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_panama

@app.delete("/panamas/{panama_id}", response_model=dict)
def delete_panama(panama_id: int, db: Session = Depends(get_db)):
    db_panama = crud.get_panama(db, panama_id=panama_id)
    if db_panama is None:
        raise HTTPException(status_code=404, detail="Car not found")
    crud.delete_panama(db, panama_id)
    return {
        "status": "ok"
    }


@app.put("/panamas/{panama_id}", response_model=schemas.Panama)
def update_panama(panama_id: int, panama: schemas.PanamaCreate, db: Session = Depends(get_db)):
    db_panama = crud.get_panama(db, panama_id=panama_id)
    if db_panama is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db_panama = crud.update_panama(db, panama_id, panama)
    return db_panama

