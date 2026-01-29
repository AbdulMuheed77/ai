from pymongo import MongoClient

# Replace with your connection string
uri = "mongodb+srv://Admin:Admin@cluster0.h5jynbq.mongodb.net/?appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri)

# Choose a database (it will be created if it doesn't exist)
db = client.testDB

# Example: List collections
print("Collections in DB:", db.list_collection_names())

# Optional: Add a test document
test_collection = db.testCollection
test_collection.insert_one({"name": "Muheed", "role": "student"})

# Read it back
for doc in test_collection.find():
    print(doc)
