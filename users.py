import os
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, constr
from usersdb import create_user, check_user_by_email, get_user_by_id
from auth import create_access_token, create_refresh_token
import bcrypt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "ritamg@lambdatest.com")
SMTP_PASS = os.getenv("SMTP_PASS", "lvbz gsow elov jjtd")
FROM_EMAIL = SMTP_USER  # or any verified from address

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key")  # Use env var in prod
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour expiration for access token

security = HTTPBearer()

class UserSignup(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

@router.post("/signup")
async def signup(user: UserSignup):
    print("Hi")
    existing_users = await check_user_by_email(user.email)
    if existing_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with given email already exists"
        )
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    await create_user(user.username, user.email, hashed_password, role="user")
    print("Done")

    # Send welcome email (async handling can be improved)
    subject = "Welcome to Our App!"
    body = f"Hi {user.username},\n\nThank you for signing up."
    try:
        send_email("ritamganguliac@gmail.com", subject, body)
    except Exception as e:
        # Log error or ignore based on your preference
        print(f"Failed to send signup email: {e}")

    return {"message": "User created successfully"}


@router.post("/login")
async def login(user: UserLogin):
    user_rows = await check_user_by_email(user.email)
    if not user_rows:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    db_user = user_rows[0]
    if not bcrypt.checkpw(user.password.encode(), db_user['password'].encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    user_data = {
        "user_id": db_user['id'],
        "email": db_user['email'],
        "role": db_user['role']
    }
    # Add expiration to tokens here or inside your create_access_token function
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return {"access_token": access_token, "refresh_token": refresh_token}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def require_roles(*allowed_roles):
    def role_checker(payload: dict = Depends(verify_token)):
        user_role = payload.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return payload
    return role_checker

@router.get("/me")
async def get_current_user(payload: dict = Depends(verify_token)):
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token payload")
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["username"], "email": user["email"], "role": user["role"]}

@router.get("/admin-area")
async def admin_area(payload: dict = Depends(require_roles("admin"))):
    return {"message": "Welcome Admin!"}

@router.get("/manage-users")
async def manage_users(payload: dict = Depends(require_roles("admin", "manager"))):
    return {"message": "Welcome Manager or Admin!"}
