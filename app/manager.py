"""
app/manager.py — Database Interaction Manager

Modul ini membungkus semua operasi logika database (CRUD) ke dalam
metode-metode statis. Menggunakan pendekatan Repositori Pattern untuk
memisahkan logika kueri SQLAlchemy dari logika rute (routing/endpoint).
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from .db_models import UserDB, MahasiswaDB, PertemuanDB, PenilaianDB


class DatabaseManager:
    """
    Helper class untuk operasi database umum.
    Setiap method menerima SQLAlchemy Session sebagai parameter.
    """

    # ── USER ────────────────────────────────────────────────────────────────

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(UserDB).filter(UserDB.username == username).first()

    @staticmethod
    def get_all_users(db: Session):
        return db.query(UserDB).all()

    @staticmethod
    def create_user(db: Session, username: str, hashed_password: str, role: str) -> UserDB:
        user = UserDB(username=username, password=hashed_password, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, username: str) -> bool:
        user = db.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True

    # ── MAHASISWA ───────────────────────────────────────────────────────────

    @staticmethod
    def get_all_mahasiswa(db: Session, kelas: str = None):
        query = db.query(MahasiswaDB)
        if kelas:
            query = query.filter(MahasiswaDB.kelas == kelas)
        return query.all()

    @staticmethod
    def get_mahasiswa_by_nim(db: Session, nim: str):
        return db.query(MahasiswaDB).filter(MahasiswaDB.nim == nim).first()

    @staticmethod
    def create_mahasiswa(db: Session, nim: str, nama: str, jurusan: str, kelas: str) -> MahasiswaDB:
        mhs = MahasiswaDB(nim=nim, nama=nama, jurusan=jurusan, kelas=kelas)
        db.add(mhs)
        db.commit()
        db.refresh(mhs)
        return mhs

    @staticmethod
    def update_mahasiswa(db: Session, nim: str, data: dict) -> MahasiswaDB:
        mhs = db.query(MahasiswaDB).filter(MahasiswaDB.nim == nim).first()
        if not mhs:
            return None
        for key, value in data.items():
            setattr(mhs, key, value)
        db.commit()
        db.refresh(mhs)
        return mhs

    @staticmethod
    def delete_mahasiswa(db: Session, nim: str) -> bool:
        mhs = db.query(MahasiswaDB).filter(MahasiswaDB.nim == nim).first()
        if not mhs:
            return False
        db.delete(mhs)
        db.commit()
        return True

    @staticmethod
    def get_distinct_kelas(db: Session) -> list[str]:
        """Ambil daftar kelas unik dari data mahasiswa."""
        rows = db.query(MahasiswaDB.kelas).distinct().all()
        return sorted([r[0] for r in rows])

    # ── PERTEMUAN ───────────────────────────────────────────────────────────

    @staticmethod
    def get_all_pertemuan(db: Session, kelas: str = None):
        query = db.query(PertemuanDB).order_by(PertemuanDB.id.desc())
        if kelas:
            query = query.filter(PertemuanDB.kelas == kelas)
        return query.all()

    @staticmethod
    def get_pertemuan_by_id(db: Session, id: int):
        return db.query(PertemuanDB).filter(PertemuanDB.id == id).first()

    @staticmethod
    def create_pertemuan(db: Session, topik: str, kelas: str) -> PertemuanDB:
        from datetime import datetime
        p = PertemuanDB(topik=topik, kelas=kelas, waktu_mulai=datetime.now(), status="aktif")
        db.add(p)
        db.commit()
        db.refresh(p)
        return p

    @staticmethod
    def tutup_pertemuan(db: Session, id: int) -> PertemuanDB:
        from datetime import datetime
        p = db.query(PertemuanDB).filter(PertemuanDB.id == id).first()
        if not p:
            return None
        p.status = "selesai"
        p.waktu_selesai = datetime.now()
        db.commit()
        db.refresh(p)
        return p

    # ── PENILAIAN ───────────────────────────────────────────────────────────

    @staticmethod
    def get_penilaian_by_pertemuan(db: Session, pertemuan_id: int):
        return db.query(PenilaianDB).filter(PenilaianDB.pertemuan_id == pertemuan_id).all()

    @staticmethod
    def create_penilaian(db: Session, pertemuan_id: int, nim: str,
                         ceklis: int, waktu_selesai, durasi_menit: float) -> PenilaianDB:
        nilai = PenilaianDB(
            pertemuan_id=pertemuan_id,
            nim=nim,
            ceklis=ceklis,
            waktu_selesai=waktu_selesai,
            durasi_menit=durasi_menit,
        )
        db.add(nilai)
        db.commit()
        db.refresh(nilai)
        return nilai

    @staticmethod
    def get_top_mahasiswa(db: Session, limit: int = 10):
        from sqlalchemy import func
        results = db.query(
            MahasiswaDB.nim,
            MahasiswaDB.nama,
            MahasiswaDB.kelas,
            func.sum(PenilaianDB.ceklis).label('total_rating')
        ).join(PenilaianDB, MahasiswaDB.nim == PenilaianDB.nim)\
         .group_by(MahasiswaDB.nim, MahasiswaDB.nama, MahasiswaDB.kelas)\
         .order_by(func.sum(PenilaianDB.ceklis).desc())\
         .limit(limit).all()

        return [
            {
                "nim": r.nim,
                "nama": r.nama,
                "kelas": r.kelas,
                "total_rating": r.total_rating
            }
            for r in results
        ]