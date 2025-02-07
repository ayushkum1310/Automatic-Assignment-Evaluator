import bcrypt
import jwt
import os
import random
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from src.Logging import logging
import aiosmtplib
from email.mime.text import MIMEText

load_dotenv()

# Config
MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Database Connection
db_client = AsyncIOMotorClient(MONGO_URI)
db = db_client["Major-Project"]  # Use the correct database name
users_collection = db["login_details"]  # Correct collection for user authentication
otp_collection = db["otps"]

logger = logging.getLogger("uvicorn")

class AuthController:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def create_jwt(email: str) -> str:
        payload = {"sub": email, "exp": datetime.utcnow() + timedelta(days=1)}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    async def get_user(email: str):
        return await users_collection.find_one({"email": email})

    @staticmethod
    async def save_otp(email: str, otp: str):
        await otp_collection.insert_one({
            "email": email, "otp": otp, "expires": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        })

    @staticmethod
    async def send_email(to_email: str, otp: str):
        msg = MIMEText(f"Your OTP for signup is: {otp}")
        msg["Subject"] = "Signup OTP Verification"
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email
        print(EMAIL_SENDER, EMAIL_PASSWORD)

        try:
            await aiosmtplib.send(
                msg,
                hostname="smtp.gmail.com",
                port=465,
                username=EMAIL_SENDER,
                password=EMAIL_PASSWORD,
                use_tls=True,
            )
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    @staticmethod
    async def verify_otp(email: str, otp: str):
        otp_record = await otp_collection.find_one({"email": email, "otp": otp})
        if otp_record:
            expires = datetime.fromisoformat(otp_record["expires"])
            print(f"Current time: {datetime.utcnow()}")
            print(f"OTP expires at: {expires}")
            if datetime.utcnow() < expires:
                return True
            else:
                print("OTP has expired.")
        else:
            print("OTP record not found.")
        return False

    @staticmethod
    async def login(email: str, password: str):
        user = await AuthController.get_user(email)
        if not user:
            return {"error": "User not found"}
        if not AuthController.verify_password(password, user["password"]):
            return {"error": "Incorrect password"}
        token = AuthController.create_jwt(email)
        return {"message": "Login successful", "token": token}

    @staticmethod
    async def signup(email: str):
        if await AuthController.get_user(email):
            return {"error": "User already exists"}
        otp = str(random.randint(100000, 999999))
        await AuthController.save_otp(email, otp)
        email_sent = await AuthController.send_email(email, otp)
        if not email_sent:
            return {"error": "Failed to send OTP"}
        return {"message": "OTP sent to your email"}

    @staticmethod
    async def verify_signup(email: str, otp: str, password: str):
        if not await AuthController.verify_otp(email, otp):
            return {"error": "Invalid OTP or expired"}
        hashed_password = AuthController.hash_password(password)
        await users_collection.insert_one({"email": email, "password": hashed_password})
        return {"message": "User registered successfully"}
    
    @staticmethod
    async def dummy(text: str):
        try:
            await otp_collection.insert_one({
                "text": text
            })
        except:
            return {"message": "Error"}
        
    @staticmethod
    async def send_password_reset_otp(email: str):
        user = await AuthController.get_user(email)
        if not user:
            return {"error": "User not found"}

        otp = str(random.randint(100000, 999999))
        await AuthController.save_otp(email, otp)
        email_sent = await AuthController.send_email(email, otp)
        if not email_sent:
            return {"error": "Failed to send OTP"}
        return {"message": "Password reset OTP sent to your email"}

    @staticmethod
    async def reset_password(email: str, otp: str, new_password: str):
        if not await AuthController.verify_otp(email, otp):
            return {"error": "Invalid or expired OTP"}
        
        hashed_password = AuthController.hash_password(new_password)
        result = await users_collection.update_one(
            {"email": email},
            {"$set": {"password": hashed_password}}
        )
        if result.modified_count == 1:
            return {"message": "Password reset successful"}
        else:
            return {"error": "Failed to reset password"}