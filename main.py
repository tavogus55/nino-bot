import discord
import requests
intents = discord.Intents.all()
client = discord.Client(intents=intents)
from lib.smart_connector import SmartConnector
from lib.ntt_connector import NTTConnector
import json
from datetime import datetime, timedelta  # For time calculations
import asyncio  # For scheduling tasks

def load_config(filename):
    with open(filename, encoding='utf-8') as config_file:
        config = json.load(config_file)
    return config

async def send_dptmail_status():
    """Sends dptmail status at scheduled times."""
    await client.wait_until_ready()  # Ensures the bot is logged in
    CONFIG = load_config('config.json')
    SMART_CONNECTOR = SmartConnector(CONFIG['DPT'])
    RASPBERRYPI_MODE = CONFIG['RaspberryPi']
    channel_id = CONFIG['channel_id']  # Add the channel ID to config.json
    channel = client.get_channel(channel_id)
    user_id = CONFIG['user_id']

    while not client.is_closed():
        now = datetime.now()
        # Schedule times (8 AM, 12 PM, 6 PM)
        schedule_times = [8, 12, 18]
        next_run = min(
            (datetime(now.year, now.month, now.day, t) for t in schedule_times if t > now.hour),
            default=datetime(now.year, now.month, now.day + 1, schedule_times[0])
        )
        # Calculate the wait time until the next run
        wait_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        # Perform the dptmail task
        unopenedEmailsNumber = SMART_CONNECTOR.getUnreadEmails(RASPBERRYPI_MODE)
        if unopenedEmailsNumber > 0:
            message = f'<@{user_id}> You have {unopenedEmailsNumber} new emails!'
            if channel:
                await channel.send(message)
            else:
                print("Channel not found or not configured.")
        else:
            print("No new emails.")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'Nino!' in message.content:
        await message.channel.send('What do you want Uesugi-kun?')

    if 'dptmail' in message.content:
        await message.channel.send('S..ure! give me a second')
        CONFIG = load_config('config.json')
        RASPBERRYPI_MODE = CONFIG['RaspberryPi']
        SMART_CONNECTOR = SmartConnector(CONFIG['DPT'])
        unopenedEmailsNumber = SMART_CONNECTOR.getUnreadEmails(RASPBERRYPI_MODE)
        await message.channel.send('You have ' + str(unopenedEmailsNumber) + ' new emails')

    if 'payntt' in message.content:
        await message.channel.send('S..ure! give me a second')
        CONFIG = load_config('config.json')
        NTT_CONNECTOR = NTTConnector(CONFIG['NTT_billing'])
        NTT_CONNECTOR.payBill()
        await message.channel.send('Bill is paid')

    if message.content.startswith('chuck'):
        response = requests.get('https://api.chucknorris.io/jokes/random')
        if response.status_code == 200:
            data = response.json()
            joke = data['value']
            if joke:
                await message.channel.send(joke)
                print('Joke sent: {0}'.format(joke))
            else:
                print('Joke is empty')
        else:
            print('Error getting joke: {0}'.format(response.status_code))

CONFIG = load_config('config.json')
token = CONFIG['token']
client.run(token)