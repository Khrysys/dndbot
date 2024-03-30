from discord import utils

from . import bot

from . import metadata
from .metadata import *
from .utils import pluralize

@bot.event
async def on_ready():
    # Get list of guilds this bot is a part of
    guilds = bot.guilds
    
    # For each guild, check the name of it to see if it is the bot's metadata guild
    metadata_guild = None
    for guild in guilds:
       if guild.name == METADATA_GUILD_NAME:
           metadata_guild = guild
           break
       
    if metadata_guild is None:
        # Make sure that the bot is not in more than 10 guilds
        if len(guilds) >= 10:
            raise Exception("This bot does not have a Metadata guild and is in more than 10 guilds, please select a new guild to become the metadata guild")
        
        # Create a new metadata guild, in case it got deleted
        metadata_guild = await bot.create_guild(name=METADATA_GUILD_NAME)
        
        #delete the default things
        for category in metadata_guild.categories:
            await category.delete()
            
        for channel in metadata_guild.channels:
            await channel.delete()
        
        # Create the main metadata channel in the guild
        await metadata_guild.create_text_channel(MAIN_METADATA_CHANNEL_NAME)
    
    
    metadata.METADATA_GUILD_ID = metadata_guild.id
        
    print(f"Found metadata server (Name: {METADATA_GUILD_NAME}, ID: {metadata_guild.id})")
    
    # We need to find the main metadata channel first
    metadata_channel = utils.get(metadata_guild.text_channels, name=MAIN_METADATA_CHANNEL_NAME)
    if metadata_channel is None:
        metadata_channel = await metadata_guild.create_text_channel(MAIN_METADATA_CHANNEL_NAME)
    
    # Create an invite link to the server so that the dev can see the data
    invite = await metadata_channel.create_invite(max_age=600)
    print(invite.url)
    
    # Check the channels in that guild
    for category in metadata_guild.categories:
        to_find = METADATA_CHANNELS
        # We want to verify that each category can represent a whole server, 
        # IE a channel for the role IDs, the DMs, the general campaign info, etc.
        for channel in category.channels:
            if channel.name in to_find:
                to_find.remove(channel.name)
            else:
                print(f"Unknown channel {channel.name} found in {category.name}")
                await channel.delete()
                
        if not len(to_find) == 0:
            for create in to_find:
                await metadata_guild.create_text_channel(create, category=category)
                
    print(f"Currently managing {pluralize('campaign', len(metadata_guild.categories))} in {pluralize('guilds', len(bot.guilds) - 1)}.")