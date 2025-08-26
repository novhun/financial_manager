from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from .. import schemas, crud, dependencies
from ..database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter(prefix="/auth", tags=["auth"])

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user or user.deleted_at:
        return False
    if not crud.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token", response_model=schemas.Token, summary="Login to get access token", description="Authenticate with username and password to receive a JWT token.")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forget", response_model=dict, summary="Request password reset", description="Request a password reset token, sent via email to the registered address.")
async def forget_password(reset: schemas.ResetTokenCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, reset.email)
    if not user or user.deleted_at:
        raise HTTPException(status_code=404, detail="User not found")
    token = crud.create_reset_token(db, user.id)
    
    msg = MIMEText(f"Use this token to reset your password: {token}\nIt expires in 1 hour.")
    msg['Subject'] = "Password Reset Request"
    msg['From'] = os.getenv("MAIL_FROM")
    msg['To'] = user.email

    try:
        with smtplib.SMTP(os.getenv("MAIL_SERVER"), int(os.getenv("MAIL_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    
    return {"message": "Password reset email sent"}

@router.post("/reset", response_model=dict, summary="Reset password", description="Reset password using the token received via email.")
def reset_password(reset: schemas.ResetPassword, db: Session = Depends(get_db)):
    db_token = crud.get_reset_token(db, reset.token)
    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = crud.get_user(db, db_token.user_id)
    if not user or user.deleted_at:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = crud.get_password_hash(reset.new_password)
    db.commit()
    crud.delete_reset_token(db, reset.token)
    return {"message": "Password reset successful"}