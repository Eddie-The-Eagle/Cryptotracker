#!/usr/bin/env python3

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import io
import json


Client = discord.Client()
client = commands.Bot(command_prefix = "$")


@client.event
async def on_ready():
    print("Bot is online and connected to Discord")


@client.event
async def on_message(message):
	if message.content.upper().startswith('$'):
		args = message.content.split(" ")
		try:
			print(args[0] + args[1])
			coinShort, coinAmount, coinLong, coinPriceUSD, coinPriceBTC, coinValueUSD, coinValueBTC = getPrice(args)
			embed = discord.Embed(title=coinLong + ' (' + coinShort + ')', description= str(coinAmount) + ' ' + str(coinLong) + ' is worth: $' + str(coinValueUSD) + ' or ₿' + str(coinValueBTC), color=0x00ff00)
			await client.send_message(message.channel, embed=embed)
		except:
			coinLong, coinShort, coinRank, coinMarketcap, coinPriceUSD, coinPriceBTC, coinVolume, coinChange1h, coinChange1d, coinChange7d = getTicker(str(message.content).replace('$','').upper())
			embed = discord.Embed(title=coinLong + ' (' + coinShort + ')', description= '**Rank: **' + str(coinRank) + '\n' + '**Marketcap: **' + str(coinMarketcap) + '\n' + '**Volume 24H: **' + str(coinVolume) + '\n\n' + '**Price USD: **' + str(coinPriceUSD) + '\n' + '**Price BTC: **' + str(coinPriceBTC) + '\n\n' + '**Change 1 hour: **' + str(coinChange1h) + '\n' + '**Change 1 day:   **' + str(coinChange1d) + '\n' + '**Change 7 days: **' + str(coinChange7d), color=0x00ff00)
			await client.send_message(message.channel, embed=embed)

def getTicker(coin):
	with io.open('/home/ExchangeData/APIData.json', 'r', encoding='utf8') as outfile:
		outfileRead = outfile.read() 
		dict = json.loads(outfileRead)
		try:
			coinLong = dict[coin]['name'].replace('-', ' ')
			coinShort = dict[coin]['shortname']
			coinRank = str('#' +  str(dict[coin]['rank'])) if dict[coin]['rank'] else '?'
			coinMarketcap = str('$' + str("{:,}".format(round(float(dict[coin]['marketcap']),0)))).replace('.0','') if dict[coin]['marketcap'] else '?'
			coinPriceUSD = '$' + dict[coin]['average_price_USD']
			coinPriceBTC = '₿' + str(round(float(dict[coin]['average_price_BTC']),5)) if float(dict[coin]['average_price_BTC']) > 0.01 else '₿' + str(round(float(dict[coin]['average_price_BTC']),9))
			coinVolume = '$' + str("{:,}".format(round(float(dict[coin]['total_volume']),2)))
			coinChange1h = str(round(float(dict[coin]['percent_change_1h_USD']),2))+ '%' if dict[coin]['percent_change_1h_USD'] else '?'
			coinChange1d = str(round(float(dict[coin]['percent_change_24h_USD']),2))+ '%' if dict[coin]['percent_change_24h_USD'] else '?'
			coinChange7d = str(round(float(dict[coin]['percent_change_7d_USD']),2))+ '%' if dict[coin]['percent_change_7d_USD'] else '?'
			if coinChange1h != '?':
				coinChange1h = str('▼ ' + coinChange1h) if '-' in dict[coin]['percent_change_1h_USD'] else str('▲ ' + coinChange1h)
			if coinChange1d != '?':
				coinChange1d = str('▼ ' + coinChange1d) if '-' in dict[coin]['percent_change_24h_USD'] else str('▲ ' + coinChange1d)
			if coinChange7d != '?':
				coinChange7d = str('▼ ' + coinChange7d) if '-' in dict[coin]['percent_change_7d_USD'] else str('▲ ' + coinChange7d)
			return coinLong, coinShort, coinRank, coinMarketcap, coinPriceUSD, coinPriceBTC, coinVolume, coinChange1h, coinChange1d, coinChange7d
		except Exception as e:
			print(e)
			messageToSend = 'Unknown Coin'
			return messageToSend
		
def getPrice(args):
	coinShort = str(args[0]).replace('$','').upper()
	coinAmount = float(args[1])
	with io.open('/home/ExchangeData/APIData.json', 'r', encoding='utf8') as outfile:
		outfileRead = outfile.read() 
		dict = json.loads(outfileRead)
		coinLong = dict[coinShort]['name'].replace('-', ' ')
		coinPriceUSD = float(dict[coinShort]['average_price_USD'])
		coinPriceBTC = float(dict[coinShort]['average_price_BTC'])
	coinValueUSD = str(round((coinPriceUSD * coinAmount),2))
	coinValueBTC = str(coinPriceBTC * coinAmount)
	return coinShort, coinAmount, coinLong, coinPriceUSD, coinPriceBTC, coinValueUSD, coinValueBTC
		
	

client.run("NDcwMjAwNTExMjk2MTc2MTI4.DjS0EA.JJOk9QeHquRyO95nlaMrz-RCCkI") #Replace token with your bots token
	