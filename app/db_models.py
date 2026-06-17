"""
app/db_models.py — SQLAlchemy ORM Models (Tabel Database)

Mendefinisikan struktur tabel di Supabase PostgreSQL:
- UserDB     → tabel 'users'
- MahasiswaDB → tabel 'mahasiswas'
- PertemuanDB → tabel 'pertemuans' (+ kolom kelas)
- PenilaianDB → tabel 'penilaians' (relasi ke pertemuan & mahasiswa)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class UserDB(Base):
    """Tabel akun pengguna sistem (Dosen & Aslab)."""
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Bcrypt hash
    role     = Column(String, nullable=False)  # "dosen" | "aslab"


class MahasiswaDB(Base):
    """Tabel data mahasiswa."""
    __tablename__ = "mahasiswas"

    id      = Column(Integer, primary_key=True, index=True)
    nim     = Column(String(12), unique=True, index=True, nullable=False)
    nama    = Column(String, nullable=False)
    jurusan = Column(String, nullable=False)
    kelas   = Column(String, nullable=False, index=True)

    # Relasi: satu mahasiswa bisa punya banyak penilaian
    penilaians = relationship("PenilaianDB", back_populates="mahasiswa")


class PertemuanDB(Base):
    """
    Tabel sesi pertemuan praktikum.
    Setiap pertemuan terikat ke satu kelas (misal '03TPLE005').
    """
    __tablename__ = "pertemuans"

    id          = Column(Integer, primary_key=True, index=True)
    topik       = Column(String, nullable=False)
    kelas       = Column(String, nullable=False, index=True)  # NEW: filter by kelas
    waktu_mulai = Column(DateTime, default=datetime.now, nullable=False)
    waktu_selesai = Column(DateTime, nullable=True)
    status      = Column(String, default="aktif", nullable=False)  # aktif | selesai

    # Relasi: satu pertemuan punya banyak penilaian
    penilaians = relationship("PenilaianDB", back_populates="pertemuan", cascade="all, delete-orphan")


class PenilaianDB(Base):
    """
    Tabel rekap penilaian mahasiswa per pertemuan.
    Relasi: many-to-one ke PertemuanDB & MahasiswaDB.
    """
    __tablename__ = "penilaians"

    id           = Column(Integer, primary_key=True, index=True)
    pertemuan_id = Column(Integer, ForeignKey("pertemuans.id"), nullable=False)
    nim          = Column(String(12), ForeignKey("mahasiswas.nim"), nullable=False)
    ceklis       = Column(Integer, nullable=False)   # Rating bintang 1–5
    waktu_selesai = Column(DateTime, nullable=False)
    durasi_menit  = Column(Float, nullable=False)

    # Relasi back-reference
    pertemuan  = relationship("PertemuanDB", back_populates="penilaians")
    mahasiswa  = relationship("MahasiswaDB", back_populates="penilaians")
