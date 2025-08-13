import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
import json
import tweepy
import re

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bearer_token = os.getenv('bearer_token')
bearertokendobby = os.getenv('bearertokendobby')

client = tweepy.Client(bearer_token)

def get_first_link(text):
  regex = r"https?://\S+"
  match = re.search(regex, text)
  if match:
    return match.group(0)
  else:
    return None

def extract_tweet_id(url):
    match = re.search(r"x\.com/[^/]+/status/(\d+)", url)
    if match:
        return match.group(1)
    else:
        return None

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Ready!')

@bot.command()
async def dobby(ctx, *, msg):
    payload = {
        "model": "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new",
        "max_tokens": 16384,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": f"{msg}"
            }
        ]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearertokendobby}"
    }
    response = requests.request("POST", "https://api.fireworks.ai/inference/v1/chat/completions", headers=headers,
                                data=json.dumps(payload))
    if response.status_code == 200:
        data = json.loads(response.text)
        answer = data.get('choices', [{}])[0].get('message', {}).get('content', 'Unable to get response from AI')
        await ctx.reply(answer)
    else:
        print(f"Error {response.status_code}: {response.text}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)