#!/usr/bin/env python3
from collections import OrderedDict
import requests
import json
import io
import re
import time
import datetime
import os
import sys
import platform
from pathlib import Path
import threading


try:
    to_unicode = unicode
except NameError:
    to_unicode = str


class GetFilePath():
	def get_main_directory(self):
		"""Gets the main directory for all files depends on OS"""
		if platform.system() == 'Linux':
			mainDirPath = '/home/ExchangeData/'
		else:
			mainDirPath = 'D:\\ExchangeData\\'
		return mainDirPath

	def get_timed_filepath(self, mainDirPath):
		"""Gets the filepaths to old files required for price changes"""
		currentTime = datetime.datetime.now()
		currentTime = datetime.datetime(currentTime.year, currentTime.month, currentTime.day, currentTime.hour, 15*(currentTime.minute // 15))
		timeList, filePathList = ([], [])
		timeList.extend([currentTime + datetime.timedelta(hours=-1), currentTime + datetime.timedelta(days=-1), currentTime + datetime.timedelta(days=-7)])
		for item in timeList:
			filePathList.append(mainDirPath + str(str(item.strftime("%Y")) + '/' + str(item.strftime("%m")) + "/" + str(item.strftime("%d")) + "/" + str(item.strftime("%H")) + str(item.strftime("%M"))+'.json'))
		return currentTime, filePathList

	def check_filepath(self, currentTime, mainDirPath):
		"""Checks if the directory for the new file exists"""
		newFilePath = mainDirPath + str(currentTime.strftime("%Y")) + '/' + str(currentTime.strftime("%m")) + "/" + str(currentTime.strftime("%d")) + "/" + str(currentTime.strftime("%H")) +  str(currentTime.strftime("%M"))+'.json'
		check = os.path.dirname(newFilePath)
		if not os.path.exists(check):
			os.makedirs(check)
		return newFilePath

class FileManagement():
	def write_JSON_file(self, filePath, data):
		"""Write data to a file"""
		data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
		data = re.sub(r'\d\d_', '', data)
		with io.open(filePath, 'w', encoding='utf8') as fileToWrite:
			fileToWrite.write(to_unicode(data))

	def open_JSON_file(self, filePath, option):
		"""Opens a file and returns the data inside"""
		# print('requested opening of file ' + str(filePath))
		with io.open(filePath, 'r', encoding='utf8') as data:
			dataReadable = data.read()
			dataList = json.loads(dataReadable)
			if option == 0:
				return dataReadable, dataList
			if option == 1:
				return dataList
			if option == 2:
				return dataReadable
			
class NetworkRequest():
	def make_API_call(self, URL, error):
		"""Makes a call to an API and returns the data in JSON format"""
		request = requests.get(URL)
		if request.status_code == 200:
			data = request.json()
			request.close()
			return data
		else:
			if error <= 2:
				time.sleep(1)
				error += 1
				self.make_API_call(URL, error)
			else:
				error = 0
				data = '{}'
				return data
				
class coinPairs():
	def check_new_pairs(self, tradingPairs, URL, coinPair, counter, exchange, pairsUpdated):
		"""Checks if an exchange listed new trading pairs"""
		data = NetworkRequest().make_API_call(URL, 0)
		linesCounted = sum(1 for line in eval(counter))
		if exchange == 'Huobi':
			linesCounted -= 2
		for i in range(0, linesCounted):
			tradingPair = eval(coinPair)
			if tradingPair not in tradingPairs: # Might need and tradingpair.isalpha()
				tradingPairs.append(tradingPair)
				pairsUpdated = 1
		return tradingPairs, pairsUpdated
	
	def get_coinPair_prices(self, tickerURL, tradingPairs, tickerPrice):
		"""Gets the prices of tradingpairs on a exchange or from our data"""
		priceList = []
		priceData = FileManagement().open_JSON_file(mainDirPath + 'APIData.json', 1)
		for coin in tradingPairs:
			try:
				data = NetworkRequest.make_API_call(eval(tickerURL), 0)
				priceList.append(eval(tickerPrice))
			except:
				try:
					priceList.append(float(priceData[coin]['average_price_USD'].replace(',', '')))
				except:
					priceList.append(float(1))
		pairPriceDict = {}
		for count, item in enumerate(tradingPairs):
			pairPriceDict[str(tradingPairs[count])] = priceList[count]
		return pairPriceDict
		
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
			
class GetExchangeData():
	def main(self, URL, counter, getCoinTicker, getCoinName, getCoinPair, getCoinPrice, getCoinVolume, pairPrices, exchange, dict):
		exchangeVolume, exchangeTradingPairs = 0, 0
		data = NetworkRequest().make_API_call(URL, 0)
		if data != None:
			shortReadable, shortData = FileManagement().open_JSON_file(mainDirPath + 'APIShort.json', 0)
			if exchange == 'IDEX':
				dataList = []
				for line in data:
					dataList.append(line)
			linesCounted = sum(1 for line in eval(counter))
			if exchange == 'Huobi':
				linesCounted -= 2
			for i in range(0, linesCounted):
				coinPair = eval(getCoinPair)
				if coinPair not in pairPrices:
					continue
				coinTicker = eval(getCoinTicker) 
				if str('"' + coinTicker + '"') in shortReadable and '?' not in shortData[coinTicker]['Name']:
					coinName = str(shortData[coinTicker]['Name'])
				else:
					if shortData[coinTicker]['Name'] == '?':
						continue
					else:
						try:
							coinName = eval(getCoinName).replace(' ', '-')
						except:
							coinName = '?????'
						if '?' not in coinName and str('"' + coinName + '"') in shortReadable:
							coinTicker = str(str([shortData[item]['Short'] for item in shortData if shortData[item]['Name'] == coinName]).replace("['", "")).replace("']", "")
						else:
							print(str(shortData[coinTicker]['Name']))
							if str('"' + coinTicker + '"') in shortReadable and '??' in str(shortData[coinTicker]['Name']):
								coinName = shortData[coinTicker]['Name'][:-1]
								UpdateData().coin_info_add_coin(coinTicker, coinName)
								continue
							else:
								UpdateData().coin_info_add_coin(coinTicker, coinName)
								continue
				try:
					coinPrice = float(eval(getCoinPrice)) * float(pairPrices[coinPair])
					coinVolume = float(eval(getCoinVolume)) * float(pairPrices[coinPair])
				except:
					continue
				if coinVolume == '0.0':
					continue
				exchangeVolume += coinVolume
				exchangeTradingPairs += 1
				dict.append(coinTicker + ' ' + coinName + ' ' + coinPair + ' ' + str(coinPrice) + ' ' + str(coinVolume) + ' ' + exchange)
			UpdateData().exchange_stats(exchange, exchangeVolume, exchangeTradingPairs, dict)
			if dict != '{}':
				ExchangeList.append(dict)	
	
class UpdateData():
	def coin_info_add_coin(self, coinTicker, coinName):
		dataList = FileManagement().open_JSON_file(mainDirPath + 'APIShort.json', 1)
		dataDict = {}
		dataDict['Name'] = coinName
		dataDict['Ticker'] = coinTicker
		dataDict['Website'] = '?'
		dataDict['Explorer'] = '?'
		dataDict['Github'] = '?'
		dataDict['Twitter'] = '?'
		dataDict['Reddit'] = '?'
		dataDict['Discord'] = '?'
		dataDict['Bitcointalk'] = '?'
		dataDict['Circulating Supply'] = '?'
		dataDict['Max Supply'] = '?'
		dataList[coinTicker] = dataDict
		FileManagement().write_JSON_file(mainDirPath + 'APIShort.json', dataList)
	
	def exchange_stats(self, exchange, exchangeVolume, exchangeTradingPairs, coinData):
		dataList = FileManagement().open_JSON_file(mainDirPath + 'ExchangeMarketStats.json', 1)
		try:
			exchangeDict = dataList[exchange]
			pairDict = exchangeDict['TradingPairs']
		except:
			exchangeDict, pairDict = {}, {}
			dataList[exchange] = exchangeDict
		for coin in coinData:
			coinDict = {}
			splitline = coin.split()
			coinDict['volume'] = int("{:.0f}".format(round(float(splitline[4]), 0)))
			coinDict['price_USD'] = splitline[3]
			coinDict['lastUpdated'] = str(currentTime)
			pairDict[splitline[0] + '/' + splitline[2]] = coinDict
		exchangeDict['tradeVolumeUSD'] = exchangeVolume
		exchangeDict['lastUpdated'] = str(currentTime)
		exchangeDict['tradingPairs'] = pairDict
		exchangeDict['amountOfTradingPairs'] = exchangeTradingPairs
		dataList[exchange] = exchangeDict
		FileManagement().write_JSON_file(mainDirPath + 'ExchangeMarketStats.json', dataList)
		
	def market_stats(self, data): # still needs to be rewritten
		marketStats = {}
		marketStats['TotalMarketcap'], marketStats['TotalVolume'], marketStats['BTCDominance'] = (int(), int(), int())
		for coin in data:
			if data[coin]['marketcap'] != "":
				marketStats['TotalMarketcap'] += int(data[coin]['marketcap'])
			marketStats['TotalVolume'] += int(data[coin]['total_volume'])
		marketStats['BTCDominance'] = str("{:.2f}".format(round((100 - ((int(marketStats['TotalMarketcap']) - int(data['BTC']['marketcap'])) / int(marketStats['TotalMarketcap']) * 100)), 2)))
		marketStats['TotalMarketcap'] = "{:,}".format(int(marketStats['TotalMarketcap']))
		marketStats['TotalVolume'] = "{:,}".format(int(marketStats['TotalVolume']))
		FileManagement().write_JSON_file(mainDirPath + 'APIMarketStats.json', marketStats)
		
	def updateJSONFile(self, newData):
		ShortList = FileManagement().open_JSON_file(mainDirPath + 'APIData.json', 1)
		for coin in ShortList:
			ShortList[coin]['rank'], ShortList[coin]['marketcap'], ShortList[coin]['total_volume'], ShortList[coin]['percent_change_1h_USD'], ShortList[coin]['percent_change_24h_USD'], ShortList[coin]['percent_change_7d_USD'], ShortList[coin]['percent_change_1h_BTC'], ShortList[coin]['percent_change_24h_BTC'], ShortList[coin]['percent_change_7d_BTC'] = '', '', '', '', '', '', '', '', ''
		ShortList.update(newData)
		for coin in ShortList:
			ShortList[coin]['00_name'] = ShortList[coin]['name']
			ShortList[coin]['01_shortname'] = ShortList[coin]['shortname']
			ShortList[coin]['02_rank'] = ShortList[coin]['rank']
			ShortList[coin]['03_marketcap'] = ShortList[coin]['marketcap']
			ShortList[coin]['04_total_volume'] = ShortList[coin]['total_volume']
			ShortList[coin]['05_average_price_USD'] = ShortList[coin]['average_price_USD']
			ShortList[coin]['06_average_price_BTC'] = ShortList[coin]['average_price_BTC']
			ShortList[coin]['07_percent_change_1h_USD'] = ShortList[coin]['percent_change_1h_USD']
			ShortList[coin]['08_percent_change_24h_USD'] = ShortList[coin]['percent_change_24h_USD']
			ShortList[coin]['09_percent_change_7d_USD'] = ShortList[coin]['percent_change_7d_USD']
			ShortList[coin]['10_percent_change_1h_BTC'] = ShortList[coin]['percent_change_1h_BTC']
			ShortList[coin]['11_percent_change_24h_BTC'] = ShortList[coin]['percent_change_24h_BTC']
			ShortList[coin]['12_percent_change_7d_BTC'] = ShortList[coin]['percent_change_7d_BTC']
			del ShortList[coin]['name'], ShortList[coin]['shortname'], ShortList[coin]['rank'], ShortList[coin]['marketcap'], ShortList[coin]['total_volume'], ShortList[coin]['average_price_USD'], ShortList[coin]['average_price_BTC'], ShortList[coin]['percent_change_1h_USD'], ShortList[coin]['percent_change_24h_USD'], ShortList[coin]['percent_change_7d_USD'], ShortList[coin]['percent_change_1h_BTC'], ShortList[coin]['percent_change_24h_BTC'], ShortList[coin]['percent_change_7d_BTC']
		FileManagement().write_JSON_file(mainDirPath + 'APIData.json', ShortList)

	def jsonify_exchanges_dict(self): # still needs to be rewritten
		coinname, oldcoinname, ShortList, exchangename, tradingdata, data, tradingpair, ExchangeData = ({}, {}, {}, {}, {}, {}, {}, {})
		ExchangeDir = []
		for item in ExchangeList:
			ExchangeDir = ExchangeDir + item
			ExchangeDir.sort()
		ExchangeData = ExchangeDir
		ExchangeData.sort()
		for k in ExchangeData:
			splitline = k.split()
			if splitline[0] in coinname:
				volume = int("{:.0f}".format(round(float(splitline[4]),0)))
				tradingdata = {}
				olddata = data
				tradingdata['PriceUSD'] = splitline[3]
				tradingdata['TradeVolumeUSD'] = volume
				tradingdata['LastUpdated'] = str(currentTime)
				tradingpair[str(splitline[0] + '/' + splitline[2])] = tradingdata
				try:
					exchangename[splitline[5]] = {**exchangename[splitline[5]], **tradingpair}
				except:
					exchangename[splitline[5]] = tradingpair
				data['exchange_data'] = {**data['exchange_data'],  **exchangename}
				data['total_volume'] = str(int(data['total_volume']) + volume)
				coinname[splitline[0]] = {**olddata, **data}
				tradingpair  = {}
			else:
				data = {}
				exchangename = {}
				tradingdata = {}
				volume = int("{:.0f}".format(round(float(splitline[4]),0)))
				tradingdata['PriceUSD'] = splitline[3]
				tradingdata['TradeVolumeUSD'] = str(volume)
				tradingdata['LastUpdated'] = str(currentTime)
				tradingpair[str(splitline[0] + '/' + splitline[2])] = tradingdata
				exchangename[splitline[5]] = tradingpair
				data['name'] = splitline[1]
				data['shortname'] = splitline[0]
				data['rank'] = ''
				data['marketcap'] = ''
				data['total_volume'] = str(volume)
				data['average_price_USD'] = ''
				data['average_price_BTC'] = ''
				data['percent_change_1h_USD'] = ''
				data['percent_change_24h_USD'] = ''
				data['percent_change_7d_USD'] = ''
				data['percent_change_1h_BTC'] = ''
				data['percent_change_24h_BTC'] = ''
				data['percent_change_7d_BTC'] = ''
				data['exchange_data'] = exchangename
				tradingpair  = {}
				coinname[splitline[0]] = data
		for k1 in coinname:
			NumberTrades, TotalPrice = (float(), float())
			for k2 in coinname[k1]['exchange_data']:
				for k3 in coinname[k1]['exchange_data'][k2]:
					TradeVolumeUSD = float(coinname[k1]['exchange_data'][k2][k3]['TradeVolumeUSD'])
					if TradeVolumeUSD <= 0.1:
						pass
					else:
						TotalVolumeUSD = float(coinname[k1]['total_volume'])
						if TotalVolumeUSD <= 0.1:
							pass
						else:
							averagePrice = float(coinname[k1]['exchange_data'][k2][k3]['PriceUSD'])
							VolumePerc = float(float(TradeVolumeUSD) / float(TotalVolumeUSD))
							TotalPrice = TotalPrice + float(averagePrice * VolumePerc)
			if TotalPrice == 0:
				for k3 in coinname[k1]['exchange_data'][k2]:
					averagePrice = float(coinname[k1]['exchange_data'][k2][k3]['PriceUSD'])
					TotalPrice = TotalPrice + averagePrice
					NumberTrades += float(1)
				TotalPrice = str(TotalPrice / NumberTrades)
			coinname[k1]['average_price_USD'] = TotalPrice
		for k1 in coinname:
			coinname[k1]['average_price_BTC'] = round(float(float(coinname[k1]['average_price_USD']) / float(coinname['BTC']['average_price_USD'])), 9)
		if StatusCode != 0:
			if Path(filePathList[0]).exists():
				ShortList = FileManagement().open_JSON_file(filePathList[0], 1)
				List1h = ShortList
			if Path(filePathList[1]).exists():
				ShortList = FileManagement().open_JSON_file(filePathList[1], 1)
				List1d = ShortList
			if Path(filePathList[2]).exists():
				ShortList = FileManagement().open_JSON_file(filePathList[2], 1)
				List7d = ShortList
			for k1 in coinname: 
				try:
					coinname[k1]['percent_change_1h_USD'] = str(str("{:.2f}".format(round((float(coinname[k1]['average_price_USD']) - float(str(List1h[k1]['average_price_USD']).replace(',',''))) / float(str(List1h[k1]['average_price_USD']).replace(',','')) * 100,2))))
					coinname[k1]['percent_change_1h_BTC'] = str(str("{:.2f}".format(round((float(coinname[k1]['average_price_BTC']) - float(str(List1h[k1]['average_price_BTC']).replace(',',''))) / float(str(List1h[k1]['average_price_BTC']).replace(',','')) * 100,2))))
				except:
					pass
				try:
					coinname[k1]['percent_change_24h_USD'] = str(str("{:.2f}".format(round((float(coinname[k1]['average_price_USD']) - float(str(List1d[k1]['average_price_USD']).replace(',',''))) / float(str(List1d[k1]['average_price_USD']).replace(',','')) * 100,2))))
					coinname[k1]['percent_change_24h_BTC'] = str(str("{:.2f}".format(round((float(coinname[k1]['average_price_BTC']) - float(str(List1d[k1]['average_price_BTC']).replace(',',''))) / float(str(List1d[k1]['average_price_BTC']).replace(',','')) * 100,2))))
				except:
					pass
				try:
					coinname[k1]['percent_change_7d_USD'] = str(str("{:.2f}".format(round((float(coinname[k1]['average_price_USD']) - float(str(List7d[k1]['average_price_USD']).replace(',',''))) / float(str(List7d[k1]['average_price_USD']).replace(',','')) * 100,2))))
					coinname[k1]['percent_change_7d_BTC'] = str(str("{:.2f}".format(round((float(coinname[k1]['average_price_BTC']) - float(str(List7d[k1]['average_price_BTC']).replace(',',''))) / float(str(List7d[k1]['average_price_BTC']).replace(',','')) * 100,2))))
				except:
					pass
			ShortList = FileManagement().open_JSON_file(mainDirPath + 'APIShort.json', 1)
			for k1 in coinname:
				try:
					coinname[k1]['marketcap'] = "{:.0f}".format(round((float(ShortList[k1]['Circulating Supply']) * float(coinname[k1]['average_price_USD'])),0))
				except Exception as e:
					pass
			marketRank = {}
			for k1 in coinname:
				if coinname[k1]['marketcap'] != '':
					marketRank[k1] = float(coinname[k1]['marketcap'])
				else:
					marketRank[k1] = 0
			sortedDict = sorted(((value, key) for (key,value) in marketRank.items()),reverse=True)
			rankNumber = 0
			for key in sortedDict:
				rankNumber += 1
				coinname[key[1]]['rank'] = rankNumber
		for coin in coinname:
			if float(coinname[coin]['average_price_USD']) >= 0.99:
				coinname[coin]['average_price_USD'] = "{:,.2f}".format(round(float(coinname[coin]['average_price_USD']),2))
			else:
				coinname[coin]['average_price_USD'] = "{:.5f}".format(round(float(coinname[coin]['average_price_USD']),5))
		if StatusCode == 2:
			self.market_stats(coinname)
		self.updateJSONFile(coinname)
		if StatusCode != 0:
			FileManagement().write_JSON_file(newFilePath, coinname)
		
class runScript():
	def exchanges(self, exchange):
		mainTickerURL = dataList[exchange]['mainTickerURL']
		tickerURL = dataList[exchange]['tickerURL']
		tickerPrice = dataList[exchange]['tickerPrice']
		tradingPairs = eval(dataList[exchange]['tradingPairs'])
		counter = dataList[exchange]['counter']
		coinPair = dataList[exchange]['coinPair']
		coinName = dataList[exchange]['coinName']
		coinTicker = dataList[exchange]['coinTicker']
		coinPrice = dataList[exchange]['coinPrice']
		coinVolume = dataList[exchange]['coinVolume']
		dict = []
		if checkForPairs == 1:
			pairsUpdated = 0
			tradingPairs, pairsUpdated = coinPairs().check_new_pairs(tradingPairs, mainTickerURL, coinPair, counter, exchange, pairsUpdated)
			dataList[exchange]['tradingPairs'] = str(tradingPairs)
			tradingPairs = eval(dataList[exchange]['tradingPairs'])
			if pairsUpdated == 1:
				FileManagement().write_JSON_file(mainDirPath + 'ExchangeInfo.json', dataList)
		pairPrices = coinPairs().get_coinPair_prices(tickerURL, tradingPairs, tickerPrice)
		GetExchangeData().main(mainTickerURL, counter, coinTicker, coinName, coinPair, coinPrice, coinVolume, pairPrices, exchange, dict)
		
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################
# ############################################################################################################################################################

StatusCode = 0
start_time = time.time()
mainDirPath = GetFilePath().get_main_directory()
currentTime, filePathList = GetFilePath().get_timed_filepath(mainDirPath)
newFilePath = GetFilePath().check_filepath(currentTime, mainDirPath)
ExchangeList = []

if (currentTime.hour / 6).is_integer() and currentTime.minute == 0:
	checkForPairs = 1
else:
	checkForPairs = 0

dataList = FileManagement().open_JSON_file(mainDirPath + 'ExchangeInfo.json', 1)
StatusCode = 1

threadsList = []
for exchange in eval(dataList['exchangeLists']['mainExchanges']):
	t = threading.Thread(target = runScript().exchanges, args = (exchange,))
	threadsList.append(t)
	t.start()

for t in threadsList:
	t.join()
	

UpdateData().jsonify_exchanges_dict()
StatusCode = 0 

threadsList = []
for exchange in eval(dataList['exchangeLists']['otherExchanges']): # Still need to change cryptopia way to get names (load the URL json file only once)
	t = threading.Thread(target = runScript().exchanges, args = (exchange,))
	threadsList.append(t)
	t.start()

for t in threadsList:
	t.join()

StatusCode = 2 
UpdateData().jsonify_exchanges_dict()

print("--- %s seconds ---" % (time.time() - start_time))
time.sleep(900 - (time.time() - start_time))
os.execv(sys.executable, [sys.executable] + sys.argv)

