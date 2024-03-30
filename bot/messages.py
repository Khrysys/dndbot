from discord import Message
from . import bot

@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return
    
    word_ban(message)

def word_ban(message: Message):
    pass