from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://username:password@cluster.mongodb.net/sarrs?retryWrites=true&w=majority"
)

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    db = client.get_database()
except Exception as e:
    print(f"MongoDB Connection Error: {e}")
    db = None

