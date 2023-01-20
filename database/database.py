import datetime
import motor.motor_asyncio
from config import Config


class Database:

    async def set_thumbnail(self, id, thumbnail):
        await self.col.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail', None)

db = Database(Config.DATABASE_URL, Config.SESSION_NAME)
