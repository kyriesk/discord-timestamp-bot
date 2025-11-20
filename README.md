# Discord Timestamp Bot

A Discord bot that converts natural language and relative time expressions into Discord timestamps that automatically adjust to each user's timezone.

## Features

- 🕒 **Natural Language Parsing**: Convert phrases like "today 3pm", "tomorrow", "next friday" to timestamps
- ⏱️ **Relative Time**: Generate timestamps for "1 hour", "30 minutes", "2 hours 15 minutes" from now
- 🌍 **Timezone Support**: Set your timezone so timestamps are accurate to your location
- 📋 **Multiple Formats**: See all Discord timestamp formats at once

## Setup

### Prerequisites

- Python 3.8 or higher
- A Discord Bot Token ([Get one here](https://discord.com/developers/applications))

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root:
   ```bash
   cp .env.example .env
   ```

4. **Add your Discord Bot Token** to the `.env` file:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

5. **Invite the bot to your server**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Go to OAuth2 > URL Generator
   - Select scopes: `bot` and `applications.commands`
   - Select bot permissions: `Send Messages`, `Use Slash Commands`
   - Copy the generated URL and open it in your browser to invite the bot

### Running the Bot

```bash
python bot.py
```

You should see:
```
Syncing commands with Discord...
Commands synced!
✅ Logged in as YourBot (ID: ...)
Bot is ready!
```

## Commands

### `/timestamp <time_string>`

Convert natural language time to Discord timestamps.

**Examples**:
- `/timestamp today 3pm`
- `/timestamp tomorrow at noon`
- `/timestamp next friday 18:00`
- `/timestamp December 25 2024`

### `/in <duration>`

Generate timestamps for a specific duration in the future.

**Examples**:
- `/in 1 hour`
- `/in 30 minutes`
- `/in 2 hours 15 minutes`
- `/in 45m` (abbreviations work too!)

### `/timezone <timezone>`

Set your timezone for accurate timestamp generation.

**Examples**:
- `/timezone America/New_York`
- `/timezone Europe/London`
- `/timezone Asia/Tokyo`
- `/timezone Australia/Sydney`

Find your timezone: [List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Discord Timestamp Formats

When you generate a timestamp, the bot shows all available Discord formats:

- **Short Time** (`t`): 9:41 PM
- **Long Time** (`T`): 9:41:30 PM
- **Short Date** (`d`): 30/06/2021
- **Long Date** (`D`): 30 June 2021
- **Short Date/Time** (`f`): 30 June 2021 9:41 PM
- **Long Date/Time** (`F`): Wednesday, 30 June 2021 9:41 PM
- **Relative** (`R`): 2 months ago / in 3 hours

## Testing

Run the unit tests:

```bash
python -m unittest discover tests
```

## Project Structure

```
discord_timestamp_bot/
├── bot.py                  # Main bot entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
├── cogs/
│   ├── __init__.py
│   └── timestamp.py       # Timestamp commands cog
├── utils/
│   ├── __init__.py
│   └── time_parser.py     # Time parsing utilities
└── tests/
    ├── __init__.py
    └── test_time_parser.py # Unit tests
```

## How It Works

1. **Natural Language Parsing**: Uses `dateparser` library to understand phrases like "tomorrow" or "next week"
2. **Timezone Handling**: Uses `pytz` to handle timezone conversions
3. **Discord Timestamps**: Generates Unix timestamps in Discord's special format: `<t:TIMESTAMP:FORMAT>`
4. **User Preferences**: Stores user timezone preferences in a JSON file

## Troubleshooting

### Bot doesn't respond to commands

1. Make sure the bot is online (check Discord server member list)
2. Verify the bot has proper permissions (Send Messages, Use Slash Commands)
3. Wait a few minutes after inviting the bot for commands to sync
4. Try kicking and re-inviting the bot if commands don't appear

### Invalid timezone error

Use the IANA timezone format (e.g., `America/New_York`, not `EST`). Find yours at the [timezone database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

### Time parsing errors

- Be specific: "today 3pm" works better than "3pm"
- Use common date formats: "December 25" or "25 Dec" or "2024-12-25"
- For relative times, use: "1 hour", "30 minutes", "2h 15m"

## License

This project is open source and available for personal and commercial use.
