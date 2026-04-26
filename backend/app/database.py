from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# .env file load karo
load_dotenv()

# MongoDB URL .env se lo
MONGODB_URL = os.getenv("MONGODB_URL")

# MongoDB client banao
client = AsyncIOMotorClient(MONGODB_URL)

# Database select karo
db = client.smarthire

# Collections (SQL mein tables jaise hoti hain)
users_collection = db["users"]
resumes_collection = db["resumes"]
jobs_collection = db["jobs"]