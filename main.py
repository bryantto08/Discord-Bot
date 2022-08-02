import discord
from discord.ext import commands
import os
import subprocess
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError, TftWatcher
from datetime import datetime
import asyncio
# import PyNaCl

import helpers
from helpers import *

client = discord.Client()
load_dotenv()
discord_key = os.getenv("discord_key")
riot_key = os.getenv("riot_key")
lol_watcher = LolWatcher(riot_key)
tft_watcher = TftWatcher(riot_key)


class StarBot(commands.Bot):
    # Initializes the bot, determines its prefix as $
    def __init__(self):
        super().__init__(
            command_prefix="*",
            help_command=commands.DefaultHelpCommand(no_category="List of Commands")
        )
        self.bot = commands.Bot(
            command_prefix="*"
        )
        self.count = 0

        # When the bot is officially online
        @self.event
        async def on_ready():
            print("Bot logged in!")

        @self.command(brief="sends back text")
        async def test(channel, *, arg):
            self.count += 1
            if sus_check():
                await channel.send("sus")
            await channel.send(arg)

        # Function occurs when test function has an error
        @test.error
        async def test_error(channel, error):
            # isinstance function checks if specified object(error) is of specified type (error type)
            if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
                await channel.send("No argument found")

        @self.command(brief="sends back league info")
        async def summoner(channel, summoner_name):
            player_info = lol_watcher.summoner.by_name("na1", summoner_name)
            player_level = player_info["summonerLevel"]
            player_rank = lol_watcher.league.by_summoner("na1", player_info["id"])
            player_tft_rank = tft_watcher.league.by_summoner("na1", player_info["id"])
            my_string = f"{summoner_name} (Level {player_level}): " + "\n"
            for i in range(len(player_rank)):
                my_string += summoner_string(player_rank[i]) + "\n"
            my_string += summoner_string(player_tft_rank[0])
            if (len(player_rank)) == 0 and (len(player_tft_rank)) == 0:
                my_string += "Unranked at everything lul"
            self.count += 1
            if sus_check():
                await channel.send("sus")
            await channel.send("```" + my_string + "```")

        @summoner.error
        async def summoner_error(channel, error):
            await channel.send("Summoner not found!")

        @self.command(brief="sends back champ mastery info")
        async def mastery(channel, *, summoner_name):
            # Helper functions located in helpers.py
            player_info = lol_watcher.summoner.by_name("na1", summoner_name)
            player_mastery = lol_watcher.champion_mastery.by_summoner("na1", player_info["id"])
            my_string = "Top 5 Champions: " + "\n"
            for i in range(5):
                my_string += champ_mastery_string(player_mastery[i]) + "\n"
            self.count += 1
            if sus_check():
                await channel.send("sus")
            await channel.send("```" + my_string + "```")

        @mastery.error
        async def mastery_error(channel, error):
            await channel.send("Summoner not found!")

        @self.command(brief="sends back match history")
        async def match_history(channel, summoner_name):
            # Used to retrieve summoner id
            player_info = lol_watcher.summoner.by_name("na1", summoner_name)
            player_match_history = lol_watcher.match.matchlist_by_puuid("na1", player_info["puuid"], count=5)
            my_string = ""
            for i in player_match_history:
                match = lol_watcher.match.by_id("na1", i)
                my_string += match_history_string(match, summoner_name) + "\n"
            self.count += 1
            if sus_check():
                await channel.send("sus")
            await channel.send("```" + my_string + "```")

        # @self.command()
        # async def join(channel):
        #     if channel.author.voice is None:
        #         await channel.send("You are not in a VC")
        #     voice_channel = channel.author.voice.channel
        #     if channel.voice_client is None:
        #         await voice_channel.connect()
        #     else:
        #         await channel.voice_client.move_to(voice_channel)



bot = StarBot()
bot.run(discord_key)
