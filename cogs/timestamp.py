"""
Discord bot cog for timestamp commands.
"""
import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from typing import Optional
import pytz

from utils.time_parser import (
    parse_natural_time,
    parse_relative_time,
    generate_discord_timestamp,
    get_all_format_examples
)


class TimestampCog(commands.Cog):
    """Cog for handling timestamp-related commands."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_timezones_file = "user_timezones.json"
        self.user_timezones = self._load_timezones()
    
    def _load_timezones(self) -> dict:
        """Load user timezones from JSON file."""
        if os.path.exists(self.user_timezones_file):
            try:
                with open(self.user_timezones_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_timezones(self):
        """Save user timezones to JSON file."""
        try:
            with open(self.user_timezones_file, 'w') as f:
                json.dump(self.user_timezones, f, indent=2)
        except Exception as e:
            print(f"Error saving timezones: {e}")
    
    def _get_user_timezone(self, user_id: int) -> str:
        """Get user's timezone, defaulting to UTC."""
        return self.user_timezones.get(str(user_id), "UTC")
    
    @app_commands.command(name="timestamp", description="Convert natural language to a Discord timestamp")
    @app_commands.describe(time_string="Natural language time (e.g., 'today 3pm', 'tomorrow', 'next friday')")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def timestamp_command(self, interaction: discord.Interaction, time_string: str):
        """Convert natural language time to Discord timestamp."""
        try:
            user_tz = self._get_user_timezone(interaction.user.id)
            
            # Parse the time
            dt = parse_natural_time(time_string, user_tz)
            
            # Generate timestamp (using Long Date/Time format by default)
            timestamp = generate_discord_timestamp(dt, "F")
            
            # Send clean response with timestamp
            await interaction.response.send_message(
                f"📅 {timestamp} (**{time_string}**)"
            )
            
        except ValueError as e:
            await interaction.response.send_message(
                f"❌ Error: {str(e)}\n\nPlease try a different format or set your timezone with `/timezone`",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An unexpected error occurred: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="in", description="Generate timestamp for a time in the future")
    @app_commands.describe(duration="Duration (e.g., '1 hour', '30 minutes', '2 hours 15 minutes')")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def in_command(self, interaction: discord.Interaction, duration: str):
        """Generate timestamp for relative future time."""
        try:
            # Parse relative time
            dt = parse_relative_time(duration)
            
            # Generate timestamp with Relative format to show "in X hours"
            timestamp = generate_discord_timestamp(dt, "R")
            
            # Send clean response with timestamp
            await interaction.response.send_message(
                f"⏱️ {timestamp} (in **{duration}**)"
            )
            
        except ValueError as e:
            await interaction.response.send_message(
                f"❌ Error: {str(e)}\n\nExample formats: '1 hour', '30 minutes', '2h 15m'",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An unexpected error occurred: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="timezone", description="Set your timezone for timestamp commands")
    @app_commands.describe(timezone="IANA timezone (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def timezone_command(self, interaction: discord.Interaction, timezone: str):
        """Set user's timezone."""
        try:
            # Validate timezone
            pytz.timezone(timezone)
            
            # Save timezone
            self.user_timezones[str(interaction.user.id)] = timezone
            self._save_timezones()
            
            await interaction.response.send_message(
                f"✅ Your timezone has been set to **{timezone}**",
                ephemeral=True
            )
            
        except pytz.exceptions.UnknownTimeZoneError:
            await interaction.response.send_message(
                f"❌ Unknown timezone: {timezone}\n\n"
                "Please use IANA timezone format (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')\n"
                "Find your timezone at: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An unexpected error occurred: {str(e)}",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    """Load the cog."""
    await bot.add_cog(TimestampCog(bot))
