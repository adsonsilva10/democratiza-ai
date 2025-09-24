from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services.auth_service import create_user, authenticate_user
from app.schemas import UserCreate, UserOut, Token

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    token = authenticate_user(db=db, username=user.username, password=user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token