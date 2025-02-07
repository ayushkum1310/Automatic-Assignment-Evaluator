from motor.motor_asyncio import (
    AsyncIOMotorClient,
)  # Asynchronous MongoDB driver for Python
from dotenv import (
    load_dotenv,
)  # Library for loading environment variables from a .env file
import os  # Library for interacting with the operating system
from src.Logging import logging
# Load environment variables from a .env file into the current environment.
load_dotenv()


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()
# Retrieve the MongoDB URI and database name from environment variables.
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB connection string
# DB_NAME = os.getenv("DB_NAME")  # MongoDB database name
logger = logging.getLogger("uvicorn")


async def getDatabase() -> AsyncIOMotorClient:
    return db.client


async def connectToDb():
    logger.info("connecting to mongodb...")
    try:
        db.client = AsyncIOMotorClient(MONGO_URI)
        await db.client.admin.command("ping")
        print("Ping")
        logger.info("CONNECTED!!!")
    except Exception as e:
        logger.error(f"Connection failed: {e}")



async def closeMongoConnection():
    logger.info("closing....")
    db.client.close()
    logger.info("CLOSED!!!")


if __name__=='__main__':
    import asyncio
    asyncio.run(connectToDb())
    asyncio.run(closeMongoConnection())