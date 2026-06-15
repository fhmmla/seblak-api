import json
import os
from fastapi import HTTPException

# Menyimpan data mahasiswa untuk CRUD
DATA_FILE: str = "data/mahasiswa.json"

# Menyimpan data user untuk autentikasi
USER_FILE: str = "data/users.json"

# Menyimpan data pertemuan & penilaian
PERTEMUAN_FILE: str = "data/pertemuan.json"
PENILAIAN_FILE: str = "data/penilaian.json"

class JSONManager:
    @staticmethod
    def read_mahasiswa():
        # TRY-CATCH: Penanganan error file
        try:
            if not os.path.exists(DATA_FILE):
                return []
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise HTTPException(status_code=500, detail=f"Gagal membaca database: {str(e)}")

    @staticmethod
    def write_mahasiswa(data):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            raise HTTPException(status_code=500, detail=f"Gagal menulis ke database: {str(e)}")

    @staticmethod
    def read_users():
        try:
            if not os.path.exists(USER_FILE): return []
            with open(USER_FILE, "r") as f: return json.load(f)
        except Exception: return []

    @staticmethod
    def write_users(data):
        with open(USER_FILE, "w") as f: json.dump(data, f, indent=4)

    @staticmethod
    def read_pertemuan():
        try:
            if not os.path.exists(PERTEMUAN_FILE): return []
            with open(PERTEMUAN_FILE, "r") as f: return json.load(f)
        except Exception: return []

    @staticmethod
    def write_pertemuan(data):
        with open(PERTEMUAN_FILE, "w") as f: json.dump(data, f, indent=4)

    @staticmethod
    def read_penilaian():
        try:
            if not os.path.exists(PENILAIAN_FILE): return []
            with open(PENILAIAN_FILE, "r") as f: return json.load(f)
        except Exception: return []

    @staticmethod
    def write_penilaian(data):
        with open(PENILAIAN_FILE, "w") as f: json.dump(data, f, indent=4)