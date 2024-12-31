import orjson
import aiofiles

class Database:
    def __init__(self):
        # TODO: Migration to motor(mongodb)
        raise DeprecationWarning("This class is temporary and will be rewrited in the future.")

    async def read(self, path: str):
        async with aiofiles.open(path, "r") as f:
            return await f.read()
    
    async def write(self, path: str, data: dict):
        async with aiofiles.open(path, "w") as f:
            await f.write(orjson.dumps(data))

    async def read_user(self, user_id: int):
        return await self.read(f"data/users/{user_id}.json")

    async def write_user(self, user_id: int, data: dict):
        await self.write(f"data/users/{user_id}.json", data)