from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017")

# Access the "SystemDB" database
db = client.SystemDB

# Access the "Users" collection
users_collection = db.Users

# Define the new user data as a Python dictionary
new_user = {
    "srno": 1,
    "name": "Sahil Shete",
    "username": "sahil",
    "password": "sgp123",
    "access": "sub-admin",
    "department": "CSE"
}

# Insert the new user document into the collection
users_collection.insert_one(new_user)

# Close the MongoDB connection
client.close()
