from celery import Celery
from sqlalchemy.orm import Session
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from app.database import SessionLocal
from app import crud, models
from app.summarizer import summarize_text

# Celery uygulamasını oluştur
celery_app = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

# Celery yapılandırması
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Istanbul',
    enable_utc=True,
)

@celery_app.task(bind=True, max_retries=3)
def summarize_note_task(self, note_id: int):
    """Not özetleme görevi - Sadece note_id alır"""
    db = SessionLocal()
    try:
        # Notu getir
        note = crud.get_note(db, note_id)
        if not note:
            raise ValueError(f"Note {note_id} not found")

        # Status: processing
        note.status = "processing"
        db.commit()
        crud.create_status_log(db, note_id, note.owner_id, "processing")

        # Özetleme yap
        summary = summarize_text(note.raw_text)
        print(f"Generated summary: {summary}")  # Debug için

        # Status: done ve summary'i güncelle
        note.status = "done"
        note.summary = summary  # Doğrudan güncelleme
        db.commit()
        crud.create_status_log(db, note_id, note.owner_id, "done")

        return {"status": "success", "summary": summary}

    except Exception as e:
        # Hata durumunda
        db.rollback()
        if note:
            note.status = "failed"
            db.commit()
            crud.create_status_log(db, note_id, note.owner_id, "failed")

        # Retry mekanizması
        try:
            raise self.retry(exc=e, countdown=60)
        except self.MaxRetriesExceededError:
            return {"status": "failed", "error": str(e)}
    finally:
        db.close()

# Test görevi
@celery_app.task
def test_task(x, y):
    return x + y