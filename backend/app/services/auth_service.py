from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import User


def create_user(db: Session, *, email: str, password: str, name: str) -> User:
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise ValueError("Email already exists")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        name=name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> tuple[User | None, str | None]:
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(password, user.hashed_password):
        return None, None

    token = create_access_token(user.id)
    return user, token
