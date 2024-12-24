import os
import discord
from config import Config
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True)


class FrontlineBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            help_command=None,
            intents=intents,
        )

    async def setup_hook(self):
        for extension in os.listdir("cogs"):
            if extension.endswith(".py"):
                await self.load_extension(f"cogs.{extension[:-3]}")

    async def on_ready(self):
        await self.change_presence(
            activity=discord.CustomActivity(name="불러오는 중. . ."),
            status=discord.Status.idle,
        )
        print(f"Logged in as {self.user}")


bot = FrontlineBot()
if __name__ == "__main__":
    bot.run(token=Config.token, log_handler=None)
