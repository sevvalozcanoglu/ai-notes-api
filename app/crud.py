from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    # Rol bilgisini de kaydediyoruz (default: AGENT)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role if hasattr(user, 'role') else schemas.UserRole.AGENT
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_notes(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(models.Note)
    if user_id:
        query = query.filter(models.Note.owner_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_user_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).offset(skip).limit(limit).all()

def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note_status(db: Session, note_id: int, status: str, summary: str = None):
    db_note = get_note(db, note_id)
    if db_note:
        db_note.status = status
        if summary is not None:  # Bu satırı düzeltiyoruz
            db_note.summary = summary
        db.commit()
        db.refresh(db_note)
    return db_note

def create_status_log(db: Session, note_id: int, user_id: int, status: str):
    db_status_log = models.NoteStatusLog(note_id=note_id, user_id=user_id, status=status)
    db.add(db_status_log)
    db.commit()
    db.refresh(db_status_log)
    return db_status_log

def get_note_status_history(db: Session, note_id: int):
    return db.query(models.NoteStatusLog).filter(models.NoteStatusLog.note_id == note_id).order_by(models.NoteStatusLog.created_at).all()