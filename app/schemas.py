from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"

class NoteStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = Field(default=UserRole.AGENT)  # Rol alanı eklendi

class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class NoteBase(BaseModel):
    raw_text: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    summary: Optional[str] = None
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StatusHistory(BaseModel):
    id: int
    note_id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# İsteğe bağlı: Not ile birlikte status history döndürmek için
class NoteWithStatusHistory(Note):
    status_history: List[StatusHistory] = []

    class Config:
        from_attributes = True