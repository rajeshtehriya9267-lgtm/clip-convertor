from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)

db = client.clip_convertor

users = db.users
jobs = db.jobs
