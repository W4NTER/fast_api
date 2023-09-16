from sqlalchemy.orm import Session
from datetime import datetime
# from . import models, schemas
import models
import schemas


def get_panama(db: Session, panama_id: int):
    return db.query(models.Panama).filter(models.Panama.id == panama_id).first()


def get_panama_by_url(db: Session, mileage: int):
    return db.query(models.Panama).filter(models.Panama.url == url).order_by(
        models.Panama.datetime.desc()).first()


def get_panamas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Panama).offset(skip).limit(limit).all()


def create_panama(db: Session, panama: schemas.PanamaCreate):
    dt = datetime.now()
    db_panama = models.Panama(
        year=panama.year,
        url=panama.url,
        price=panama.price,
        mileage=panama.mileage,
        datetime=dt
    )
    db.add(db_panama)
    db.commit()
    db.refresh(db_panama)
    return db_panama


def delete_panama(db: Session, panama_id: int):
    item = db.query(models.Panama).filter(models.Panama.id == panama_id).delete()
    db.commit()
    return


def update_panama(db: Session, panama_id: int, panama: schemas.PanamaCreate):
    item = db.query(models.Panama).filter(models.Panama.id == panama_id).first()
    item.url = panama.url
    item.year = panama.year
    item.price = panama.price
    item.mileage = panama.mileage
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# def add_panama(db: Session, panama_url: str, panama: schemas.PanamaCreate):
#     is_exist = session.query(models.Panama).filter(models.Panama.mileage == mileage).order_by(
#         models.Panama.datetime.desc()).first()
#     item.url = panama.url
#     item.year = panama.year
#     item.price = panama.price
#     item.mileage = panama.mileage
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item