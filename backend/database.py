from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://sssony22112000:Maskisu82%40@shashank.obuhq.mongodb.net/"
)
db = client["shapp"]
roles_collection = db["roles"]
users_collection = db["signup"]
products_collection = db["products"]
org_account_mapping_collection = db["orgaccountmapping"]
Login_History_collection = db["LoginHistory"]
role_mapping_collection = db["RoleMapping"]
