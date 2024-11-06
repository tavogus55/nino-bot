import discord
import requests
intents = discord.Intents.all()
client = discord.Client(intents=intents)
from lib.smart_connector import SmartConnector
from lib.ntt_connector import NTTConnector
import json


def load_config(filename):
    with open(filename, encoding='utf-8') as config_file:
        config = json.load(config_file)
    return config

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