from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas, crud, auth
from app.auth import get_current_user, get_current_admin
from app.celery_worker import summarize_note_task
from app.models import User

router = APIRouter()


@router.post("/", response_model=schemas.Note)
async def create_note(
        note: schemas.NoteCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Yeni not oluştur ve özetleme işlemini başlat"""
    db_note = crud.create_note(db, note, current_user.id)
    summarize_note_task.delay(db_note.id)
    return db_note


@router.get("/", response_model=List[schemas.Note])
async def read_notes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Kullanıcının notlarını getir"""
    if current_user.role == schemas.UserRole.ADMIN:
        notes = crud.get_notes(db, skip=skip, limit=limit)
    else:
        notes = crud.get_user_notes(db, user_id=current_user.id, skip=skip, limit=limit)
    return notes


@router.get("/{note_id}", response_model=schemas.Note)
async def read_note(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Belirli bir notu getir"""
    db_note = crud.get_note(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Yetki kontrolü: Admin veya notun sahibi
    if current_user.role != schemas.UserRole.ADMIN and db_note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return db_note


@router.get("/{note_id}/status-history", response_model=List[schemas.StatusHistory])
async def get_note_status_history(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_note = crud.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if current_user.role != schemas.UserRole.ADMIN and db_note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return crud.get_note_status_history(db, note_id)


# Admin-only endpoint - tüm notları görüntüleme
@router.get("/admin/all", response_model=List[schemas.Note])
async def read_all_notes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin)
):
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes


@router.get("/{note_id}/status-history", response_model=List[schemas.StatusHistory])
def get_note_status_history(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth.get_current_active_user)
):
    db_note = crud.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if current_user.role != "ADMIN" and db_note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return crud.get_note_status_history(db, note_id)