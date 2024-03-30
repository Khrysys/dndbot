
METADATA_GUILD_NAME = 'DNDBOT_METADATA'
MAIN_METADATA_CHANNEL_NAME = 'general-metadata'

METADATA_CHANNELS = ['general']
METADATA_GUILD_ID: int
MAIN_METADATA_CHANNEL_ID: int

from typing import List, Tuple
from . import bot

from discord import Guild, utils

async def get_metadata_guild() -> Guild | None:
    return await utils.get(bot.guilds, id=METADATA_GUILD_ID, name=METADATA_GUILD_NAME) # type: ignore

async def search_all_campaigns(data_name: str):
    '''
    Search through all campaigns for a piece of metadata, IE the DM UID.
    Returns a list of tuples of all found occurrences, with the first value
    being the category ID that the data was found in, and the second being the value found
    '''
    metadata_guild = await get_metadata_guild()
    
    if metadata_guild is None:
        raise Exception(f"Metadata guild could not be found with ID {METADATA_GUILD_ID} and name {METADATA_GUILD_NAME}") # type: ignore
    
    found: List[Tuple[int, str]] = []
    for category in metadata_guild.categories:
        [found.append(d) for d in await search_campaign(category.id, data_name)]
                
                
    return found # type: ignore
    
async def search_campaign(campaign_id: int, data_name: str):
    '''
    Returns: A list of tuples, with the first value being the name of the channel it was found, and the second being the value found for the metadata key.
    
    Most likely, there is only one instance of each bit of metadata, but it's still good to be sure, just in case the program expands
    '''
    metadata_guild = await get_metadata_guild()
    
    if metadata_guild is None:
        raise Exception(f"Metadata guild could not be found with ID {METADATA_GUILD_ID} and name {METADATA_GUILD_NAME}") # type: ignore
    
    # This can be changed to name if needed
    category = utils.get(metadata_guild.categories, id=campaign_id)
    
    if category is None:
        raise Exception(f"Campaign with ID {campaign_id} was not found")
    
    found: List[Tuple[int, str]] = []
    for channel in category.text_channels:
        async for message in channel.history():
                content = message.content
                # find the content
                index = content.find(data_name)
                
                if index != -1:
                    # Substring the message content
                    content = content[index:]
                    # Split off the rest of the data via newlines
                    content = content.split('\n')[0]
                    # Delete the name piece (the +2 is for the colon and space after the name)
                    content = content[len(data_name) + 2]
                    # Store this
                    found.append( (category.id, content) )
            
    return found