from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SignUp(BaseModel):
    _id: str  # Auto-generated ID
    FirstName: str
    LastName: str
    UserName: str
    emailaddress: str
    user_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "johndoe",
                "emailaddress": "john.doe@example.com",
                "user_password": "securePassword123",
            }
        }


class Login(BaseModel):
    UserName: str
    user_password: str

    class Config:
        json_schema_extra = {
            "example": {"UserName": "johndoe", "user_password": "securePassword123"}
        }


class Roles(BaseModel):
    roleName: str
    Created_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {"roleName": "admin", "Created_at": "2023-01-01T00:00:00Z"}
        }


class Products(BaseModel):
    productname: str
    price: float

    class Config:
        json_schema_extra = {"example": {"productname": "Laptop", "price": 999.99}}


class OrgAccountMapping(BaseModel):
    orgid: int
    accountid: int

    class Config:
        json_schema_extra = {"example": {"orgid": 123, "accountid": 123}}


class UserCart(BaseModel):
    username: str
    productname: str
    quantity: int = 1

    class Config:
        json_schema_extra = {
            "example": {"username": "johndoe", "productname": "Laptop", "quantity": 2}
        }


class LoginHistory(BaseModel):
    id: str  # Auto-generated ID
    userid: str
    UserName: str
    LoginTime: datetime
    Status: bool

    class Config:
        json_schema_extra = {
            "example": {
                "userid": 1,
                "UserName": "johndoe",
                "LoginTime": "2023-01-01T00:00:00Z",
                "Status": "Success",
            }
        }


class RolesMap(BaseModel):
    role: str
    user: str

    class Config:
        json_schema_extra = {"example": {"role": "Data Engineer", "user": "gr8282"}}
