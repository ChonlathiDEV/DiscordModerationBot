import discord
import requests
import json

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
TYPHOON_API_URL = "https://api.typhoon.ai/moderation"
TYPHOON_API_KEY = "YOUR_TYHOON_API_KEY"

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

def check_with_typhoon(text):
    headers = {"Authorization": f"Bearer {TYPHOON_API_KEY}"}
    payload = {"text": text}
    response = requests.post(TYPHOON_API_URL, headers=headers, json=payload)
    result = response.json()
    return result.get("label"), result.get("score")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    label, score = check_with_typhoon(message.content)

    if label in ["toxic", "bullying"] and score > 0.8:
        await message.delete()
        await message.channel.send(
            f"⚠️ ข้อความของ {message.author.mention} ถูกลบเพราะเข้าข่าย {label}"
        )

client.run(TOKEN)
