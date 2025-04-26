from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import users_collection, Login_History_collection, roles_collection
from models import SignUp, Login, LoginHistory


# JWT Settings
SECRET_KEY = "your-secure-key-123"  # Replace with a strong secret key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token and return username if valid."""
    try:
        print(f"Received Token: {token}")  # Debugging

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")  # Debugging

        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        return username
    except JWTError as e:
        print(f"JWT Error: {str(e)}")  # Debugging
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/signup", status_code=201)
async def signup(user: SignUp):
    try:
        # Check if username already exists
        if users_collection.find_one({"UserName": user.UserName}):
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the password
        hashed_password = bcrypt.hash(user.user_password)

        new_user = {
            "FirstName": user.FirstName,
            "LastName": user.LastName,
            "UserName": user.UserName,
            "emailaddress": user.emailaddress,
            "user_password": hashed_password,
            "created_at": datetime.utcnow(),
        }

        users_collection.insert_one(new_user)
        return {"message": "User created successfully", "_id": str(new_user["_id"])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/login", response_model=Token)
async def login(user: Login):
    db_user = users_collection.find_one({"UserName": user.UserName})

    if not db_user or not bcrypt.verify(user.user_password, db_user["user_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate token
    access_token = create_token(db_user["UserName"])

    # Log login attempt
    Login_History_collection.insert_one(
        {
            "Userid": str(db_user["_id"]),
            "UserName": db_user["UserName"],
            "LoginTime": datetime.utcnow(),
            "Status": "Success",
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}
