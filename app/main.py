"""
app/main.py — SEBLAK API Routes (FastAPI)

Modul ini merupakan titik masuk (entry point) utama untuk REST API.
Berisi definisi semua rute (endpoints) untuk manajemen data mahasiswa,
autentikasi pengguna, manajemen pertemuan, dan pencatatan penilaian.

Menggunakan SQLAlchemy ORM untuk interaksi dengan database PostgreSQL
dan mengimplementasikan injeksi dependensi (Dependency Injection) untuk
manajemen sesi database yang aman.
"""

import os
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from .models import Mahasiswa, UserCreate, UserResponse, PertemuanCreate, Pertemuan, PenilaianCreate, Penilaian
from .database import engine, get_db
from .db_models import UserDB, MahasiswaDB, PertemuanDB, PenilaianDB
from .db_models import Base  # Untuk create_all
from .manager import DatabaseManager
from .algorithms import MahasiswaAlgo
from .auth import verify_password, create_access_token, get_password_hash, get_current_user, require_dosen

load_dotenv()

app = FastAPI(
    title="SEBLAK API",
    description="Sistem Evaluasi Belajar Lab Akademik & Kelas — v2.0 (Supabase)",
    version="2.0.0"
)

# CORS — izinkan frontend Flask mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── STARTUP ──────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup_event():
    """
    Dijalankan saat server pertama kali start.
    1. Buat semua tabel di Supabase (jika belum ada)
    2. Seed user admin default (jika belum ada user)
    3. Seed data mahasiswa dari mahasiswa.json (jika tabel kosong)
    """
    # 1. Buat tabel
    Base.metadata.create_all(bind=engine)
    print("Tabel database berhasil dibuat/diverifikasi.")

    db = None
    try:
        from .database import SessionLocal
        db = SessionLocal()

        # 2. Seed admin user default
        admin_username = os.getenv("DEFAULT_ADMIN_USERNAME", "dosen_alpro")
        admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "secret")
        existing_admin = db.query(UserDB).filter(UserDB.username == admin_username).first()
        if not existing_admin:
            DatabaseManager.create_user(
                db=db,
                username=admin_username,
                hashed_password=get_password_hash(admin_password),
                role="dosen"
            )
            print(f"User admin '{admin_username}' berhasil dibuat.")
        else:
            print(f"User admin '{admin_username}' sudah ada.")

        # 3. Seed mahasiswa dari file JSON (jika tabel mahasiswas kosong)
        mhs_count = db.query(MahasiswaDB).count()
        if mhs_count == 0:
            import json, os as _os
            json_path = _os.path.join(_os.path.dirname(__file__), "..", "data", "mahasiswa.json")
            if _os.path.exists(json_path):
                with open(json_path, "r") as f:
                    mhs_list = json.load(f)
                for m in mhs_list:
                    db.add(MahasiswaDB(
                        nim=m["nim"], nama=m["nama"],
                        jurusan=m["jurusan"], kelas=m["kelas"]
                    ))
                db.commit()
                print(f"{len(mhs_list)} data mahasiswa berhasil di-seed dari mahasiswa.json.")
    except Exception as e:
        print(f"Startup seeding error: {e}")
    finally:
        if db:
            db.close()


# ─── ROOT ─────────────────────────────────────────────────────────────────────

@app.get("/")
def read_root():
    return {
        "message": "Selamat datang di SEBLAK API 🍜 v2.0",
        "storage": "Supabase PostgreSQL (Persistent)",
        "author": "Fahmi Maulana Fadila (241011450401)",
        "fitur_unggulan": [
            "Manajemen Data Mahasiswa (CRUD)",
            "Sistem Penilaian Praktikum Otomatis (Timer + Rating Bintang)",
            "Pertemuan by Kelas — Filter & Relasi",
            "Pencarian (Linear, Sequential, Binary Search)",
            "Pengurutan (Insertion & Selection Sort)",
            "Keamanan JWT Token & RBAC (Dosen/Aslab)",
            "Database Persistent: Supabase PostgreSQL"
        ],
        "panduan_api": "Buka /docs untuk Swagger UI interaktif"
    }


# ─── AUTHENTICATION ───────────────────────────────────────────────────────────

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = DatabaseManager.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Username atau password salah")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


# ─── USER CRUD (Dosen Only) ───────────────────────────────────────────────────

@app.get("/export-backup", dependencies=[Depends(require_dosen)])
def export_database_to_json(db: Session = Depends(get_db)):
    """
    Mengekspor seluruh data dari database ke dalam file JSON lokal.
    Memenuhi kriteria tugas: Penyimpanan ke file (File I/O Write).
    """
    import json, os
    
    # Ambil semua data
    users = [{"username": u.username, "role": u.role} for u in db.query(UserDB).all()]
    mhs = [{"nim": m.nim, "nama": m.nama, "jurusan": m.jurusan, "kelas": m.kelas} for m in db.query(MahasiswaDB).all()]
    
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "users": users,
        "mahasiswas": mhs
    }
    
    # Tulis ke file JSON (File I/O Write)
    backup_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, "backup.json")
    
    try:
        with open(backup_path, "w") as f:
            json.dump(backup_data, f, indent=4)
        return {
            "message": "Backup berhasil dibuat di server.", 
            "path": backup_path,
            "data": backup_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menulis file backup: {str(e)}")


@app.post("/users", response_model=UserResponse, dependencies=[Depends(require_dosen)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if DatabaseManager.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username sudah dipakai")
    new_user = DatabaseManager.create_user(db, user.username, get_password_hash(user.password), user.role)
    return new_user


@app.get("/users", response_model=list[UserResponse], dependencies=[Depends(require_dosen)])
def get_all_users(db: Session = Depends(get_db)):
    return DatabaseManager.get_all_users(db)


@app.delete("/users/{username}", dependencies=[Depends(require_dosen)])
def delete_user(username: str, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    if username == current_user.username:
        raise HTTPException(status_code=400, detail="Tidak dapat menghapus akun sendiri")
    if not DatabaseManager.delete_user(db, username):
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return {"message": f"User '{username}' berhasil dihapus"}


# ─── MAHASISWA CRUD ───────────────────────────────────────────────────────────

def mhs_to_dict(m: MahasiswaDB) -> dict:
    """Konversi ORM object ke dict untuk keperluan algoritma."""
    return {"nim": m.nim, "nama": m.nama, "jurusan": m.jurusan, "kelas": m.kelas}


@app.post("/mahasiswa", response_model=Mahasiswa)
def create_mahasiswa(mhs: Mahasiswa, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    if DatabaseManager.get_mahasiswa_by_nim(db, mhs.nim):
        raise HTTPException(status_code=400, detail="NIM sudah terdaftar!")
    new_mhs = DatabaseManager.create_mahasiswa(db, mhs.nim, mhs.nama, mhs.jurusan, mhs.kelas)
    return new_mhs


@app.get("/mahasiswa")
def read_all_mahasiswa(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
    kelas: str = Query(None, description="Filter mahasiswa berdasarkan kelas")
):
    """
    Ambil semua mahasiswa. Support filter by kelas:
    GET /mahasiswa?kelas=03TPLE005
    Dipakai frontend untuk populate dropdown NIM di form penilaian.
    """
    result = DatabaseManager.get_all_mahasiswa(db, kelas=kelas)
    return [mhs_to_dict(m) for m in result]


@app.get("/mahasiswa/kelas")
def get_daftar_kelas(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """Ambil daftar kelas unik dari data mahasiswa. Dipakai untuk dropdown filter & form pertemuan."""
    return DatabaseManager.get_distinct_kelas(db)


@app.get("/mahasiswa/search")
def search_mahasiswa(nim: str, method: str = "linear",
                     current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    data = [mhs_to_dict(m) for m in DatabaseManager.get_all_mahasiswa(db)]
    if method == "linear":
        result = MahasiswaAlgo.linear_search(data, nim)
    else:
        result = MahasiswaAlgo.binary_search(data, nim)
    if not result:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return result


@app.get("/mahasiswa/sequential-search")
def sequential_search_mahasiswa(keyword: str, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    data = [mhs_to_dict(m) for m in DatabaseManager.get_all_mahasiswa(db)]
    results = MahasiswaAlgo.sequential_search(data, keyword)
    if not results:
        raise HTTPException(status_code=404, detail="Tidak ada mahasiswa yang cocok dengan keyword")
    return results


@app.get("/mahasiswa/sort")
def sort_mahasiswa(method: str = "insertion", key: str = "nim",
                   current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    data = [mhs_to_dict(m) for m in DatabaseManager.get_all_mahasiswa(db)]
    if method == "insertion":
        return MahasiswaAlgo.insertion_sort(data, key)
    return MahasiswaAlgo.selection_sort(data, key)


@app.put("/mahasiswa/{nim}", response_model=Mahasiswa)
def update_mahasiswa(nim: str, mhs_update: Mahasiswa,
                     current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = DatabaseManager.get_mahasiswa_by_nim(db, nim)
    if not existing:
        raise HTTPException(status_code=404, detail="NIM tidak ditemukan")
    # Cek NIM baru tidak bertabrakan
    if mhs_update.nim != nim and DatabaseManager.get_mahasiswa_by_nim(db, mhs_update.nim):
        raise HTTPException(status_code=400, detail="NIM baru sudah dipakai mahasiswa lain!")
    updated = DatabaseManager.update_mahasiswa(db, nim, mhs_update.model_dump())
    return updated


@app.delete("/mahasiswa/{nim}")
def delete_mahasiswa(nim: str, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    if not DatabaseManager.delete_mahasiswa(db, nim):
        raise HTTPException(status_code=404, detail="NIM tidak ditemukan")
    return {"message": f"Mahasiswa dengan NIM {nim} berhasil dihapus"}


# ─── PERTEMUAN & PENILAIAN ────────────────────────────────────────────────────

@app.post("/pertemuan", response_model=Pertemuan)
def create_pertemuan(data: PertemuanCreate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    new_p = DatabaseManager.create_pertemuan(db, data.topik, data.kelas)
    return new_p


@app.get("/pertemuan", response_model=list[Pertemuan])
def get_all_pertemuan(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
    kelas: str = Query(None, description="Filter pertemuan berdasarkan kelas")
):
    """
    Ambil semua pertemuan. Support filter:
    GET /pertemuan?kelas=03TPLE005
    """
    return DatabaseManager.get_all_pertemuan(db, kelas=kelas)


@app.put("/pertemuan/{id}/tutup", response_model=Pertemuan)
def tutup_pertemuan(id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    result = DatabaseManager.tutup_pertemuan(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Pertemuan tidak ditemukan")
    return result


@app.post("/pertemuan/{id}/nilai", response_model=Penilaian)
def input_penilaian(id: int, data: PenilaianCreate,
                    current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    # Validasi pertemuan
    pertemuan = DatabaseManager.get_pertemuan_by_id(db, id)
    if not pertemuan:
        raise HTTPException(status_code=404, detail="Pertemuan tidak ditemukan")
    if pertemuan.status != "aktif":
        raise HTTPException(status_code=400, detail="Pertemuan sudah ditutup")

    # Validasi NIM mahasiswa ada di database
    mhs = DatabaseManager.get_mahasiswa_by_nim(db, data.nim)
    if not mhs:
        raise HTTPException(status_code=404, detail="NIM mahasiswa tidak ditemukan")

    # Validasi mahasiswa sesuai kelas pertemuan
    if mhs.kelas != pertemuan.kelas:
        raise HTTPException(
            status_code=400,
            detail=f"Mahasiswa dengan NIM {data.nim} bukan dari kelas {pertemuan.kelas}"
        )

    # Cek apakah mahasiswa sudah dinilai di pertemuan ini
    existing = db.query(PenilaianDB).filter(
        PenilaianDB.pertemuan_id == id,
        PenilaianDB.nim == data.nim
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"NIM {data.nim} sudah dinilai di pertemuan ini")

    # Kalkulasi durasi
    waktu_selesai = datetime.now()
    durasi_detik = (waktu_selesai - pertemuan.waktu_mulai).total_seconds()
    durasi_menit = round(durasi_detik / 60, 2)

    new_nilai = DatabaseManager.create_penilaian(
        db=db,
        pertemuan_id=id,
        nim=data.nim,
        ceklis=data.ceklis,
        waktu_selesai=waktu_selesai,
        durasi_menit=durasi_menit
    )
    return new_nilai


@app.get("/pertemuan/{id}/nilai", response_model=list[Penilaian])
def get_penilaian_per_pertemuan(id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    return DatabaseManager.get_penilaian_by_pertemuan(db, id)


@app.get("/penilaian/top")
def get_top_mahasiswa(limit: int = 10, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """Ambil top mahasiswa dengan rating bintang (ceklis) terbanyak."""
    return DatabaseManager.get_top_mahasiswa(db, limit)