# 🍜 SEBLAK API (Sistem Evaluasi Belajar Lab Akademik & Kelas)

**Nama:** Fahmi Maulana Fadila  
**NIM:** 241011450401  
**Kelas:** 03TPLE005  
**Mata Kuliah:** Algoritma Dan Pemrograman II  
**Jenis Ujian:** UAS  

---

## 📖 Tentang Project

**SEBLAK (Sistem Evaluasi Belajar Lab Akademik & Kelas)** adalah **Backend REST API** untuk aplikasi Manajemen Data Mahasiswa terpadu yang dibangun menggunakan **FastAPI (Python)**. Selain menyediakan layanan CRUD mahasiswa biasa, SEBLAK berinovasi dengan fitur Penilaian Praktikum Otomatis (Timer & Ceklis), autentikasi JWT, role-based access control (RBAC), serta menerapkan berbagai konsep algoritma (Searching, Sorting) dan pemrograman berorientasi objek (OOP) sesuai dengan arahan tugas UAS.

🔗 **Repository:** [https://github.com/fhmmla/seblak-api](https://github.com/fhmmla/seblak-api)  
⚖️ **Lisensi:** MIT License

> **Catatan:** Project ini hanya mencakup sisi **Backend (API)**. Frontend akan dikembangkan secara terpisah.

---

## 🏗️ Struktur Project

```
Sourecode/
├── app/
│   ├── main.py          # Entry point API, seluruh route/endpoint
│   ├── models.py        # Pydantic models (OOP: Class, Inheritance, Polymorphism)
│   ├── auth.py          # Autentikasi JWT & bcrypt password hashing
│   ├── algorithms.py    # Algoritma Sorting & Searching
│   └── manager.py       # JSON File I/O Manager
├── data/
│   ├── mahasiswa.json   # Database mahasiswa (JSON)
│   └── users.json       # Database user/admin (JSON)
├── test/
│   ├── __init__.py
│   └── test_api.py      # Unit Testing dengan pytest
├── requirements.txt     # Daftar dependencies
└── venv/                # Virtual environment Python
```

---

## 🔧 Cara Menjalankan

### 1. Setup Virtual Environment
```bash
cd Sourecode
python -m venv venv
```

### 2. Aktifkan Virtual Environment
```bash
# Windows (PowerShell)
.\venv\Scripts\Activate

# Windows (Git Bash)
source venv/Scripts/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server
```bash
uvicorn app.main:app --reload
```
Server akan berjalan di `http://127.0.0.1:8000`  
Dokumentasi API otomatis tersedia di `http://127.0.0.1:8000/docs`

### 5. Jalankan Unit Testing
```bash
pytest test/ -v
```

---

## 📋 Implementasi Aspek Tugas

Berikut penjelasan detail implementasi setiap aspek arahan tugas beserta lokasi file dan baris kode spesifik.

---

### 1. CRUD — Input, Edit, Hapus, Tampilkan Data Mahasiswa

Seluruh operasi CRUD diimplementasikan sebagai endpoint REST API di file **`app/main.py`**.

| Operasi | Method | Endpoint | File | Baris |
|---------|--------|----------|------|-------|
| **Create** (Input) | `POST` | `/mahasiswa` | `main.py` | Baris 50–57 |
| **Read** (Tampilkan semua) | `GET` | `/mahasiswa` | `main.py` | Baris 59–61 |
| **Update** (Edit) | `PUT` | `/mahasiswa/{nim}` | `main.py` | Baris 85–96 |
| **Delete** (Hapus) | `DELETE` | `/mahasiswa/{nim}` | `main.py` | Baris 99–108 |

**Penggunaan Array:**  
Data mahasiswa disimpan dalam bentuk **list (array)** Python. Operasi seperti `append()`, `enumerate()`, dan *list comprehension* digunakan untuk manipulasi data.

- **`main.py` baris 55** — `data.append(mhs.model_dump())` → menambahkan data ke array
- **`main.py` baris 88** — `for i, mhs in enumerate(data)` → iterasi array dengan index
- **`main.py` baris 102** — `new_data = [d for d in data if d['nim'] != nim]` → filter array (list comprehension)

**Penggunaan Fungsi:**  
Setiap endpoint merupakan fungsi Python yang modular dan terpisah sesuai tanggung jawabnya:
- `create_mahasiswa()`, `read_all_mahasiswa()`, `update_mahasiswa()`, `delete_mahasiswa()`

---

### 2. Penyimpanan & Pembacaan Data dari File (File I/O)

Diimplementasikan di file **`app/manager.py`** menggunakan class `JSONManager`.

| Operasi | Method | File | Baris |
|---------|--------|------|-------|
| Baca data mahasiswa | `read_mahasiswa()` | `manager.py` | Baris 12–21 |
| Tulis data mahasiswa | `write_mahasiswa()` | `manager.py` | Baris 23–29 |
| Baca data user | `read_users()` | `manager.py` | Baris 31–36 |
| Tulis data user | `write_users()` | `manager.py` | Baris 38–40 |

**Detail:**
- Menggunakan modul `json` dan `os` bawaan Python
- Data disimpan di 2 file JSON: `data/mahasiswa.json` dan `data/users.json`
- **`manager.py` baris 18–19** — `open(DATA_FILE, "r")` lalu `json.load(f)` untuk membaca
- **`manager.py` baris 26–27** — `open(DATA_FILE, "w")` lalu `json.dump(data, f, indent=4)` untuk menulis

---

### 3. Konsep OOP (Class, Objek, Enkapsulasi, Pewarisan, Polimorfisme)

Diimplementasikan di file **`app/models.py`**.

| Konsep | Implementasi | File | Baris |
|--------|-------------|------|-------|
| **Class & Objek** | `Person`, `Mahasiswa`, `UserCreate`, `UserResponse` | `models.py` | Baris 5, 9, 19, 24 |
| **Enkapsulasi** | Atribut di-encapsulate dalam class `Person` | `models.py` | Baris 5–6 |
| **Pewarisan (Inheritance)** | `Mahasiswa(Person)` — Mahasiswa mewarisi Person | `models.py` | Baris 9 |
| **Polimorfisme** | Method `display_info()` pada Mahasiswa | `models.py` | Baris 16–17 |

**Detail:**
- **`models.py` baris 5–6** — `class Person(BaseModel)` → Base class dengan atribut `nama`
- **`models.py` baris 9** — `class Mahasiswa(Person)` → Inheritance, Mahasiswa mewarisi `nama` dari Person dan menambahkan `nim`, `jurusan`, `kelas`
- **`models.py` baris 16–17** — `def display_info(self)` → Polymorphism, representasi objek Mahasiswa dalam format string

Selain itu, class `JSONManager` di **`manager.py` baris 11** dan class `MahasiswaAlgo` di **`algorithms.py` baris 3** juga menerapkan konsep OOP dengan penggunaan `@staticmethod`.

---

### 4. Fitur Pencarian Data (Linear Search, Sequential Search & Binary Search)

Diimplementasikan di file **`app/algorithms.py`** dalam class `MahasiswaAlgo`.

| Algoritma | Method | File | Baris | Time Complexity |
|-----------|--------|------|-------|----------------|
| **Linear Search** | `linear_search()` | `algorithms.py` | Baris 30–36 | **O(n)** |
| **Sequential Search** | `sequential_search()` | `algorithms.py` | Baris 38–49 | **O(n)** |
| **Binary Search** | `binary_search()` | `algorithms.py` | Baris 52–68 | **O(n²)** * |

> \* Binary Search sendiri O(log n), namun karena data perlu di-sort terlebih dahulu menggunakan Selection Sort O(n²), maka total complexity menjadi O(n²). Proses sort dilakukan di **baris 56**.

**Perbedaan ketiga algoritma:**
| Algoritma | Cara Kerja | Input | Output |
|-----------|-----------|-------|--------|
| **Linear Search** | Exact match berdasarkan NIM | NIM (exact) | 1 mahasiswa atau `null` |
| **Sequential Search** | Partial match keyword di semua field (nama, nim, jurusan, kelas) | Keyword (bebas) | List mahasiswa yang cocok |
| **Binary Search** | Data di-sort dulu, lalu divide & conquer | NIM (exact) | 1 mahasiswa atau `null` |

**Endpoint API:**
- `GET /mahasiswa/search?nim={nim}&method=linear|binary` → Linear/Binary Search (**`main.py` baris 64–75**)
- `GET /mahasiswa/sequential-search?keyword={keyword}` → Sequential Search (**`main.py` baris 77–83**)

**Detail:**
- **`algorithms.py` baris 31–36** — Linear Search: Iterasi satu per satu elemen array, cocokkan NIM secara exact
- **`algorithms.py` baris 39–49** — Sequential Search: Iterasi semua elemen, cek apakah keyword cocok di field `nama`, `nim`, `jurusan`, atau `kelas` (case-insensitive, partial match)
- **`algorithms.py` baris 53–68** — Binary Search: Data di-sort dulu (baris 56), lalu membagi array menjadi dua bagian secara berulang

---

### 5. Fitur Pengurutan Data (Insertion Sort & Selection Sort)

Diimplementasikan di file **`app/algorithms.py`** dalam class `MahasiswaAlgo`.

| Algoritma | Method | File | Baris | Time Complexity |
|-----------|--------|------|-------|----------------|
| **Insertion Sort** | `insertion_sort()` | `algorithms.py` | Baris 5–15 | **O(n²)** |
| **Selection Sort** | `selection_sort()` | `algorithms.py` | Baris 18–28 | **O(n²)** |

**Endpoint API:** `GET /mahasiswa/sort?method=insertion|selection&key=nim|nama|jurusan|kelas`  
Diakses melalui **`main.py` baris 77–82**.

**Detail:**
- **`algorithms.py` baris 6–15** — Insertion Sort: Mengambil elemen satu per satu dan menyisipkannya ke posisi yang tepat dalam bagian array yang sudah terurut
- **`algorithms.py` baris 19–28** — Selection Sort: Mencari elemen terkecil dari bagian yang belum terurut, lalu menukarnya dengan posisi paling depan
- Sorting bisa dilakukan berdasarkan key apapun (`nim`, `nama`, `jurusan`, `kelas`) melalui parameter `key`

---

### 6. Validasi Input Menggunakan Regular Expression (Regex)

Diimplementasikan di file **`app/models.py`** menggunakan Pydantic `Field(pattern=...)`.

| Validasi | Pattern Regex | File | Baris |
|----------|--------------|------|-------|
| NIM harus 12 digit angka | `^\d{12}$` | `models.py` | Baris 11 |
| Role hanya boleh `dosen` atau `aslab` | `^(dosen\|aslab)$` | `models.py` | Baris 22 |

**Detail:**
- **`models.py` baris 11** — `nim: str = Field(..., pattern=r"^\d{12}$")` → NIM harus tepat 12 digit angka (contoh: `241011450401`)
- **`models.py` baris 22** — `role: str = Field(..., pattern="^(dosen|aslab)$")` → Role user hanya boleh `dosen` atau `aslab`
- Jika input tidak sesuai pattern regex, Pydantic akan otomatis menolak request dengan HTTP 422 (Validation Error)

---

### 7. Penanganan Error Menggunakan Try–Catch & Exception

Diimplementasikan di beberapa file.

| Penanganan | File | Baris | Keterangan |
|-----------|------|-------|-----------|
| Error baca file mahasiswa | `manager.py` | Baris 14–21 | Try-catch `JSONDecodeError` & `IOError` |
| Error tulis file mahasiswa | `manager.py` | Baris 25–29 | Try-catch `IOError` |
| Error baca file user | `manager.py` | Baris 33–36 | Try-catch generic `Exception` |
| Error verifikasi password | `auth.py` | Baris 15–18 | Try-catch saat `bcrypt.checkpw()` gagal |
| Error decode token JWT | `auth.py` | Baris 38–44 | Try-catch `jwt.PyJWTError` |
| NIM sudah terdaftar | `main.py` | Baris 53–54 | Raise `HTTPException(400)` |
| NIM tidak ditemukan | `main.py` | Baris 96, 104–105 | Raise `HTTPException(404)` |
| Akses ditolak (RBAC) | `auth.py` | Baris 52–57 | Raise `HTTPException(403)` |
| Login gagal | `main.py` | Baris 18–19 | Raise `HTTPException(400)` |

**Detail:**
- **`manager.py` baris 14–21** — Contoh try-catch utama:
  ```python
  try:
      with open(DATA_FILE, "r") as f:
          return json.load(f)
  except (json.JSONDecodeError, IOError) as e:
      raise HTTPException(status_code=500, detail=f"Gagal membaca database: {str(e)}")
  ```
- FastAPI secara otomatis menangani exception `HTTPException` dan mengembalikan response error JSON yang sesuai ke client

---

### 8. Estimasi Time Complexity

| Fitur | Algoritma | Time Complexity | Lokasi |
|-------|-----------|----------------|--------|
| Insertion Sort | Nested loop (while inside for) | **O(n²)** | `algorithms.py` baris 6–15 |
| Selection Sort | Nested loop (for inside for) | **O(n²)** | `algorithms.py` baris 19–28 |
| Linear Search | Single loop | **O(n)** | `algorithms.py` baris 31–36 |
| Sequential Search | Single loop + partial match | **O(n)** | `algorithms.py` baris 39–49 |
| Binary Search | Divide & conquer (halving) | **O(log n)** | `algorithms.py` baris 53–68 |
| Create Mahasiswa | Array append + linear scan | **O(n)** | `main.py` baris 51–57 |
| Update Mahasiswa | Linear scan + enumerate | **O(n)** | `main.py` baris 86–96 |
| Delete Mahasiswa | List comprehension (filter) | **O(n)** | `main.py` baris 100–108 |
| Login (cari user) | Generator expression with `next()` | **O(n)** | `main.py` baris 16 |

---

### 9. Guidelines & Best Practices

#### Penamaan Variabel
- Menggunakan **snake_case** sesuai konvensi Python (contoh: `access_token`, `current_user`, `min_idx`)
- Nama variabel deskriptif dan bermakna (contoh: `sorted_data`, `credentials_exception`, `mhs_update`)
- Konstanta menggunakan **UPPER_CASE** (contoh: `SECRET_KEY`, `ALGORITHM`, `DATA_FILE`)

#### Modularisasi Kode
Kode dipisah menjadi **5 modul** sesuai tanggung jawab (Single Responsibility):

| Modul | Tanggung Jawab |
|-------|----------------|
| `main.py` | Routing & endpoint API |
| `models.py` | Definisi data model (Pydantic/OOP) |
| `auth.py` | Autentikasi, JWT, password hashing, RBAC |
| `algorithms.py` | Algoritma sorting & searching |
| `manager.py` | File I/O (baca/tulis JSON) |

#### Komentar
Setiap bagian kode diberi komentar penjelasan:
- **`models.py`** — Komentar konsep OOP di setiap class (`# KONSEP OOP: Inheritance`, `# KONSEP OOP: Polymorphism`)
- **`algorithms.py`** — Komentar nama algoritma dan complexity (`# 1. INSERTION SORT (O(n^2))`)
- **`main.py`** — Section header dengan separator (`# ==========================================`)
- **`manager.py`** — Komentar penanganan error (`# TRY-CATCH: Penanganan error file`)

---

## 🌟 Added Value: Sistem Penilaian Praktikum Otomatis (Timer & Ceklis)

Sebagai nilai tambah yang menunjukkan **kreativitas dalam pengembangan software**, project ini tidak hanya berisi manajemen data mahasiswa biasa, melainkan diintegrasikan dengan **Sistem Penilaian Praktikum / Assignment**. 

**Latar Belakang Masalah:** 
Biasanya, aslab atau dosen mencatat pengerjaan tugas (modul) secara manual di kertas (siapa yang cepat selesai, siapa yang mengerjakan tugas tambahan). Hal ini berisiko hilang, *human error*, atau manipulasi waktu. 

**Solusi & Konsep Fitur:**
Sistem ini menyediakan endpoint *Timer* dan *Penilaian* murni dari sisi backend untuk menjamin keakuratan data:
1. **Dosen membuka sesi pertemuan:** Dosen/Aslab membuat record pertemuan (`POST /pertemuan`). Sistem **otomatis merekam waktu server** sebagai titik mulai (`waktu_mulai`).
2. **Mahasiswa Mengerjakan Tugas:** Waktu terus berjalan secara independen.
3. **Dosen mensubmit nilai mahasiswa:** Saat mahasiswa menyetor tugas, Aslab langsung menembak API (`POST /pertemuan/{id}/nilai`) dengan memasukkan NIM dan nilai tugas (ceklis). 
4. **Kalkulasi Durasi Otomatis:** Sistem langsung merekam waktu saat API ditembak (`waktu_selesai`), menghitung selisihnya dengan `waktu_mulai`, dan menyimpan **`durasi_menit` pengerjaan yang 100% akurat dan tamper-proof**.

**Detail Implementasi:**
- **File & Model:** `models.py` baris 26–45 (Model `Pertemuan` dan `Penilaian`), `manager.py` (File I/O ke `pertemuan.json` dan `penilaian.json`).
- **Endpoint API:** `main.py` baris 120–190 (Endpoint khusus untuk flow timer dan penilaian).
- **Time/Datetime Logic:** Menggunakan fungsi `datetime.now()` bawaan Python untuk merekam *timestamp* saat API dipanggil dan `total_seconds()` untuk kalkulasi durasi.

---

## 🔐 Sistem Autentikasi & RBAC

Backend ini dilengkapi sistem keamanan:

### Autentikasi (JWT)
- Login via `POST /login` menghasilkan **JWT access token** (expired 60 menit)
- Setiap request ke endpoint yang dilindungi harus menyertakan header `Authorization: Bearer <token>`
- Implementasi di **`auth.py` baris 25–30** (create token) dan **baris 32–50** (verify token)

### Role-Based Access Control (RBAC)
| Role | Akses |
|------|-------|
| **Dosen** | Semua fitur (CRUD Mahasiswa + CRUD User) |
| **Aslab** | Hanya CRUD Mahasiswa |

- Middleware RBAC di **`auth.py` baris 52–58** (`require_dosen()`)
- Endpoint `/users` dilindungi dengan `dependencies=[Depends(require_dosen)]` di **`main.py` baris 27, 42**

---

## 🧪 Unit Testing

File: **`test/test_api.py`** — 5 skenario test menggunakan `pytest` + FastAPI `TestClient`.

| No | Test | Deskripsi | Baris |
|----|------|-----------|-------|
| 1 | `test_login_success` | Login berhasil, dapat token JWT | Baris 40–45 |
| 2 | `test_login_failed` | Login gagal dengan password salah | Baris 47–50 |
| 3 | `test_create_mahasiswa_with_auth` | CRUD Create mahasiswa dengan token Dosen | Baris 52–66 |
| 4 | `test_rbac_aslab_cannot_access_users` | RBAC: Aslab ditolak akses endpoint `/users` | Baris 68–77 |
| 5 | `test_search_mahasiswa` | Algoritma search (Linear) via API | Baris 79–92 |

**Setup/Teardown** (baris 20–34): Menggunakan `@pytest.fixture(autouse=True)` untuk membuat database dummy sebelum test dan menghapusnya setelah test selesai.

---

## 📡 Daftar Endpoint API

| Method | Endpoint | Deskripsi | Auth | Role |
|--------|----------|-----------|------|------|
| `POST` | `/login` | Login & dapatkan JWT token | ❌ | — |
| `POST` | `/users` | Buat user baru | ✅ | Dosen |
| `GET` | `/users` | Lihat semua user | ✅ | Dosen |
| `POST` | `/mahasiswa` | Tambah mahasiswa baru | ✅ | Semua |
| `GET` | `/mahasiswa` | Lihat semua mahasiswa | ✅ | Semua |
| `GET` | `/mahasiswa/search` | Cari mahasiswa (Linear/Binary) | ✅ | Semua |
| `GET` | `/mahasiswa/sequential-search` | Cari mahasiswa (Sequential/Keyword) | ✅ | Semua |
| `GET` | `/mahasiswa/sort` | Urutkan mahasiswa (Insertion/Selection) | ✅ | Semua |
| `PUT` | `/mahasiswa/{nim}` | Update data mahasiswa | ✅ | Semua |
| `DELETE` | `/mahasiswa/{nim}` | Hapus mahasiswa | ✅ | Semua |
| `POST` | `/pertemuan` | Buat sesi pertemuan baru (start timer) | ✅ | Dosen/Aslab |
| `GET` | `/pertemuan` | Lihat daftar pertemuan | ✅ | Dosen/Aslab |
| `PUT` | `/pertemuan/{id}/tutup` | Tutup sesi pertemuan (stop) | ✅ | Dosen/Aslab |
| `POST` | `/pertemuan/{id}/nilai` | Input nilai ceklis mahasiswa & catat waktu kumpul | ✅ | Dosen/Aslab |
| `GET` | `/pertemuan/{id}/nilai` | Lihat semua nilai di pertemuan tertentu | ✅ | Dosen/Aslab |

---

## 📦 Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Framework | FastAPI 0.137.0 |
| Runtime | Python 3.13 |
| Autentikasi | PyJWT 2.13.0 + bcrypt 5.0.0 |
| Validasi | Pydantic 2.13.4 |
| Server | Uvicorn 0.49.0 |
| Testing | Pytest 9.1.0 |
| Database | JSON File (File I/O) |
