from pydantic import BaseModel, Field
import re

# KONSEP OOP: Base Class (Encapsulation awal)
class Person(BaseModel):
    nama: str

# KONSEP OOP: Inheritance (Mahasiswa mewarisi Person)
class Mahasiswa(Person):
    # REGEX: NIM harus 12 digit angka
    nim: str = Field(..., pattern=r"^\d{12}$")
    jurusan: str
    kelas: str

    # KONSEP OOP: Polymorphism (Representasi objek dalam string)
    def display_info(self):
        return f"{self.nama} ({self.nim})"

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = Field(..., pattern="^(dosen|aslab)$") # Role hanya boleh dosen atau aslab

class UserResponse(BaseModel):
    username: str
    role: str

class PertemuanCreate(BaseModel):
    topik: str

class Pertemuan(BaseModel):
    id: int
    topik: str
    waktu_mulai: str
    status: str = "aktif" # aktif / selesai

class PenilaianCreate(BaseModel):
    nim: str = Field(..., pattern=r"^\d{12}$")
    ceklis: int = Field(..., ge=0)

class Penilaian(BaseModel):
    id: int
    pertemuan_id: int
    nim: str
    ceklis: int
    waktu_selesai: str
    durasi_menit: float