from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal
from app import models
from app.routers import users, notes
import os
from alembic import command
from alembic.config import Config


# Alembic migration'ı uygulama başlangıcında çalıştır
def run_migrations():
    try:
        # Önce tabloları kontrol et, zaten varsa migration çalıştırma
        from sqlalchemy import inspect
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            print("No tables found, running migrations...")
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            print("Database migrations applied successfully")
        else:
            print("Tables already exist, skipping migrations")
    except Exception as e:
        print(f"Migration error: {e}")
        # Fallback: Tabloları doğrudan oluştur
        print("Falling back to direct table creation")
        models.Base.metadata.create_all(bind=engine)


# Migration'ları çalıştır
run_migrations()

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Notes Summarizer API",
    description="API for AI-powered note summarization with authentication",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])


@app.get("/")
async def read_root():
    return {"message": "Notes Summarizer API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notes-api"}
