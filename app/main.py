from fastapi import FastAPI, HTTPException, Depends, Query
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from .models import Mahasiswa, UserCreate, UserResponse, PertemuanCreate, Pertemuan, PenilaianCreate, Penilaian
from .manager import JSONManager
from .algorithms import MahasiswaAlgo
from .auth import verify_password, create_access_token, get_password_hash, get_current_user, require_dosen

app = FastAPI(
    title="SEBLAK API",
    description="Sistem Evaluasi Belajar Lab Akademik & Kelas",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Selamat datang di SEBLAK API 🍜",
        "kisi_kisi": "Sistem Evaluasi Belajar Lab Akademik & Kelas",
        "author": "Fahmi Maulana Fadila (241011450401)",
        "fitur_unggulan": [
            "Manajemen Data Mahasiswa (CRUD)",
            "Sistem Penilaian Praktikum Otomatis (Timer backend 100% akurat)",
            "Pencarian (Linear & Sequential & Binary Search)",
            "Pengurutan (Insertion & Selection Sort)",
            "Keamanan dengan JWT Token & RBAC (Dosen/Aslab)"
        ],
        "panduan_api": "Buka URL endpoint /docs untuk melihat dokumentasi interaktif Swagger UI"
    }

# ==========================================
# AUTHENTICATION ROUTE
# ==========================================
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = JSONManager.read_users()
    user = next((u for u in users if u["username"] == form_data.username), None)
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Username atau password salah")
        
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# ==========================================
# USER CRUD ROUTES (KHUSUS DOSEN)
# ==========================================
@app.post("/users", response_model=UserResponse, dependencies=[Depends(require_dosen)])
def create_user(user: UserCreate):
    users = JSONManager.read_users()
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username sudah dipakai")
        
    new_user = {
        "username": user.username,
        "password": get_password_hash(user.password), # Enkripsi password sebelum disave
        "role": user.role
    }
    users.append(new_user)
    JSONManager.write_users(users)
    return new_user

@app.get("/users", response_model=list[UserResponse], dependencies=[Depends(require_dosen)])
def get_all_users():
    return JSONManager.read_users()

@app.delete("/users/{username}", dependencies=[Depends(require_dosen)])
def delete_user(username: str, current_user: dict = Depends(get_current_user)):
    if username == current_user["username"]:
        raise HTTPException(status_code=400, detail="Tidak dapat menghapus akun sendiri")
    users = JSONManager.read_users()
    new_users = [u for u in users if u["username"] != username]
    if len(new_users) == len(users):
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    JSONManager.write_users(new_users)
    return {"message": f"User '{username}' berhasil dihapus"}

# ==========================================
# MAHASISWA CRUD ROUTES (DOSEN & ASLAB BISA AKSES)
# ==========================================

@app.post("/mahasiswa", response_model=Mahasiswa)
def create_mahasiswa(mhs: Mahasiswa, current_user: dict = Depends(get_current_user)):
    data = JSONManager.read_mahasiswa()
    if any(d['nim'] == mhs.nim for d in data):
        raise HTTPException(status_code=400, detail="NIM sudah terdaftar!")
    data.append(mhs.model_dump())
    JSONManager.write_mahasiswa(data)
    return mhs

@app.get("/mahasiswa")
def read_all_mahasiswa(current_user: dict = Depends(get_current_user)):
    return JSONManager.read_mahasiswa()

# Fitur Pencarian Data (Exact Match)
@app.get("/mahasiswa/search")
def search_mahasiswa(nim: str, method: str = "linear", current_user: dict = Depends(get_current_user)):
    data = JSONManager.read_mahasiswa()
    if method == "linear":
        result = MahasiswaAlgo.linear_search(data, nim)
    else:
        result = MahasiswaAlgo.binary_search(data, nim)
    
    if not result:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return result

# Fitur Pencarian Data (Sequential Search - Partial Match)
@app.get("/mahasiswa/sequential-search")
def sequential_search_mahasiswa(keyword: str, current_user: dict = Depends(get_current_user)):
    data = JSONManager.read_mahasiswa()
    results = MahasiswaAlgo.sequential_search(data, keyword)
    
    if not results:
        raise HTTPException(status_code=404, detail="Tidak ada mahasiswa yang cocok dengan keyword")
    return results

# Fitur Pengurutan Data
@app.get("/mahasiswa/sort")
def sort_mahasiswa(method: str = "insertion", key: str = "nim", current_user: dict = Depends(get_current_user)):
    data = JSONManager.read_mahasiswa()
    if method == "insertion":
        return MahasiswaAlgo.insertion_sort(data, key)
    return MahasiswaAlgo.selection_sort(data, key)

# Fitur Update Data
@app.put("/mahasiswa/{nim}", response_model=Mahasiswa)
def update_mahasiswa(nim: str, mhs_update: Mahasiswa, current_user: dict = Depends(get_current_user)):
    data = JSONManager.read_mahasiswa()
    for i, mhs in enumerate(data):
        if mhs['nim'] == nim:
            # Validasi tambahan biar NIM baru yang diinput ga bentrok sama mahasiswa lain
            if mhs_update.nim != nim and any(d['nim'] == mhs_update.nim for d in data):
                raise HTTPException(status_code=400, detail="NIM baru sudah dipakai mahasiswa lain!")
            data[i] = mhs_update.model_dump()
            JSONManager.write_mahasiswa(data)
            return mhs_update
    raise HTTPException(status_code=404, detail="NIM tidak ditemukan")

# Fitur Hapus Data
@app.delete("/mahasiswa/{nim}")
def delete_mahasiswa(nim: str, current_user: dict = Depends(get_current_user)):
    data = JSONManager.read_mahasiswa()
    new_data = [d for d in data if d['nim'] != nim]
    
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="NIM tidak ditemukan")
        
    JSONManager.write_mahasiswa(new_data)
    return {"message": f"Mahasiswa dengan NIM {nim} berhasil dihapus"}

# ==========================================
# PENILAIAN & PERTEMUAN ROUTES (TIMER & CEKLIS)
# ==========================================

@app.post("/pertemuan", response_model=Pertemuan)
def create_pertemuan(data: PertemuanCreate, current_user: dict = Depends(get_current_user)):
    pertemuan_list = JSONManager.read_pertemuan()
    new_id = 1 if not pertemuan_list else max(p["id"] for p in pertemuan_list) + 1
    new_pertemuan = {
        "id": new_id,
        "topik": data.topik,
        "waktu_mulai": datetime.now().isoformat(),
        "status": "aktif"
    }
    pertemuan_list.append(new_pertemuan)
    JSONManager.write_pertemuan(pertemuan_list)
    return new_pertemuan

@app.get("/pertemuan", response_model=list[Pertemuan])
def get_all_pertemuan(current_user: dict = Depends(get_current_user)):
    return JSONManager.read_pertemuan()

@app.put("/pertemuan/{id}/tutup", response_model=Pertemuan)
def tutup_pertemuan(id: int, current_user: dict = Depends(get_current_user)):
    pertemuan_list = JSONManager.read_pertemuan()
    for p in pertemuan_list:
        if p["id"] == id:
            p["status"] = "selesai"
            JSONManager.write_pertemuan(pertemuan_list)
            return p
    raise HTTPException(status_code=404, detail="Pertemuan tidak ditemukan")

@app.post("/pertemuan/{id}/nilai", response_model=Penilaian)
def input_penilaian(id: int, data: PenilaianCreate, current_user: dict = Depends(get_current_user)):
    pertemuan_list = JSONManager.read_pertemuan()
    pertemuan = next((p for p in pertemuan_list if p["id"] == id), None)
    if not pertemuan:
        raise HTTPException(status_code=404, detail="Pertemuan tidak ditemukan")
    if pertemuan["status"] != "aktif":
        raise HTTPException(status_code=400, detail="Pertemuan sudah ditutup")
    
    # Validasi NIM ada
    mhs_list = JSONManager.read_mahasiswa()
    if not any(m['nim'] == data.nim for m in mhs_list):
        raise HTTPException(status_code=404, detail="NIM mahasiswa tidak ditemukan")

    penilaian_list = JSONManager.read_penilaian()
    
    # Kalkulasi durasi
    waktu_mulai = datetime.fromisoformat(pertemuan["waktu_mulai"])
    waktu_selesai = datetime.now()
    durasi_detik = (waktu_selesai - waktu_mulai).total_seconds()
    durasi_menit = round(durasi_detik / 60, 2)

    new_id = 1 if not penilaian_list else max(p["id"] for p in penilaian_list) + 1
    new_penilaian = {
        "id": new_id,
        "pertemuan_id": id,
        "nim": data.nim,
        "ceklis": data.ceklis,
        "waktu_selesai": waktu_selesai.isoformat(),
        "durasi_menit": durasi_menit
    }
    penilaian_list.append(new_penilaian)
    JSONManager.write_penilaian(penilaian_list)
    return new_penilaian

@app.get("/pertemuan/{id}/nilai", response_model=list[Penilaian])
def get_penilaian_per_pertemuan(id: int, current_user: dict = Depends(get_current_user)):
    penilaian_list = JSONManager.read_penilaian()
    return [p for p in penilaian_list if p["pertemuan_id"] == id]