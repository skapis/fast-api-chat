from motor.motor_asyncio import AsyncIOMotorClient
from app.config import DB_URL, DB_NAME

client = AsyncIOMotorClient(DB_URL)
db = client[DB_NAME]

users_collection = db['users']
messages_collection = db['messages']
chats_collection = db['chats']