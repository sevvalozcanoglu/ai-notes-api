from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import users, notes

# Tabloları oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes Summarizer API",
    description="API for AI-powered note summarization with authentication",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da daha spesifik ayarlayın
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
