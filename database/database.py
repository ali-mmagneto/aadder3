# (c) @AbirHasan2005 | X-Noid

import datetime
import motor.motor_asyncio
from config import Config


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            upload_as_doc=False,
            thumbnail=None,
            notif=True,
            caption=False,
            generate_ss=False,
            generate_sample_video=False,
            blocked_exts=["webm", "3gp", "m4a", "mp4"],
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def add_user_pass(self, id, ag_pass):
        await self.add_user(int(id))
        await self.col.update_one({'id': int(id)}, {'$set': {'ag_p': ag_pass}})

    async def get_user_pass(self, id):
        user_pass = await self.col.find_one({'id': int(id)})
        return user_pass.get("ag_p", None) if user_pass else None

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_upload_as_doc(self, id, upload_as_doc):
        await self.col.update_one({'id': id}, {'$set': {'upload_as_doc': upload_as_doc}})

    async def get_upload_as_doc(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('upload_as_doc', False)

    async def set_aria2(self, id, aria2):
        await self.col.update_one({'id': id}, {'$set': {'aria2': aria2}})

    async def set_thumbnail(self, id, thumbnail):
        await self.col.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail', None)

    async def set_caption(self, id, thumbnail):
        await self.col.update_one({'id': id}, {'$set': {'caption': thumbnail}})

    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None)

    async def set_generate_ss(self, id, generate_ss):
        await self.col.update_one({'id': id}, {'$set': {'generate_ss': generate_ss}})

    async def get_generate_ss(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('generate_ss', False)

    async def set_generate_sample_video(self, id, generate_sample_video):
        await self.col.update_one({'id': id}, {'$set': {'generate_sample_video': generate_sample_video}})

    async def get_generate_sample_video(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('generate_sample_video', False)

    async def set_notif(self, id, notif):
        await self.col.update_one({"id": id}, {"$set": {"notif": notif}})

    async def get_notif(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("notif", False)

    async def get_all_notif_user(self):
        notif_users = self.col.find({"notif": True})
        return notif_users

    async def get_user_data(self, id) -> dict:
        user = await self.col.find_one({'id': int(id)})
        return user or None

    async def get_blocked_exts(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('blocked_exts', ["webm", "mhtml", "3gp", "m4a", "mp4"])

    async def set_blocked_exts(self, id, blocked_exts):
        await self.col.update_one({'id': id}, {'$set': {'blocked_exts': blocked_exts}})


db = Database(Config.DATABASE_URL, Config.SESSION_NAME)
