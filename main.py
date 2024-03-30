from os import getenv
from dotenv import load_dotenv

load_dotenv()

from bot import bot

TOKEN = getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise Exception("TOKEN was none!")

bot.run(TOKEN)