# Discord Bot

## Description
A simple Discord bot written in Python using the discord.py library.  
Features:  
- Detects and deletes messages containing blacklisted words.  
- Warning system with automatic kicking after 3 warnings.  
- Weather command using OpenWeatherMap API.  
- Clear messages command.  
- Ban command for administrators.

## Installation
1. Clone the repository:

```
git clone https://github.com/Neszorro/Discord-bot.git
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a .env file in the project root and add your tokens:
```
DISCORD_TOKEN=your_discord_token
API_KEY=your_openweathermap_api_key
```
# Usage
Run the bot with: 
```
python head.py
```
