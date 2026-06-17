"""
app/auth.py — Autentikasi JWT + RBAC (Role-Based Access Control)

Perubahan dari versi sebelumnya:
- SECRET_KEY dipindah ke environment variable (.env) — tidak di-hardcode lagi
- get_current_user sekarang query user dari database (bukan baca file JSON)
"""

import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .database import get_db
from .db_models import UserDB

load_dotenv()  # pastikan env sudah dimuat sebelum baca SECRET_KEY

# SECRET_KEY sekarang dari .env — lebih aman
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_ganti_segera")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi password plain text dengan bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash password menggunakan bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def create_access_token(data: dict) -> str:
    """Buat JWT access token dengan expiry."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserDB:
    """
    FastAPI dependency — decode JWT dan ambil user dari database.
    Dipakai di semua route yang memerlukan autentikasi.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # Query user dari database (bukan baca JSON)
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def require_dosen(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    """
    FastAPI dependency — pastikan user yang login adalah Dosen.
    Gunakan sebagai Depends() di route yang hanya boleh diakses Dosen.
    """
    if current_user.role != "dosen":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses ditolak! Fitur ini hanya untuk Dosen."
        )
    return current_user