from typing import Any
from discord import PermissionOverwrite
from discord.ext.commands import Context # type: ignore

def pluralize(word: str, count: int) -> str:
    return f"{count} {word}{'s' if count != 1 else ''}"


def create_overwrites(ctx: Context[Any], *objects): #type: ignore
    """This is just a helper function that creates the overwrites for the
    voice/text channels.

    A `discord.PermissionOverwrite` allows you to determine the permissions
    of an object, whether it be a `discord.Role` or a `discord.Member`.

    In this case, the `view_channel` permission is being used to hide the channel
    from being viewed by whoever does not meet the criteria, thus creating a
    secret channel.
    """

    # a dict comprehension is being utilised here to set the same permission overwrites
    # for each `discord.Role` or `discord.Member`.
    overwrites = {obj: PermissionOverwrite(view_channel=True) for obj in objects} #type: ignore

    # prevents the default role (@everyone) from viewing the channel
    # if it isn't already allowed to view the channel.
    overwrites.setdefault(ctx.guild.default_role, PermissionOverwrite(view_channel=False)) #type: ignore

    # makes sure the client is always allowed to view the channel.
    overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True) #type: ignore

    return overwrites #type: ignore