from discord import Intents
from discord.ext.commands import Bot #type: ignore

intents = Intents.all()
bot = Bot(command_prefix='!?', intents=intents)

from . import commands, messages, metadata, start, utils #type: ignore