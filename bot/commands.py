from typing import Any
from discord.ext.commands import Context, guild_only # type: ignore

from . import bot
from .metadata import *

@bot.group(pass_context=True, invoke_without_command=True)
@guild_only()
async def campaign(ctx: Context[Any]):
    '''Check if this user has a campaign here'''
    data = await search_all_campaigns("game_master")
    
    valid_campaigns: List[str] = []
    for campaign in data:
        # Unpack
        campaign_id, game_master_id = campaign
        # Check
        if game_master_id == str(ctx.author.id):
            valid_campaigns.append(str(campaign_id))
    if len(valid_campaigns) > 0:
        await ctx.send("You are the game master of the following campaigns:")
        return
    
    await ctx.send("You are not running any campaigns.")
        
@campaign.group(pass_context=True, invoke_without_command=True)
@guild_only()
async def start(ctx: Context[Any], name: str):
    '''Start a new campaign (Must be a DM)'''
    # Check that user is a DM