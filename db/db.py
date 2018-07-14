import asyncio
import os

import gino
from sqlalchemy.sql import exists
import asyncpg.exceptions

from db.models.base import db
from db.models.user import User
from db.models.guild import Guild
from db.models.autoreply import Autoreply

asyncio.ensure_future(db.set_bind(os.environ["DATABASE_URL"]))


# TODO: implement caching


# User ops
async def add_user(user: User):
    try:
        await user.create()
        return True
    except asyncpg.UniqueViolationError:
        return False


async def get_user(user_id: int):
    return await User.get(user_id)


# Guild ops
async def add_guild(guild: Guild):
    try:
        await guild.create()
        return True
    except asyncpg.UniqueViolationError:
        return False


async def remove_guild(guild: Guild):
    await guild.delete()


async def get_guild(guild_id: int):
    return await Guild.get(guild_id)


# Autoreply ops
async def add_autoreply(autoreply: Autoreply):
    try:
        await autoreply.create()
        return True
    except asyncpg.UniqueViolationError:
        return False


async def get_autoreply(guild_id: int, rgx: str):
    return await Autoreply.get((guild_id, rgx))


# space-inefficient. assume a sane limit on the number of rows this query returns.
async def get_all_autoreplies(guild_id: int):
    return await Autoreply.query.where(Autoreply.guild_id == guild_id).gino.all()


async def delete_autoreply(guild_id: int, rgx: str):
    return await Autoreply.delete.where((Autoreply.guild_id == guild_id) & (Autoreply.regex == rgx)).gino.status()