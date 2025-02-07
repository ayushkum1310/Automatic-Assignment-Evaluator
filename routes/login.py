from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from controller.login import AuthController

login_router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    email: EmailStr

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
    password: str
class TextRequest(BaseModel):
    text: str
    
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

@login_router.post("/login")
async def login(request: LoginRequest):
    result = await AuthController.login(request.email, request.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@login_router.post("/signup")
async def signup(request: SignupRequest):
    result = await AuthController.signup(request.email)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@login_router.post("/verify-otp")
async def verify_otp(request: OTPVerifyRequest):
    result = await AuthController.verify_signup(request.email, request.otp, request.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result



@login_router.post("/dummy")
async def dummy(request: TextRequest):  # Accept request body as TextRequest model
    result = await AuthController.dummy(request.text)
    # return {"message": "Dummy route"}

# Request Password Reset OTP
@login_router.post("/request-password-reset")
async def request_password_reset(request: PasswordResetRequest):
    result = await AuthController.send_password_reset_otp(request.email)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Verify OTP and Reset Password
@login_router.post("/reset-password")
async def reset_password(request: PasswordResetVerifyRequest):
    result = await AuthController.reset_password(request.email, request.otp, request.new_password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result