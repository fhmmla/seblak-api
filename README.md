# 🍜 SEBLAK API (Sistem Evaluasi Belajar Lab Akademik & Kelas)

**Nama:** Fahmi Maulana Fadila  
**NIM:** 241011450401  
**Kelas:** 03TPLE005  
**Mata Kuliah:** Algoritma Dan Pemrograman II  
**Jenis Ujian:** UAS  

---

## 📖 Tentang Project

**SEBLAK (Sistem Evaluasi Belajar Lab Akademik & Kelas)** adalah **Backend REST API** untuk aplikasi Manajemen Data Mahasiswa terpadu yang dibangun menggunakan **FastAPI (Python)**. Selain menyediakan layanan CRUD mahasiswa, SEBLAK berinovasi dengan fitur **Penilaian Praktikum Otomatis** (Timer & Ceklis), autentikasi JWT, *role-based access control* (RBAC), serta terhubung ke database **PostgreSQL (Supabase)**. 

Project ini dirancang sedemikian rupa untuk memenuhi semua kriteria dan arahan tugas UAS mata kuliah Algoritma dan Pemrograman II, termasuk penerapan konsep algoritma (Searching, Sorting) dan Pemrograman Berorientasi Objek (OOP).

🔗 **Repository:** [https://github.com/fhmmla/seblak-api](https://github.com/fhmmla/seblak-api)  
🌍 **Live Demo Frontend:** [https://seblak-pedas.vercel.app/](https://seblak-pedas.vercel.app/)  
⚙️ **Live API Backend:** [https://seblak-api.onrender.com/](https://seblak-api.onrender.com/)  
⚖️ **Lisensi:** MIT License

> **Catatan:** Project ini berfokus pada sisi **Backend (API)**.

---

## 🏗️ Struktur Project

```
Sourecode/
├── app/
│   ├── main.py          # Entry point API, definisi endpoint RESTful
│   ├── models.py        # Pydantic schemas (Validasi Regex, OOP: Base Class)
│   ├── db_models.py     # SQLAlchemy ORM Models (Definisi skema database relasional)
│   ├── database.py      # Konfigurasi koneksi PostgreSQL & Dependency Injection Session
│   ├── auth.py          # Keamanan: Autentikasi JWT, bcrypt password hashing, RBAC
│   ├── algorithms.py    # Modul Algoritma: Sorting & Searching
│   └── manager.py       # Interaksi terstruktur antara API dan Database (CRUD Logic)
├── data/
│   └── mahasiswa.json   # JSON file untuk Data Seeding (File I/O Requirement)
├── test/
│   └── test_api.py      # Unit Testing terotomatisasi (Pytest)
├── .env                 # Konfigurasi environment variables (Database URL, Secret Key)
├── requirements.txt     # Daftar dependensi library
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

### 4. Konfigurasi Environment (File I/O & Config)
Buat file `.env` di dalam folder `Sourecode/` dan isi dengan detail koneksi database PostgreSQL (Supabase):
```env
user=postgres.xyzxyzyxyzcqhwyvcjketfg
password=password_anda
host=aws-1-ap-southeast-1.pooler.supabase.com
port=5432
dbname=postgres
SECRET_KEY=kunci_rahasia_jwt
DEFAULT_ADMIN_USERNAME=dosen_alpro
DEFAULT_ADMIN_PASSWORD=secret
```

### 5. Jalankan Server
```bash
uvicorn app.main:app --reload
```
- Server berjalan di: `http://127.0.0.1:8000`
- Dokumentasi Interaktif (Swagger UI): `http://127.0.0.1:8000/docs`

> Saat server pertama kali berjalan, sistem akan secara otomatis membuat tabel di database dan melakukan **seeding** data menggunakan file `mahasiswa.json`.

---

## 📋 Pemenuhan Kriteria Arahan Tugas (UAS)

Berikut adalah pemetaan implementasi kode terhadap kriteria yang diminta oleh tugas Algoritma dan Pemrograman II.

### 1. CRUD (Input, Edit, Hapus, Tampilkan)
Beroperasi pada data mahasiswa, didesain menggunakan arsitektur REST API. Pemenuhan kriteria teknis algoritma dasar diwujudkan sebagai berikut:
- **Fungsi (`def`)**: Seluruh operasi CRUD dipecah menjadi fungsi-fungsi modular (misal: `create_mahasiswa()`, `get_all_mahasiswa()`).
- **Array (`List`)**: Di Python, struktur data array diimplementasikan menggunakan tipe data `List` (`[]`). Data mahasiswa dikumpulkan ke dalam list memori ini sebelum dirender atau dimanipulasi.
- **Pointer (Object Reference)**: Meskipun Python tidak memiliki *syntax pointer* eksplisit (`*ptr`) seperti C/C++, variabel di Python bekerja berdasarkan konsep **Pass-by-Object-Reference**. Setiap pemanggilan data (misal saat proses iterasi atau *sorting*) sejatinya me-referensikan alamat memori (*pointer*) dari objek yang sama tanpa menduplikasi data aslinya.

| Operasi | Endpoint API | File Modul | Lokasi Implementasi |
|---------|--------------|------------|---------------------|
| **Create** | `POST /mahasiswa` | `main.py` | Fungsi `create_mahasiswa()` memvalidasi data dan menggunakan session database untuk `add()` |
| **Read** | `GET /mahasiswa` | `main.py` | Mengembalikan representasi array (list) dari objek database. |
| **Update** | `PUT /mahasiswa/{nim}` | `main.py` | Pencarian instan menggunakan referensi Primary Key, dilanjutkan modifikasi atribut. |
| **Delete** | `DELETE /mahasiswa/{nim}` | `main.py` | Penghapusan persisten dari memori dan database. |

### 2. Penyimpanan dan Pembacaan Data dari File (File I/O)
Penyimpanan utama menggunakan **PostgreSQL (Supabase)** agar data terjamin persisten. Namun, kriteria **File I/O (Read & Write)** tetap diwujudkan secara utuh melalui mekanisme berikut:
- **Read I/O (Data Seeding)**: Saat startup, program membaca file `data/mahasiswa.json` (menggunakan fungsi `open(..., "r")` dan `json.load()`) untuk mentransformasikannya menjadi objek database (Inisialisasi tabel).
- **Write I/O (Data Export/Backup)**: Tersedia endpoint `GET /export-backup` yang mengambil snapshot data dari PostgreSQL, menyimpannya (menggunakan `open(..., "w")` dan `json.dump()`) ke file fisik `data/backup.json` di server, serta **mengembalikan data tersebut ke klien** agar otomatis memicu file unduhan di *browser* (klien dapat mendownload `seblak_backup_{tanggal}.json`).

### 3. Penerapan Konsep OOP (Object-Oriented Programming)
Arsitektur sangat bertumpu pada OOP untuk menjamin modularitas dan keamanan data:

- **Class & Objek**: Penggunaan class ORM (misal: `MahasiswaDB`) di `db_models.py` dan class Pydantic (misal: `Mahasiswa`) di `models.py`.
- **Enkapsulasi**: Variabel environment sensitif disembunyikan; field data dibatasi aksesnya melalui property Pydantic.
- **Pewarisan (Inheritance)**: Model Pydantic `Mahasiswa` mewarisi properti dari base class `Person`. Model SQLAlchemy mewarisi `DeclarativeBase`.
- **Polimorfisme**: Metode representasi data yang di-override (misalnya serialisasi dictionary).

### 4. Fitur Pencarian Data (Linear, Sequential, Binary Search)
Algoritma pencarian diterapkan untuk pencarian data mahasiswa (diimplementasikan di `app/algorithms.py`):

> **Estimasi Time Complexity & Pengukuran UI**: Untuk membuktikan kompleksitas waktu ini di dunia nyata, aplikasi dilengkapi dengan indikator **Waktu Eksekusi (⏱️ ms)** pada *Dashboard Frontend*. Indikator ini menghitung waktu `performance.now()` secara *real-time* saat eksekusi algoritma berlangsung!

| Algoritma | Deskripsi | Kompleksitas |
|-----------|-----------|--------------|
| **Linear Search** | Mencari *exact match* NIM dengan iterasi dari awal hingga akhir koleksi. | **O(n)** |
| **Sequential Search** | Melakukan *partial match* lintas atribut (nama, NIM, jurusan, kelas) untuk fitur search bar. | **O(n)** |
| **Binary Search** | Menggunakan prinsip *divide & conquer* setelah data diurutkan (*sorted*) berdasarkan NIM. | **O(log n)** |

### 5. Fitur Pengurutan Data (Insertion & Selection Sort)
Mengurutkan koleksi data mahasiswa berdasarkan parameter fleksibel (NIM, Nama, dll).

> **Estimasi Time Complexity & Pengukuran UI**: Seperti halnya pencarian, durasi eksekusi pengurutan di *backend* akan dihitung secara persisi dan dirender angkanya dalam satuan *milidetik (ms)* pada tabel halaman Dashboard.

| Algoritma | Deskripsi | Kompleksitas |
|-----------|-----------|--------------|
| **Insertion Sort** | Menyisipkan elemen satu persatu pada indeks yang tepat dalam bagian array yang telah diurutkan. | **O(n²)** |
| **Selection Sort** | Mencari nilai minimum secara iteratif dan menukarnya (swap) ke posisi terdepan. | **O(n²)** |

### 6. Validasi Input Menggunakan Regular Expression (Regex)
Regex diimplementasikan di tingkat skema validasi (Pydantic `models.py`) untuk menjaga integritas data sebelum menyentuh database:
- `nim: str = Field(pattern=r"^\d{12}$")` memastikan NIM persis terdiri dari 12 digit numerik.
- `role: str = Field(pattern="^(dosen|aslab)$")` membatasi kewenangan hanya untuk dua tipe spesifik.

### 7. Penanganan Error (Try-Catch & Exception)
Berfokus pada stabilitas server saat menghadapi keadaan anomali:
- **I/O Exception**: `try...except Exception as e` di `main.py` saat membaca JSON seeding.
- **Database Integrity Error**: Menangani duplikasi Primary Key (NIM) atau Foreign Key violation.
- **JWT Decode Error**: Blok `try...except jwt.PyJWTError` di `auth.py` untuk mengamankan API dari token palsu.
- **HTTP Exception**: Standardisasi pengembalian status code error (400 Bad Request, 404 Not Found, 403 Forbidden).

### 8. Guidelines & Best Practices
- **Penamaan Variabel**: Mengikuti pedoman *PEP-8* (snake_case untuk variabel/fungsi, PascalCase untuk Class, UPPER_CASE untuk konstanta).
- **Modularisasi Kode**: Sistem dipisah (Decoupled) antara Routing (`main.py`), Skema Validasi (`models.py`), Model ORM (`db_models.py`), Operasi DB (`manager.py`), dan Algoritma (`algorithms.py`).
- **Komentar (Docstrings)**: Dokumentasi kode profesional yang merinci fungsi modul, tipe argumen, dan logika return, dirancang untuk kolaborasi tim programmer.

---

## 🌟 Inovasi Tambahan: Sistem Penilaian Praktikum Otomatis & Gamifikasi

Sebagai demonstrasi tingkat lanjut, proyek ini dilengkapi dengan subsistem penilaian yang dikembangkan berdasarkan permasalahan nyata di laboratorium:

**Latar Belakang (Permasalahan):**
Sebelumnya, asisten laboratorium harus mencatat waktu penyelesaian tugas secara manual di kertas dan sekadar memberikan tanda *ceklis* bagi mahasiswa yang sudah selesai. Metode ini sangat merepotkan, rentan terhadap *human error* (terutama saat menghitung durasi pengerjaan), dan kurang memberikan apresiasi proporsional bagi mahasiswa yang mengerjakan tugas dengan sangat cepat maupun berkualitas tinggi.

Berangkat dari masalah tersebut, SEBLAK berinovasi dengan merombak sistem *ceklis* manual menjadi **Sistem Rating Bintang (1–5)** dan mengotomatisasi perhitungan *stopwatch* atau durasi. Tidak hanya itu, sistem kini diperkaya dengan elemen **Gamifikasi (Leaderboard)** untuk memacu semangat kompetisi positif antar mahasiswa.

**Fitur Inovasi Utama:**
1. **Manajemen Sesi Otomatis (Smart Timer)**: Dosen membuka pertemuan (`POST /pertemuan`), dan server menandai *timestamp* absolut sebagai titik mula (`waktu_mulai`).
2. **Kalkulasi Waktu Independen**: Saat Aslab men-submit nilai, server mengambil *timestamp* instan (`waktu_selesai`) dan mengkalkulasi `durasi_menit` secara presisi dan *tamper-proof* (tidak bisa diakali dari sisi *frontend* klien).
3. **Sistem Rating Bintang (Evolusi Ceklis)**: Menggantikan ceklis tradisional untuk memberikan rentang apresiasi yang lebih representatif terhadap kualitas kode dan logika mahasiswa.
4. **Dashboard Leaderboard "Top 10 Terbaik"**: Sistem secara otomatis mengagregasi total bintang (rating) yang dikumpulkan setiap mahasiswa dari seluruh pertemuan dan menampilkannya secara *real-time* dalam bentuk klasemen, menciptakan lingkungan belajar yang kompetitif.
5. **Integritas Relasional Kuat**: Penggunaan *Foreign Key* yang ketat antara tabel Pertemuan, Mahasiswa, dan Penilaian memastikan tidak ada data nilai yang yatim-piatu di database.
---

## 🔐 Sistem Keamanan (Security)

### Autentikasi JSON Web Token (JWT)
Seluruh request mutasi (*Create, Update, Delete*) dilindungi dengan header `Authorization: Bearer <token>`.

### Role-Based Access Control (RBAC)
- **Dosen**: Super-user (Akses ke manajemen pengguna & manajemen mahasiswa).
- **Aslab**: User terbatas (Hanya memiliki hak ases pada fitur pencatatan praktikum dan modifikasi mahasiswa).

---

## 📦 Stack Teknologi

| Lapisan (Layer) | Teknologi Utama |
|-----------------|-----------------|
| **Web Framework** | FastAPI (Python 3.13) |
| **ORM & Database** | SQLAlchemy & PostgreSQL (Supabase) |
| **Driver Koneksi** | psycopg (v3) - Dukungan IPv4 & IPv6 via Pooler |
| **Data Validation** | Pydantic |
| **Keamanan Kriptografi** | PyJWT, bcrypt |
