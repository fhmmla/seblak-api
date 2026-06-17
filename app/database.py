"""
app/database.py — Database Configuration & Connection Management

Modul ini bertanggung jawab untuk mengatur koneksi ke database PostgreSQL (Supabase)
menggunakan SQLAlchemy. Modul ini membangun (construct) Data Source Name (DSN)
dari environment variables, mengkonfigurasi connection pool, dan menyediakan
dependency injection (get_db) untuk manajemen sesi database pada setiap request.
"""

import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

# Ambil variabel koneksi dari .env (format Supabase)
DB_USER     = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_HOST     = os.getenv("host")
DB_PORT     = os.getenv("port", "5432")
DB_NAME     = os.getenv("dbname")
SECRET_KEY  = os.getenv("SECRET_KEY", "fallback_secret_ganti_segera")

# Validasi semua variabel tersedia
missing = [k for k, v in {
    "user": DB_USER, "password": DB_PASSWORD,
    "host": DB_HOST, "dbname": DB_NAME
}.items() if not v]
if missing:
    raise RuntimeError(f"Variabel .env berikut belum diisi: {', '.join(missing)}")

# Encode password agar karakter spesial (@, #, %, dll) aman di URL
encoded_password = quote_plus(DB_PASSWORD)

# Construct connection URL sesuai format Supabase (wajib sslmode=require)
DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
)

# Engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Test koneksi sebelum query (hindari koneksi mati)
    pool_size=5,
    max_overflow=10,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    FastAPI dependency — inject DB session ke setiap route.
    Session otomatis ditutup setelah request selesai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
