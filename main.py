import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

client = discord.Client()
load_dotenv()
discord_key = os.getenv("discord_key")


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
        async def test(ctx, arg):
            await ctx.send(arg)

        # Function occurs when test function has an error
        @test.error
        async def test_error(ctx, error):
            # isinstance function checks if specified object(error) is of specified type (error type)
            if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
                await ctx.send("No argument found")


bot = PointGameBot()
bot.run(discord_key)
