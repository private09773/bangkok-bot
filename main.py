import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Configuring Gateway Intents.
intents = discord.Intents.default()
intents.message_content = True  # Required for Prefix Commands.
intents.members = True  # Privileged Intent for Member Events.

# Instiantiate Bot Client with prefix, default prefix is "." but you can change it to your preference.
bot = commands.Bot(command_prefix=".", intents=intents)

# Load all cogs (modules).
initial_extensions = [
    "cogs.utils",
    "cogs.announcement",
    "cogs.flight"
]

@bot.event
async def setup_hook():
    for extension in initial_extensions:
        await bot.load_extension(extension)
        
# Running The Bot
@bot.event
async def on_ready():
    print(f"Online as {bot.user.name}.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")

    # Set presence INSIDE the async function
    activity = discord.Activity(
        type=discord.ActivityType.watching, 
        name="in development"
    )
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: You have not placed your token inside the '.env' file, place it inside there.")
        
if __name__ == "__main__":
    GUILD = os.getenv("GUILD_ID")
    if GUILD:
        print("Your Guild ID is succesfully Configured, the bot will run.")
    else:
        print("Error: Your Guild ID is not set, please set it in the '.env' file.")
        
if __name__ == "__main__":
    OWNER = os.getenv("OWNER_ID")
    if OWNER:
        print("Your OWNER ID is succesfully configured, the bot will run.")
    else:
        print("Error: Owner ID is not setted up.")
