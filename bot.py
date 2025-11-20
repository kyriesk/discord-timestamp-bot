"""
Discord Timestamp Bot - Main entry point
Converts natural language and relative time to Discord timestamps.
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio


# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("Error: DISCORD_TOKEN not found in .env file")
    print("Please create a .env file with your Discord bot token:")
    print("DISCORD_TOKEN=your_bot_token_here")
    exit(1)


class TimestampBot(commands.Bot):
    """Custom bot class for the Timestamp Bot."""
    
    def __init__(self):
        # Use default intents - no privileged intents needed for slash commands
        intents = discord.Intents.default()
        
        super().__init__(
            command_prefix="!",  # Prefix for text commands (not used for slash commands)
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Called when the bot is starting up."""
        # Load cogs
        await self.load_extension("cogs.timestamp")
        
        # Sync commands with Discord
        print("Syncing commands with Discord...")
        await self.tree.sync()
        print("Commands synced!")
    
    async def on_ready(self):
        """Called when the bot is ready."""
        print(f"✅ Logged in as {self.user} (ID: {self.user.id})")
        print(f"Connected to {len(self.guilds)} guild(s)")
        print("Bot is ready!")
        print("\nAvailable commands:")
        print("  /timestamp <time_string> - Convert natural language to timestamp")
        print("  /in <duration> - Generate timestamp for future time")
        print("  /timezone <timezone> - Set your timezone")
        print("\n" + "="*50)


def main():
    """Main entry point."""
    bot = TimestampBot()
    
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("\n❌ Error: Invalid Discord token")
        print("Please check your DISCORD_TOKEN in the .env file")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
