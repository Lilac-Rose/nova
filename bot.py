# bot.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import environ
import json
from pathlib import Path
from tasks.daily_reminder import DailyReminder

# Load environment variables
load_dotenv()

# Path to the JSON file
SPARKLES_FILE = Path("sparkles.json")

def load_sparkles():
    """Load the sparkles data from a JSON file."""
    if SPARKLES_FILE.exists():
        with open(SPARKLES_FILE, "r") as f:
            return json.load(f)
    return {}

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Set up the bot
class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sparkles = load_sparkles()  # Load sparkles data on startup

    def save_sparkles(sparkles):
    """Save the sparkles data to a JSON file."""
    with open(SPARKLES_FILE, "w") as f:
        json.dump(sparkles, f, indent=4)

    async def close(self):
        self.save_sparkles(self.sparkles)  # Save sparkles data on shutdown
        await super().close()

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await load_extensions()
    DailyReminder(bot)  # Initialize the DailyReminder task
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Load commands and events
async def load_extensions():
    await bot.load_extension("commands.hello")
    await bot.load_extension("commands.ping")
    await bot.load_extension("commands.forcesparkle")
    await bot.load_extension("commands.leaderboard")
    await bot.load_extension("commands.whoareyou")
    await bot.load_extension("events.on_message")

# Run the bot
bot.run(environ.get('TOKEN'))
