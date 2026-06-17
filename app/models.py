"""
app/models.py — Pydantic Schemas (Validasi Request & Response)

KONSEP OOP: Dipertahankan inheritance, encapsulation, polymorphism.
Semua schema menggunakan from_attributes=True agar bisa langsung
di-serialize dari SQLAlchemy ORM objects.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import re


# ─── MAHASISWA ────────────────────────────────────────────────────────────────

# KONSEP OOP: Base Class (Encapsulation awal)
class Person(BaseModel):
    nama: str

# KONSEP OOP: Inheritance (Mahasiswa mewarisi Person)
class Mahasiswa(Person):
    # REGEX: NIM harus 12 digit angka
    nim: str = Field(..., pattern=r"^\d{12}$")
    jurusan: str
    kelas: str

    model_config = ConfigDict(from_attributes=True)

    # KONSEP OOP: Polymorphism (Representasi objek dalam string)
    def display_info(self):
        return f"{self.nama} ({self.nim})"


# ─── USER ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = Field(..., pattern="^(dosen|aslab)$")  # Role hanya boleh dosen atau aslab

class UserResponse(BaseModel):
    username: str
    role: str

    model_config = ConfigDict(from_attributes=True)


# ─── PERTEMUAN ────────────────────────────────────────────────────────────────

class PertemuanCreate(BaseModel):
    topik: str
    kelas: str  # Wajib diisi — pertemuan terikat ke kelas tertentu

class Pertemuan(BaseModel):
    id: int
    topik: str
    kelas: str
    waktu_mulai: datetime
    waktu_selesai: Optional[datetime] = None
    status: str = "aktif"  # aktif | selesai

    model_config = ConfigDict(from_attributes=True)


# ─── PENILAIAN ────────────────────────────────────────────────────────────────

class PenilaianCreate(BaseModel):
    nim: str = Field(..., pattern=r"^\d{12}$")
    ceklis: int = Field(..., ge=1, le=5)  # Rating bintang 1–5

class Penilaian(BaseModel):
    id: int
    pertemuan_id: int
    nim: str
    ceklis: int
    waktu_selesai: datetime
    durasi_menit: float

    model_config = ConfigDict(from_attributes=True)