import os
from dotenv import load_dotenv
import json
import requests
import discord
from discord.ext import commands


interns = discord.Intents.default()
interns.message_content = True
bot = commands.Bot(command_prefix='!',intents=interns)
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
API = os.getenv("API_KEY")

Warnings = {}

def get_warnings():
    try:
        with open('Warnings.json','r')as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_warnings(warnings):
    with open("warnings.json", "w") as file:
        json.dump(warnings, file, indent=4)

def get_blacklist():
    with open("blacklist.txt", "r") as f:
        return [line.strip().lower() for line in f if line.strip()]
blacklist = []

@bot.event
async def on_ready():
    global blacklist
    blacklist = get_blacklist()

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric'
    response = requests.get(url)
    data = response.json()

    if 'main' in data:
        temp = data['main']['temp']
        typ = data['weather'][0]['main'].lower()
        opis = data['weather'][0]['description']
        emoji_map = {
            'clear': '☀️',
            'clouds': '☁️',
            'rain': '🌧️',
            'drizzle': '🌦️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '🌫️',
            'haze': '🌫️',
            'smoke': '🌫️',
            'dust': '🌪️',
            'sand': '🌪️',

        }
        emoji_type = emoji_map.get(typ,'🌈')
        return temp,emoji_type,opis
    else:
        raise KeyError(f"Can't find city {city}")

@bot.command()
async def weather(ctx, *,city: str):
    try:
        temp,emoji,opis = get_weather(city)
        await ctx.send(f'Current Temperature in {city.capitalize()}: {round(temp)}°C {emoji} - {opis.capitalize()}')
    except Exception as e:
            await ctx.send(f"Something's wrong! ({e})")

@bot.command()
async def clear(ctx, amount: int):
    if amount < 1 or amount > 100:
        await ctx.send('Enter a number between 1 and 100')
        return
    await ctx.channel.purge(limit=amount + 1 )
    await ctx.send(f'{amount} messages deleted!',delete_after=5)

@bot.event
async def on_message(message):
    warnings = get_warnings()
    user_id = str(message.author.id)
    if message.author.bot:
        return
    else:
            if any(slowo in message.content.lower() for slowo in blacklist):
                await message.delete()
                warnings[user_id] = warnings.get(user_id, 0) + 1
                save_warnings(warnings)
                await message.channel.send(f"{message.author}, You receive {warnings[user_id]} Warning(s) !")
                if warnings[user_id] >= 3:
                    if message.author == message.guild.owner:
                        await message.channel.send(f"{message.author} can't be kicked from the server!")
                        warnings[user_id] = 0
                        save_warnings(warnings)
                    else:
                        await message.author.kick(reason='Too many Blacklisted words!')
                        warnings[user_id] = 2
                        save_warnings(warnings)

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx,member:discord.Member, *,reason = None):
    await member.ban(reason=reason)
    if reason == None:
        await ctx.send(f'{member} has been banned!')
    else:
        await ctx.send(f'{member} has been banned for {reason}!')



bot.run(token)