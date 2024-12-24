from discord.ext import commands, tasks
from config import Config
import discord
import aiohttp
import orjson  # orjson is faster than json


def port_to_name(port):
    # ex: 7777 = (7777 - 7777) + 1 = 0 + 1 = 1
    # ex: 7778 = (7778 - 7777) + 1 = 1 + 1 = 2
    return port - 7777 + 1


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_server_index = 0

    @tasks.loop(seconds=6)
    async def nwapi_interact(self):
        # for async code, use aiohttp
        params = {"id": Config.server_id, "key": Config.api_token}
        header = {
            "User-Agent": "FrontlineBot/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.scpslgame.com/serverinfo.php?players=true",
                    params=params,
                    headers=header,
                ) as response:
                    data = orjson.loads(await response.text())
                    servers = []

                    for server in data["Servers"]:
                        # Include only online servers
                        if server.get("Players") is not None:
                            servers.append(server)

                    self.servers = servers

        except Exception as e:
            print(e)

    @tasks.loop(seconds=2)
    async def update_presence(self):
        if not hasattr(self, "servers"):
            # Not ready yet
            return
        try:
            server = self.servers[self.current_server_index]
            if server.get("Players") is not None:
                await self.bot.change_presence(
                    activity=discord.Game(
                        name=f"#{port_to_name(server['Port'])}ㅣ{server['Players']} 플레이"
                    ),
                    status=discord.Status.online,
                )
            self.current_server_index = (self.current_server_index + 1) % len(
                self.servers
            )
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_ready(self):
        self.nwapi_interact.start()
        self.update_presence.start()


async def setup(bot):
    await bot.add_cog(Server(bot))
