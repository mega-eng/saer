from __future__ import annotations

import csv
import hashlib
import time
from pathlib import Path
from typing import Generator

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, create_engine, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from backend.app.config import DB_DIR, DB_PATH, IMAGES_CSV, LISTINGS_CSV, ROOT


class Base(DeclarativeBase):
    pass


class Listing(Base):
    __tablename__ = "listings"

    uid: Mapped[str] = mapped_column(String, primary_key=True)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    make: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    model: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    model_std: Mapped[str | None] = mapped_column(String, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    condition: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    mileage: Mapped[float | None] = mapped_column(Float, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    transmission: Mapped[str | None] = mapped_column(String, nullable=True)
    fuel: Mapped[str | None] = mapped_column(String, nullable=True)
    trim: Mapped[str | None] = mapped_column(String, nullable=True)
    trim_std: Mapped[str | None] = mapped_column(String, nullable=True)
    body: Mapped[str | None] = mapped_column(String, nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
    listing_date: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    usable_price: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    image_count: Mapped[int] = mapped_column(Integer, default=0)


class ImageAsset(Base):
    __tablename__ = "images"

    image_uid: Mapped[str] = mapped_column(String, primary_key=True)
    listing_uid: Mapped[str] = mapped_column(ForeignKey("listings.uid"), index=True)
    relative_path: Mapped[str] = mapped_column(String)
    sha256: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    image_kind: Mapped[str | None] = mapped_column(String, nullable=True)
    valid: Mapped[bool] = mapped_column(Boolean, default=False)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)


class DatasetMeta(Base):
    __tablename__ = "dataset_meta"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String)


class AuthUser(Base):
    __tablename__ = "auth_users"

    user_id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[float] = mapped_column(Float, default=time.time)


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    token_hash: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("auth_users.user_id"), index=True)
    expires_at: Mapped[float] = mapped_column(Float, index=True)


DB_DIR.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _bool(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"true", "1", "yes"}


def _int(value: str | None) -> int | None:
    try:
        return int(float(value)) if value not in (None, "") else None
    except (TypeError, ValueError, OverflowError):
        return None


def _float(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError, OverflowError):
        return None


def _fingerprint() -> str:
    digest = hashlib.sha256()
    for path in (LISTINGS_CSV, IMAGES_CSV):
        if not path.is_file():
            raise FileNotFoundError(f"ملف بيانات المشروع غير موجود: {path}")
        with path.open("rb") as file:
            for block in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(block)
    return digest.hexdigest()


def ensure_database() -> dict[str, int | bool]:
    """يبني نسخة SQLite محلية من ملفات processed دون تعديلها."""
    Base.metadata.create_all(engine)
    source_hash = _fingerprint()
    with SessionLocal() as session:
        prior = session.get(DatasetMeta, "source_sha256")
        listings_count = session.scalar(select(Listing.uid).limit(1))
        if prior and prior.value == source_hash and listings_count:
            return {
                "rebuilt": False,
                "listings": session.query(Listing).count(),
                "images": session.query(ImageAsset).count(),
            }

        session.execute(delete(ImageAsset))
        session.execute(delete(Listing))
        listing_rows: list[Listing] = []
        with LISTINGS_CSV.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                uid = row.get("listing_uid") or ""
                if not uid:
                    continue
                listing_rows.append(Listing(
                    uid=uid,
                    source=row.get("source_dataset") or None,
                    make=row.get("make") or None,
                    model=row.get("model") or None,
                    model_std=row.get("model_std") or None,
                    year=_int(row.get("year")),
                    condition=row.get("condition") or None,
                    price=_float(row.get("sar_price")),
                    mileage=_float(row.get("km_mileage")),
                    city=row.get("city") or None,
                    transmission=row.get("transmission") or None,
                    fuel=row.get("type_fuel") or None,
                    trim=row.get("trim") or None,
                    trim_std=row.get("trim_std") or None,
                    body=row.get("body_type_std") or row.get("body_type") or None,
                    color=row.get("color_std") or row.get("color") or None,
                    listing_date=row.get("listing_date") or None,
                    usable_price=_bool(row.get("usable_price")),
                    image_count=_int(row.get("n_images")) or 0,
                ))
        session.add_all(listing_rows)
        session.flush()

        image_rows: list[ImageAsset] = []
        with IMAGES_CSV.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                listing_uid = row.get("listing_uid") or ""
                path = row.get("relative_path") or ""
                image_uid = row.get("image_uid") or path
                if not listing_uid or not path:
                    continue
                # Keep the source-relative path; file serving separately checks its root.
                image_rows.append(ImageAsset(
                    image_uid=image_uid,
                    listing_uid=listing_uid,
                    relative_path=path,
                    sha256=row.get("sha256") or None,
                    image_kind=row.get("image_kind") or None,
                    valid=_bool(row.get("is_valid")) and (ROOT / Path(path)).is_file(),
                    width=_int(row.get("width")),
                    height=_int(row.get("height")),
                ))
        session.add_all(image_rows)
        session.merge(DatasetMeta(key="source_sha256", value=source_hash))
        session.commit()
        return {"rebuilt": True, "listings": len(listing_rows), "images": len(image_rows)}


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
