"""Seed the default admin user. Run once after DB migrations."""
import sys
from pathlib import Path

# Add backend to path so we can import app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def seed_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("Admin user already exists, skipping.")
            return
        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
        )
        db.add(admin)
        db.commit()
        print("Admin user created: username=admin, password=admin123")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()