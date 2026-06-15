import os
import json
import pytest
from fastapi.testclient import TestClient

import app.manager as manager 
from app.main import app

client = TestClient(app)

# ==========================================
# SETUP DATABASE TESTING (MOCKING)
# ==========================================
TEST_USER_FILE = "test_users.json"
TEST_MAHASISWA_FILE = "test_mahasiswa.json"
TEST_PERTEMUAN_FILE = "test_pertemuan.json"
TEST_PENILAIAN_FILE = "test_penilaian.json"

manager.USER_FILE = TEST_USER_FILE
manager.DATA_FILE = TEST_MAHASISWA_FILE
manager.PERTEMUAN_FILE = TEST_PERTEMUAN_FILE
manager.PENILAIAN_FILE = TEST_PENILAIAN_FILE

@pytest.fixture(autouse=True)
def setup_teardown():
    from app.auth import get_password_hash
    
    dummy_users = [
        {"username": "dosen_test", "password": get_password_hash("dosen123"), "role": "dosen"},
        {"username": "aslab_test", "password": get_password_hash("aslab123"), "role": "aslab"}
    ]
    with open(TEST_USER_FILE, "w") as f: json.dump(dummy_users, f)
    with open(TEST_MAHASISWA_FILE, "w") as f: json.dump([], f)
    with open(TEST_PERTEMUAN_FILE, "w") as f: json.dump([], f)
    with open(TEST_PENILAIAN_FILE, "w") as f: json.dump([], f)
    
    yield
    
    if os.path.exists(TEST_USER_FILE): os.remove(TEST_USER_FILE)
    if os.path.exists(TEST_MAHASISWA_FILE): os.remove(TEST_MAHASISWA_FILE)
    if os.path.exists(TEST_PERTEMUAN_FILE): os.remove(TEST_PERTEMUAN_FILE)
    if os.path.exists(TEST_PENILAIAN_FILE): os.remove(TEST_PENILAIAN_FILE)

# ==========================================
# SKENARIO TESTING
# ==========================================

def test_login_success():
    """Test fitur login dan mendapatkan token JWT"""
    response = client.post("/login", data={"username": "dosen_test", "password": "dosen123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failed():
    """Test fitur login dengan password salah"""
    response = client.post("/login", data={"username": "dosen_test", "password": "salah_password"})
    assert response.status_code == 400

def test_create_mahasiswa_with_auth():
    """Test CRUD Create Mahasiswa dengan token Dosen"""
    login_res = client.post("/login", data={"username": "dosen_test", "password": "dosen123"})
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nama": "Mahasiswa Dummy",
        "nim": "241011459999",  # SULAP JADI 12 DIGIT
        "jurusan": "Teknik Informatika",
        "kelas": "03TPLE005"
    }
    response = client.post("/mahasiswa", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["nim"] == "241011459999"

def test_rbac_aslab_cannot_access_users():
    """Test Middleware RBAC: Aslab harus ditolak (403) saat mau akses data user/admin"""
    login_res = client.post("/login", data={"username": "aslab_test", "password": "aslab123"})
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Akses ditolak! Fitur ini hanya untuk Dosen."

def test_search_mahasiswa():
    """Test algoritma Linear/Binary Search via API"""
    login_res = client.post("/login", data={"username": "dosen_test", "password": "dosen123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # INDONESIAKAN NIM JADI 12 DIGIT BIAR LOLOS REGEX PYDANTIC
    client.post("/mahasiswa", json={"nama": "A", "nim": "241011450001", "jurusan": "TI", "kelas": "03TPLE005"}, headers=headers)
    client.post("/mahasiswa", json={"nama": "B", "nim": "241011450002", "jurusan": "SI", "kelas": "03TPLE005"}, headers=headers)
    
    # Test pencarian dengan NIM 12 digit
    search_res = client.get("/mahasiswa/search?nim=241011450002&method=linear", headers=headers)
    assert search_res.status_code == 200
    assert search_res.json()["nama"] == "B"

def test_create_pertemuan_and_input_nilai():
    """Test fitur Pertemuan (timer) dan Penilaian"""
    login_res = client.post("/login", data={"username": "dosen_test", "password": "dosen123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Buat mahasiswa dulu untuk dinilai
    client.post("/mahasiswa", json={"nama": "Mahasiswa Uji", "nim": "241011450099", "jurusan": "TI", "kelas": "03TPLE005"}, headers=headers)
    
    # 2. Buat pertemuan
    res_pert = client.post("/pertemuan", json={"topik": "Pertemuan 1"}, headers=headers)
    assert res_pert.status_code == 200
    pert_id = res_pert.json()["id"]
    assert res_pert.json()["status"] == "aktif"
    
    # 3. Input nilai
    res_nilai = client.post(f"/pertemuan/{pert_id}/nilai", json={"nim": "241011450099", "ceklis": 3}, headers=headers)
    assert res_nilai.status_code == 200
    assert res_nilai.json()["durasi_menit"] >= 0
    assert res_nilai.json()["ceklis"] == 3
    
    # 4. Tutup pertemuan
    res_tutup = client.put(f"/pertemuan/{pert_id}/tutup", headers=headers)
    assert res_tutup.status_code == 200
    assert res_tutup.json()["status"] == "selesai"