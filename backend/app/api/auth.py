from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token
from app.api.deps import get_current_user, get_optional_user
from app.auth.oauth import verify_google_token, verify_github_token

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(
        email=payload.email,
        username=payload.username,
        password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access = create_access_token({"sub": user.email})
    refresh = create_refresh_token({"sub": user.email})
    return Token(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=Token)
def refresh(token_data: dict, db: Session = Depends(get_db)):
    from app.auth.jwt import decode_token
    payload = decode_token(token_data.get("refresh_token"))
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access = create_access_token({"sub": user.email})
    refresh = create_refresh_token({"sub": user.email})
    return Token(access_token=access, refresh_token=refresh)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/oauth/google")
async def oauth_google(token: str, db: Session = Depends(get_db)):
    info = await verify_google_token(token)
    email = info.get("email")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, username=email.split("@")[0], password=hash_password("oauth"))
        db.add(user)
        db.commit()
        db.refresh(user)
    access = create_access_token({"sub": user.email})
    refresh = create_refresh_token({"sub": user.email})
    return Token(access_token=access, refresh_token=refresh)


@router.post("/oauth/github")
async def oauth_github(token: str, db: Session = Depends(get_db)):
    info = await verify_github_token(token)
    email = info.get("email") or info.get("login")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, username=info.get("login", email), password=hash_password("oauth"))
        db.add(user)
        db.commit()
        db.refresh(user)
    access = create_access_token({"sub": user.email})
    refresh = create_refresh_token({"sub": user.email})
    return Token(access_token=access, refresh_token=refresh)
