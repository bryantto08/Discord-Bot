import discord
from discord.ext import commands
import os
import subprocess
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError
from datetime import datetime
import asyncio

import helpers
from helpers import *

client = discord.Client()
load_dotenv()
discord_key = os.getenv("discord_key")
riot_key = os.getenv("riot_key")
lol_watcher = LolWatcher(riot_key)


class PointGameBot(commands.Bot):
    # Initializes the bot, determines its prefix as $
    def __init__(self):
        super().__init__(
            command_prefix="$",
            help_command=commands.DefaultHelpCommand(no_category="List of Commands")
        )
        self.bot = commands.Bot(
            command_prefix="$"
        )

        # When the bot is officially online
        @self.event
        async def on_ready():
            print("Bot logged in!")

        @self.command(brief="sends back text")
        async def test(channel, arg):
            await channel.send(arg)

        # Function occurs when test function has an error
        @test.error
        async def test_error(channel, error):
            # isinstance function checks if specified object(error) is of specified type (error type)
            if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
                await channel.send("No argument found")

        @self.command(brief="sends back league level")
        async def summoner(channel, arg):
            player_info = lol_watcher.summoner.by_name("na1", arg)
            await channel.send(player_info["summonerLevel"])

        @self.command(brief="sends back champ mastery info")
        async def champ_mastery(channel, arg):
            # Helper functions located in helpers.py
            player_info = lol_watcher.summoner.by_name("na1", arg)
            player_mastery = lol_watcher.champion_mastery.by_summoner("na1", player_info["id"])
            my_string = "Top 5 Champions: " + "\n"
            for i in range(5):
                my_string += champ_mastery_string(player_mastery[i]) + "\n"
            await channel.send("```" + my_string + "```")


bot = PointGameBot()
bot.run(discord_key)
