import io
import json
import os
import re
import requests
import platform

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

OS = platform.system()
if OS == 'Windows':
	prePath = 'D:\\ExchangeData\\'
elif OS == 'Linux':
	prePath = '/home/ExchangeData/'
	

r = requests.head('https://api.coinmarketcap.com/v1/ticker/?limit=5000')
if r.status_code != 200:
	print('https://api.coinmarketcap.com/v1/ticker/?limit=5000')
	data = '{}'
else:
	request = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=5000')
	try:
		data = request.json()
	except:
		data = '{}'
request.close()
r.close()

coinCount = 0
for i in data:
	coinCount += 1
	
with io.open(prePath + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
	outfileShortRead = outfileShort.read() 
	ShortList = json.loads(outfileShortRead)

def circSupply():
	for k1 in ShortList:
		if ShortList[k1]['Circulating Supply'] == '':
				coinLong = ShortList[k1]['Name'].lower()
				for i in range(0, coinCount):
					if coinLong in str(data[i]):
						circsupply = str(data[i]['available_supply'])
						if circsupply == 'None':
							ShortList[k1]['Circulating Supply'] = '?'
						else:
							ShortList[k1]['Circulating Supply'] = str(circsupply)
						break
					else:
						ShortList[k1]['Circulating Supply'] = '?'
			
circSupply()

def maxSupply():
	for k1 in ShortList:
		if ShortList[k1]['Max Supply'] == '':
				coinLong = ShortList[k1]['Name'].lower()
				for i in range(0, coinCount):
					if coinLong in str(data[i]):
						maxsupply = str(data[i]['max_supply'])
						if maxsupply == 'None':
							ShortList[k1]['Max Supply'] = '?'
						else:
							ShortList[k1]['Max Supply'] = str(maxsupply)
						break
					else:
						ShortList[k1]['Max Supply'] = '?'

maxSupply()

class specificCoins(object):
	def Bitcoin(self):
		data = getJSON('https://api.blockchain.info/stats')
		ShortList['BTC']['Circulating Supply'] = str(int((round((float(data['totalbc']) / 100000000),0))))
		self.Ethereum()

	def Ethereum(self):
		data = getJSON('https://api.etherscan.io/api?module=stats&action=ethsupply')
		ShortList['ETH']['Circulating Supply'] = str(int((round((float(data['result']) / 1000000000000000000),0))))
		self.Litecoin()
		
	def Litecoin(self):
		data = getJSON('https://chainz.cryptoid.info/ltc/api.dws?q=totalcoins')
		ShortList['LTC']['Circulating Supply'] = str(int(round(data, 0)))
	
		
def getJSON(URL):
	r = requests.head(URL)
	if r.status_code != 200:
		data = '{}'
	else:
		request = requests.get(URL)
		try:
			data = request.json()
		except:
			data = '{}'
		request.close()
	r.close()
	return data
	
specificCoins().Bitcoin()

def WriteToFile():
	with io.open(prePath + 'APIShort.json', 'w', encoding='utf8') as outfileShort:
		str_ = json.dumps(ShortList,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
		outfileShort.write(to_unicode(str_))
		
WriteToFile()