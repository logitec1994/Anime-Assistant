from database.session import Base, engine
from database.models import Item
import asyncio

async def init_db():
    await Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    asyncio.run(init_db())
