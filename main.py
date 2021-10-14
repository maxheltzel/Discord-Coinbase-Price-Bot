import random
import requests
from discord.ext import commands
import json
from datetime import datetime, time

token = 'ODk4MjI3MTI1NTc0ODU2NzM0.YWhJMg.VZ4mHvxd7aeKMHB1Qof-mHWpHb4'
client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot is online")

@client.command(pass_context=True)
async def ping(ctx):
    await ctx.channel.send('Pong!')


@client.command(aliases=['8ball', 'Biggest Bobs'])
async def _8ball(ctx, *, question):
    responses = ['It is Certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes definitely.', 'You may rely on it.',
                 'As I see it, yes.', 'Most likely.', 'Yes', 'Signs point to yes.','My reply is no.', 'My sources say no.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

delay = 1800  # seconds
discordWebhook = 'https://discord.com/api/webhooks/898307388321443901/KP9V8WsbETC547PS-sB8avCWQJo0mZjAzTSO9Idv2yuN6DLqmKldpTy1srrlVx7kIHVH'

def getPrice(currency):
    priceUrl = 'https://api.coinbase.com/v2/prices/{}-USD/spot'.format(currency)
    r = requests.get(priceUrl)
    r = json.loads(r.text)
    return r['data']['amount']

@client.command(pass_context=True)
async def coin(ctx, *, coin_name):
    while True:
        coin_price = getPrice(coin_name.upper())
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
        embeds = [{
            'type': 'rich',
            "color": 0xf1c40f,
            "timestamp": timestamp,
            "fields": [{"name": f"{coin_name.upper()}", "value": "$" + str(coin_price), "inline": True}]
        }]
        payload = {"embeds": embeds}
        r = requests.post(discordWebhook, json=payload)
        time.sleep(delay)
        await ctx.send(r)

client.run(token)