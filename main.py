import os
import discord
import sentry_sdk
from aiohttp import web
from config import Config
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True)
routes = []


class FrontlineBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            help_command=None,
            intents=intents,
        )

    async def setup_hook(self):
        if not Config.disable_ascii:
            with open("data/ascii.txt", "r") as f:
                print(f.read())
        else:
            print("Frontline Bot\n")
        print("Just feel alive, Fear or light\n") # from Daybreak Frontline lyrics :)

        print("=== Checking Sentry DSN ===")
        if Config.sentry_dsn:
            sentry_sdk.init(Config.sentry_dsn)
            print("Sentry initialized")
        print("=== Sentry DSN checked ===\n")

        print("=== Loading extensions ===")
        for extension in os.listdir("cogs"):
            if extension.endswith(".py"):
                await self.load_extension(f"cogs.{extension[:-3]}")
                print(f"Loaded extension: {extension}")
        print("=== Extensions loaded ===\n")

        print("=== Loading routes ===")
        for file in os.listdir("routes"):
            if file.endswith(".py"):
                module_name = "routes." + file[:-3]
                module = __import__(module_name, fromlist=[""]) # Import the module
                route = getattr(module, "get_route")() # Get the route
                print(f"Loaded route: {route.path}")
                routes.append(route)
        print("=== Routes loaded ===\n")

    async def on_ready(self):
        await self.change_presence(
            activity=discord.CustomActivity(name="불러오는 중. . ."),
            status=discord.Status.idle,
        )
        print(f"Logged in as {self.user}")

        # Start the web server
        await run_server(self)

async def run_server(bot: FrontlineBot):
    return
    # I know this is a bad way to do it,
    # but I don't want to create new project for this
    app = web.Application(loop=bot.loop)
    app.bot = bot # Pass the bot instance to the app
    app.temp = {} # Temporary storage for the app
    bot.http_app = app # Store the app in the bot instance

    for route in routes:
        app.router.add_route(route.method, route.path, route.handler)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", Config.port)
    await site.start()

    print("Started web server")

bot = FrontlineBot()

if __name__ == "__main__":
    bot.run(Config.token, log_handler=None)