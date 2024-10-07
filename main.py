import discord
from discord.ext import commands
import os
import logging

# Set up logging for better debugging and tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# Enable message content intent to handle messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize bot with command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Retrieve the bot token from Heroku environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Make sure to set this in Heroku

# Optional setting: Enable or disable message deletion
DELETE_ORIGINAL_MESSAGE = True  # Set to False if you don't want the bot to delete original user messages

@bot.event
async def on_ready():
    logging.info(f'{bot.user.name} is now online and ready to send replies on behalf of the team.')

@bot.command()
async def reply(ctx, *, message: str):
    try:
        if DELETE_ORIGINAL_MESSAGE:
            await ctx.message.delete()

        await ctx.send(f"**Support Team:** {message}")
    
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages or send messages here.")
        logging.error(f"Permission error in channel {ctx.channel.name}")
    
    except discord.HTTPException as e:
        await ctx.send("An unexpected error occurred while trying to send the message.")
        logging.error(f"HTTP error in channel {ctx.channel.name}: {str(e)}")

    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
        logging.exception(f"Unexpected error in channel {ctx.channel.name}: {str(e)}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You forgot to provide a message. Please use the command like this: `!reply [your message]`.")
        logging.warning(f"Missing argument in channel {ctx.channel.name}: {str(error)}")
    
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Please check your command syntax.")
        logging.info(f"Unknown command used in channel {ctx.channel.name}: {str(error)}")
    
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Something went wrong while executing the command.")
        logging.error(f"Command invoke error in channel {ctx.channel.name}: {str(error)}")
    
    else:
        await ctx.send(f"An unexpected error occurred: {error}")
        logging.exception(f"Unexpected command error in channel {ctx.channel.name}: {str(error)}")

bot.run(TOKEN)
