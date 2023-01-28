from datetime import datetime
from decouple import config
import certifi
from motor.motor_asyncio import AsyncIOMotorClient


class Mongo_DB:
    dorama_collection = {
        "_id": "",
        "title": "",
        "series": "",
        "country": "",
        "year": "",
        "genre": "",
        "image": "",
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    }

    def __init__(self):
        self.client = AsyncIOMotorClient(
            config("MONGO_DB_URL"), tlsCAFile=certifi.where()
        )
        self.db = self.client.dorama_mongo_db
        self.collection = self.db.dorama_collection

    async def add_to_dorama_collection(self, dorama_objects):
        await self.collection.insert_one(dorama_objects)
