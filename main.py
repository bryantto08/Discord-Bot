import discord
from discord.ext import commands
import os
import subprocess
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError, TftWatcher
from datetime import datetime
import asyncio
# import PyNaCl
from keep_alive import keep_alive


import helpers
from helpers import *

intents = discord.Intents.all()
client = discord.Client(intents=intents)
load_dotenv()
discord_key = os.getenv("discord_key")
riot_key = os.getenv("riot_key")
lol_watcher = LolWatcher(riot_key)
tft_watcher = TftWatcher(riot_key)


class StarBot(commands.Bot):
    # Initializes the bot, determines its prefix as $
    def __init__(self):
        super().__init__(command_prefix="*",
                         intents=intents,
                         help_command=commands.DefaultHelpCommand(
                             no_category="List of Commands"))
        self.remove_command("help")
        self.bot = commands.Bot(command_prefix="*", intents=intents)
        self.count = 0

        # When the bot is officially online
        @self.event
        async def on_ready():
            print("Bot logged in!")

        @self.command()
        async def help(channel):
            embed = discord.Embed(
                title="Bot Commands",
                description="sussy commands",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="*test",
                value="For Testing this Sussy Little Bot",
                inline=False
            )
            embed.add_field(
                name="*help",
                value="List of Commands",
                inline=False
            )
            embed.add_field(
                name="*summoner",
                value="League of Legends Summoner Stats",
                inline=False
            )
            embed.add_field(
                name="*mastery",
                value="League of Legends Mastery Stats",
                inline=False
            )
            embed.add_field(
                name="*match_history",
                value="League of Legends Match History (Last 5 Games)",
                inline=False
            )
            await channel.send(embed=embed)

        @self.command(brief="sends back text")
        async def test(channel, *, arg):
            embed=discord.Embed(
                title=arg
            )

            self.count += 1
            if sus_check():
                await channel.send(embed=discord.Embed(title="sus"))
            await channel.send(embed=embed)

        # Function occurs when test function has an error
        @test.error
        async def test_error(channel, error):
            # isinstance function checks if specified object(error) is of specified type (error type)
            if isinstance(error,
                          discord.ext.commands.errors.MissingRequiredArgument):
                await channel.send("No argument found")

        @self.command(brief="sends back league info")
        async def summoner(channel, summoner_name):
            player_info = lol_watcher.summoner.by_name("na1", summoner_name)
            player_level = player_info["summonerLevel"]
            player_rank = lol_watcher.league.by_summoner(
                "na1", player_info["id"])
            player_tft_rank = tft_watcher.league.by_summoner(
                "na1", player_info["id"])
            embed = discord.Embed(
                title=player_info["name"] + " (Level:" + str(player_level) + ")",
                color=discord.Color.blurple()
            )
            for i in range(len(player_rank)):
                embed.add_field(
                    name=player_rank[i]["queueType"],
                    value=player_rank[i]["tier"] + " " + player_rank[i]["rank"],
                    inline=False

                )
            if len(player_tft_rank) > 0:
                embed.add_field(
                    name=player_rank[i]["queueType"],
                    value=player_rank[i]["tier"] + " " + player_rank[i]["rank"],
                    inline=False
                )
            if (len(player_rank)) == 0 and (len(player_tft_rank)) == 0:
                embed.add_field(
                    name="Unranked at everything lul"
                )
            self.count += 1

            if sus_check():
                await channel.send(embed=discord.Embed(title="sus"))
            await channel.send(embed=embed)

        @summoner.error
        async def summoner_error(channel, error):
            await channel.send("Summoner not found!")

        @self.command(brief="sends back champ mastery info")
        async def mastery(channel, *, summoner_name):
            # Helper functions located in helpers.py
            player_info = lol_watcher.summoner.by_name("na1", summoner_name)
            player_mastery = lol_watcher.champion_mastery.by_summoner(
                "na1", player_info["id"])
            embed = discord.Embed(
                title=player_info["name"] + "'s Top 5 Champions",
                color=discord.Color.blurple()
            )
            for i in range(5):
                champ_mastery_string(player_mastery[i], embed)
            self.count += 1
            if sus_check():
                await channel.send(embed=discord.Embed(title="sus"))
            await channel.send(embed=embed)

        @mastery.error
        async def mastery_error(channel, error):
            await channel.send("Summoner not found!")

        @self.command(brief="sends back match history")
        async def match_history(channel, summoner_name):
            # Used to retrieve summoner id
            player_info = lol_watcher.summoner.by_name("na1", summoner_name)
            # Returns a json dictionary containing 5 matches
            player_match_history = lol_watcher.match.matchlist_by_puuid(
                "na1", player_info["puuid"], count=5)
            embed = discord.Embed(
                title=player_info["name"] + "'s Match History",
            )
            for i in player_match_history:
                match = lol_watcher.match.by_id("na1", i)
                match_history_string(match, summoner_name, embed)
            self.count += 1
            if sus_check():
                await channel.send(embed=discord.Embed(title="sus"))
            await channel.send(embed=embed)

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
