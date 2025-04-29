from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import (
    roles_collection,
    users_collection,
    products_collection,
    org_account_mapping_collection,
    role_mapping_collection,
)
from auth import router as auth_router, verify_token, bcrypt, create_token
from fastapi.security import OAuth2PasswordBearer
from models import Roles, Products, OrgAccountMapping, RolesMap
from fastapi.middleware.cors import CORSMiddleware

# FastAPI App
app = FastAPI()

# Include Auth Routes
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:8080"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/roles", status_code=201)
async def create_role(role: Roles, username: str = Depends(verify_token)):
    """Create a new role (requires authentication)"""
    try:
        new_role = {"roleName": role.roleName, "Created_at": datetime.utcnow()}
        result = roles_collection.insert_one(new_role)
        return {"message": "Role created", "role_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@app.get("/users")
async def get_all_users(username: str = Depends(verify_token)):
    """Get all users (requires authentication)"""
    try:
        # Exclude password for security
        users = list(users_collection.find({}, {"user_password": 0, "_id": 0}))
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/products", status_code=201)
async def create_product(product: Products, username: str = Depends(verify_token)):
    """Add a new product (requires authentication)"""
    try:
        new_product = {
            "productname": product.productname,
            "price": product.price,
            "created_at": datetime.utcnow(),
            "created_by": username,  # Track who created the product
        }
        result = products_collection.insert_one(new_product)
        return {"message": "Product added", "product_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@app.get("/products")
async def get_products(username: str = Depends(verify_token)):
    """Get all products (requires authentication)"""
    try:
        products = list(products_collection.find({}, {"_id": 0}))
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/orgaccountmapping", status_code=201)
async def create_mapping(
    mapping: OrgAccountMapping, username: str = Depends(verify_token)
):
    """Create organization-account mapping (requires authentication)"""
    try:
        new_mapping = {
            "Orgid": mapping.orgid,
            "Morgid": 1,
            "Accountid": mapping.accountid,
            "Created_At": datetime.utcnow(),
            "Createdbyid": 535,
            "SystemName": "SHASHANK",
            "created_by": username,  # Track who created the mapping
        }
        result = org_account_mapping_collection.insert_one(new_mapping)
        return {"message": "Mapping created", "mapping_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@app.post("/rolemap", status_code=201)
async def create_mapping(mapping: RolesMap, username: str = Depends(verify_token)):
    """
    Create role-mapping (requires authentication).
    Validates role and user before mapping.
    """
    try:
        # Check if role exists (case-insensitive search)
        role_data = roles_collection.find_one(
            {"roleName": {"$regex": f"^{mapping.role}$", "$options": "i"}}
        )
        if not role_data:
            raise HTTPException(status_code=404, detail="Role not found")

        # Check if user exists (case-insensitive search)
        user_data = users_collection.find_one(
            {"UserName": {"$regex": f"^{mapping.user}$", "$options": "i"}}
        )
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare new mapping
        new_mapping = {
            "roleid": str(role_data["_id"]),
            "userid": str(user_data["_id"]),
            "created_at": datetime.utcnow(),
            "created_by": username,
        }

        # Insert mapping
        result = role_mapping_collection.insert_one(new_mapping)
        return {
            "message": "Role mapping created successfully",
            "mapping_id": str(result.inserted_id),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


# @app.post("/rolemap", status_code=201)
# async def create_mapping(mapping: RolesMap, username: str = Depends(verify_token)):
#     """
#     Create role-mapping (requires authentication).
#     Gets all roles and users first, then selects and creates mapping.
#     """
#     try:
#         # Get all roles
#         all_roles = list(roles_collection.find({}, {"roleName": 1}))
#         if not all_roles:
#             raise HTTPException(status_code=404, detail="No roles found in system")

#         # Get all users
#         all_users = list(users_collection.find({}, {"UserName": 1}))
#         if not all_users:
#             raise HTTPException(status_code=404, detail="No users found in system")

#         # Find the selected role (case-insensitive search)
#         role_data = next(
#             (
#                 role
#                 for role in all_roles
#                 if role["roleName"].lower() == mapping.role.lower()
#             ),
#             None,
#         )
#         if not role_data:
#             raise HTTPException(status_code=404, detail="Selected role not found")

#         # Find the selected user (case-insensitive search)
#         user_data = next(
#             (
#                 user
#                 for user in all_users
#                 if user["UserName"].lower() == mapping.user.lower()
#             ),
#             None,
#         )
#         if not user_data:
#             raise HTTPException(status_code=404, detail="Selected user not found")

#         # Prepare new mapping
#         new_mapping = {
#             "roleid": str(role_data["_id"]),
#             "userid": str(user_data["_id"]),
#             "created_at": datetime.utcnow(),
#             "created_by": username,
#         }

#         # Insert mapping
#         result = role_mapping_collection.insert_one(new_mapping)
#         return {
#             "message": "Role mapping created successfully",
#             "mapping_id": str(result.inserted_id),
#         }

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
