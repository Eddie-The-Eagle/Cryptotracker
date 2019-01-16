from django.shortcuts import render
from django.http import HttpResponse
import io
import json
from pathlib import Path
import datetime

def coinPage(request, coinLong):
	with io.open('/home/ExchangeData/' + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
		outfileShortRead = outfileShort.read() 
		ShortList = json.loads(outfileShortRead)
		for item in ShortList:
			if ShortList[item]['Name'] == coinLong:
				coin = item
		coinShort = coin
		coinAmount = 0
		coinAmount = len(ShortList)
		try:
			coinCircSupply = "{:,}".format(int(round(float(ShortList[coin]['Circulating Supply']),0)))
		except:
			coinCircSupply = '?'
		try:
			coinMaxSupply = "{:,}".format(int(round(float(ShortList[coin]['Max Supply']),0)))
		except:
			coinMaxSupply = '?'
		coinWebsite = 'https://'+ ShortList[coin]['Website'] if ShortList[coin]['Website'] != '?' and ShortList[coin]['Website'] != '' else ''
		coinExplorer = 'https://'+ ShortList[coin]['Explorer'] if ShortList[coin]['Explorer'] != '?' and ShortList[coin]['Explorer'] != '' else ''
		coinBitcoinTalk = 'https://'+ ShortList[coin]['Bitcointalk'] if ShortList[coin]['Bitcointalk'] != '?' and ShortList[coin]['Bitcointalk'] != '' else ''
		coinGithub = 'https://github.com/'+ ShortList[coin]['Github'] if ShortList[coin]['Github'] != '?' and ShortList[coin]['Github'] != '' else ''
		coinTwitter = 'https://Twitter.com/'+ ShortList[coin]['Twitter'] if ShortList[coin]['Twitter'] != '?' and ShortList[coin]['Twitter'] != '' else ''
		coinReddit = 'https://Reddit.com/r/'+ ShortList[coin]['Reddit'] if ShortList[coin]['Reddit'] != '?' and ShortList[coin]['Reddit'] != '' else ''
		coinDiscord = 'https://Discord.com/'+ ShortList[coin]['Discord'] if ShortList[coin]['Discord'] != '?' and ShortList[coin]['Discord'] != '' else ''
	with io.open('/home/ExchangeData/' + 'APIData.json', 'r', encoding='utf8') as outfileData:	
		outfileDataRead = outfileData.read() 
		DataList = json.loads(outfileDataRead)
		try:
			coinPriceUSD = str(DataList[coin]['average_price_USD'])
		except:
			coinPriceUSD = ''
		try:
			coinPriceBTC = DataList[coin]['average_price_BTC']
		except:
			coinPriceBTC = ''
		try:
			coinVolume = "{:,}".format(int(round(float(DataList[coin]['total_volume']),0)))
		except:
			coinVolume = '0'
		try:
			coinMarketcap = "{:,}".format(int(round(float(DataList[coin]['marketcap']),0)))
		except:
			coinMarketcap = '?'
		if DataList[coin]['percent_change_24h_USD'] != '':
			percent_change_24h_USD = DataList[coin]['percent_change_24h_USD']
			if '-' not in str(percent_change_24h_USD):
				percent_change_24h_USD = DataList[coin]['percent_change_24h_USD']
			else:
				percent_change_24h_USD = DataList[coin]['percent_change_24h_USD']
		else:
			percent_change_24h_USD = ''
		if DataList[coin]['percent_change_24h_BTC'] != '':
			percent_change_24h_BTC = DataList[coin]['percent_change_24h_BTC']
			if '-' not in str(percent_change_24h_BTC):
				percent_change_24h_BTC = DataList[coin]['percent_change_24h_BTC']
			else:
				percent_change_24h_BTC = DataList[coin]['percent_change_24h_BTC']
		else:
			percent_change_24h_BTC = ''
		coinMarketsList = []
		CoinExchangeData = []
		try:
			for Exchange in DataList[coin]['exchange_data']:
				for coinPair in DataList[coin]['exchange_data'][Exchange]:
					coinMarketsList.append(Exchange)
					coinMarketsList.append(coinPair)
					coinMarketsList.append('$' + str("{:,}".format(round(float(DataList[coin]['exchange_data'][Exchange][coinPair]['PriceUSD']),2))))
					coinMarketsList.append('$' + str("{:,}".format(int(round(float(DataList[coin]['exchange_data'][Exchange][coinPair]['TradeVolumeUSD']),0)))))
					try:
						timenotUpdated = (datetime.datetime.strptime(DataList[coin]['exchange_data'][Exchange][coinPair]['LastUpdated'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()) / datetime.timedelta(minutes=1)
						if timenotUpdated >= 60:
							timenotUpdated = int(round((timenotUpdated / 60),0))
							if timenotUpdated <= 2:
								timenotUpdated = str(timenotUpdated).replace('-','') + ' hours ago'
							else:
								timenotUpdated = str(timenotUpdated).replace('-','') + ' hour ago'
						else:
							timenotUpdated = int(round(timenotUpdated,0))
							if timenotUpdated <= 2:
								timenotUpdated = str(timenotUpdated).replace('-','') + ' minutes ago'
							else:
								timenotUpdated = str(timenotUpdated).replace('-','') + ' minute ago'
						coinMarketsList.append(str(timenotUpdated))
					except Exception as e:
						coinMarketsList.append(str(e))
					CoinExchangeData.append(coinMarketsList)
					coinMarketsList = []
		except:
			pass
		CoinimgPath = Path("/home/mysite/coininfo/static/coininfo/img/coinLogos/" + coin + ".png")
		if CoinimgPath.is_file():
			coinImage = '<img class="d-block img-fluid" src="/static/coininfo/img/coinLogos/' + coin +'.png" width="140" height="140">'
		else:
			coinImage = '<img class="d-block img-fluid" src="/static/coininfo/img/coinLogos/UnknownCoin.png" width="140" height="140">'
		tbl = CoinExchangeData
		cols = ["<td>{0}</td>". format( "</td><td>".join(t)  ) for t in tbl]
		coinExchangeTable = "<tr>{0}</tr>".format( "</tr>\n<tr>".join(cols))
		
		with io.open('/home/ExchangeData/' + 'APIMarketStats.json', 'r', encoding='utf8') as outFileMarketStats:	
			outFileMarketStatsRead = outFileMarketStats.read() 
			outFileMarketStatsList = json.loads(outFileMarketStatsRead)
			TotalMarketcap = outFileMarketStatsList["TotalMarketcap"]
			TotalVolume = outFileMarketStatsList["TotalVolume"]
			BTCDominance = outFileMarketStatsList["BTCDominance"]
		coinLong = coinLong.replace('-',' ')
			
		context= {
		'coinLong': coinLong,
		'coinShort': coinShort,
		'coinCircSupply': coinCircSupply,
		'coinMaxSupply': coinMaxSupply,
		'coinWebsite': coinWebsite,
		'coinExplorer': coinExplorer,
		'coinBitcoinTalk': coinBitcoinTalk,
		'coinGithub': coinGithub,
		'coinTwitter': coinTwitter,
		'coinReddit': coinReddit,
		'coinDiscord': coinDiscord,
		'coinPriceUSD': coinPriceUSD,
		'coinPriceBTC': coinPriceBTC,
		'coinVolume': coinVolume,
		'coinMarketcap': coinMarketcap,
		'percent_change_24h_USD': percent_change_24h_USD,
		'percent_change_24h_BTC': percent_change_24h_BTC,
		'coinExchangeTable': coinExchangeTable,
		'coinImage': coinImage,
		'coinAmount': coinAmount,
		'TotalMarketcap': TotalMarketcap,
		'TotalVolume': TotalVolume, 
		'BTCDominance': BTCDominance
        }
	return render(request, 'coininfo/coinpage.html', context)
		
def homepage(request):
	with io.open('/home/ExchangeData/' + 'APIData.json', 'r', encoding='utf8') as outfileData:	
		url = '<a href="http://185.185.42.47:8000/'
		outfileDataRead = outfileData.read() 
		DataList = json.loads(outfileDataRead)
		CoinTop100 = []
		for coin in DataList:
			TempCoinList = []
			if str(DataList[coin]['rank']) == "":
				continue
			if str(DataList[coin]['marketcap']) == "":
				continue
			TempCoinList.append(str(DataList[coin]['rank']))
			imgPath = Path("/home/mysite/coininfo/static/coininfo/img/coinLogos/" + coin + ".png")
			if imgPath.is_file():
				image = '<div class="d-flex" ><img class="d-block" src="/static/coininfo/img/coinLogos/' + coin +'.png" width="25" height="25">'
			else:
				image = '<div class="d-flex" ><img class="d-block" src="/static/coininfo/img/coinLogos/UnknownCoin.png" width="25" height="25">'
			TempCoinList.append(image + '<span>' + ' '+ url + 'coin/' + DataList[coin]['name'] + '/">' + DataList[coin]['name'].replace('-', ' ') + '</a></span></div>')
			TempCoinList.append(coin)
			try:
				TempCoinList.append('$' + str("{:,}".format(int(round(float(DataList[coin]['marketcap']),0)))))
			except:
				TempCoinList.append('???')
			TempCoinList.append('$' + str(DataList[coin]['average_price_USD']))
			try:
				TempCoinList.append('$' + str("{:,}".format(int(round(float(DataList[coin]['total_volume']),0)))))
			except:
				TempCoinList.append('$' + '0')
			if DataList[coin]['percent_change_24h_USD'] != '':
				percent_change_24h = DataList[coin]['percent_change_24h_USD']
				if '-' not in str(percent_change_24h):
					percent_change_24h = DataList[coin]['percent_change_24h_USD']
				else:
					percent_change_24h = DataList[coin]['percent_change_24h_USD']
			else:
				percent_change_24h = ''
			TempCoinList.append(percent_change_24h)
			CoinTop100.append(TempCoinList)
		tbl = CoinTop100
		cols = ["<td>{0}</td>". format( '</td><td>'.join(t)  ) for t in tbl]
		CoinTop100Table = "<tr>{0}</tr>".format( "</tr>\n<tr>".join(cols))
		with io.open('/home/ExchangeData/' + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
			outfileShortRead = outfileShort.read() 
			ShortList = json.loads(outfileShortRead)
			coinAmount = len(ShortList)
			
		with io.open('/home/ExchangeData/' + 'APIMarketStats.json', 'r', encoding='utf8') as outFileMarketStats:	
			outFileMarketStatsRead = outFileMarketStats.read() 
			outFileMarketStatsList = json.loads(outFileMarketStatsRead)
			TotalMarketcap = outFileMarketStatsList["TotalMarketcap"]
			TotalVolume = outFileMarketStatsList["TotalVolume"]
			BTCDominance = outFileMarketStatsList["BTCDominance"]
			
		context = CoinTop100Table
		context= {
		'CoinTop100Table': CoinTop100Table,
		'coinAmount': coinAmount,
		'TotalMarketcap': TotalMarketcap,
		'TotalVolume': TotalVolume, 
		'BTCDominance': BTCDominance
		}
	return render(request, 'coininfo/home.html', context)
	
def exchangesOverview(request):
	# return HttpResponse("Hello world") 
	with io.open('/home/ExchangeData/' + 'ExchangeMarketStats.json', 'r', encoding='utf8') as outfileData:	
		url = '<a href="http://185.185.42.47:8000/'
		outfileDataRead = outfileData.read() 
		DataList = json.loads(outfileDataRead)
		ExchangeTop100 = []
		for Exchange in DataList:
			TempExchangeList = []
			# TempExchangeList.append(str(DataList[Exchange]['rank']))
			TempExchangeList.append('???')
			imgPath = Path("/home/mysite/coininfo/static/coininfo/img/exchangeLogos/" + Exchange + ".png")
			if imgPath.is_file():
				image = '<div class="d-flex" ><img class="d-block" src="/static/coininfo/img/exchangeLogos/' + Exchange +'.png" width="25" height="25">'
			else:
				image = '<div class="d-flex" ><img class="d-block" src="/static/coininfo/img/ExchangeLogos/UnknownExchange.png" width="25" height="25">'
			TempExchangeList.append(image + '<span>' + ' '+ url + 'exchange/' + Exchange + '/">' + Exchange + '</a></span></div>')
			try:
				TempExchangeList.append('$' + str("{:,}".format(int(round(float(DataList[Exchange]['tradeVolumeUSD']),0)))))
			except:
				TempExchangeList.append('???')
			ExchangeTop100.append(TempExchangeList)
		tbl = ExchangeTop100
		cols = ["<td>{0}</td>". format( "</td><td>".join(t)  ) for t in tbl]
		ExchangeTop100Table = "<tr>{0}</tr>".format( "</tr>\n<tr>".join(cols))
	with io.open('/home/ExchangeData/' + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
		outfileShortRead = outfileShort.read() 
		ShortList = json.loads(outfileShortRead)
		coinAmount = len(ShortList)
	with io.open('/home/ExchangeData/' + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
		outfileShortRead = outfileShort.read() 
		ShortList = json.loads(outfileShortRead)
		coinAmount = len(ShortList)
	with io.open('/home/ExchangeData/' + 'APIMarketStats.json', 'r', encoding='utf8') as outFileMarketStats:	
		outFileMarketStatsRead = outFileMarketStats.read() 
		outFileMarketStatsList = json.loads(outFileMarketStatsRead)
		TotalMarketcap = outFileMarketStatsList["TotalMarketcap"]
		TotalVolume = outFileMarketStatsList["TotalVolume"]
		BTCDominance = outFileMarketStatsList["BTCDominance"]
		
		context = ExchangeTop100Table
		context= {
		'CoinTop100Table': ExchangeTop100Table,
		'coinAmount': coinAmount,
		'TotalMarketcap': TotalMarketcap,
		'TotalVolume': TotalVolume, 
		'BTCDominance': BTCDominance
		}
	return render(request, 'coininfo/exchangehome.html', context)
	
def exchangePage(request, exchangeName):
	with io.open('/home/ExchangeData/' + 'ExchangeMarketStats.json', 'r', encoding='utf8') as outfileData:	
		url = '<a href="http://185.185.42.47:8000/'
		outfileDataRead = outfileData.read() 
		DataList = json.loads(outfileDataRead)
		exchangeVolumeUSD = str("{:,}".format(round(float(DataList[exchangeName]['tradeVolumeUSD']),2)))
		exchangeChange = '10'
		exchangeVolumeBTC = '1'
		CoinimgPath = Path("/home/mysite/coininfo/static/coininfo/img/exchangeLogos/" + exchangeName + ".png")
		if CoinimgPath.is_file():
			image = '<img class="d-block m-3" src="/static/coininfo/img/exchangeLogos/' + exchangeName +'.png" width="140" height="140"></div>'
		else:
			image = '<img class="d-block m-3" src="/static/coininfo/img/coinLogos/UnknownCoin.png" width="140" height="140"></div>'
		coinMarketsList = []
		CoinExchangeData = []
		try:
			for tradingPair in DataList[exchangeName]['tradingPairs']:
				coinMarketsList.append(tradingPair)
				coinMarketsList.append('$' + str("{:,}".format(round(float(DataList[exchangeName]['tradingPairs'][tradingPair]['price_USD']),2))))
				coinMarketsList.append('$' + str("{:,}".format(int(round(float(DataList[exchangeName]['tradingPairs'][tradingPair]['volume']),0)))))
				try:
					timenotUpdated = (datetime.datetime.strptime(DataList[exchangeName]['tradingPairs'][tradingPair]['lastUpdated'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()) / datetime.timedelta(minutes=1)
					if timenotUpdated >= 60:
						timenotUpdated = int(round((timenotUpdated / 60),0))
						if timenotUpdated <= 2:
							timenotUpdated = str(timenotUpdated).replace('-','') + ' hours ago'
						else:
							timenotUpdated = str(timenotUpdated).replace('-','') + ' hour ago'
					else:
						timenotUpdated = int(round(timenotUpdated,0))
						if timenotUpdated <= 2:
							timenotUpdated = str(timenotUpdated).replace('-','') + ' minutes ago'
						else:
							timenotUpdated = str(timenotUpdated).replace('-','') + ' minute ago'
					coinMarketsList.append(str(timenotUpdated))
				except Exception as e:
					coinMarketsList.append(str(e))
				CoinExchangeData.append(coinMarketsList)
				coinMarketsList = []
		except:
			pass
		# CoinimgPath = Path("/home/mysite/coininfo/static/coininfo/img/coinLogos/" + coin + ".png")
		# if CoinimgPath.is_file():
			# coinImage = '<img class="d-block m-3" src="/static/coininfo/img/coinLogos/' + coin +'.png" width="140" height="140"></div>'
		# else:
			# coinImage = '<img class="d-block m-3" src="/static/coininfo/img/coinLogos/UnknownCoin.png" width="140" height="140"></div>'
		tbl = CoinExchangeData
		cols = ["<td>{0}</td>". format( "</td><td>".join(t)  ) for t in tbl]
		ExchangeTable = "<tr>{0}</tr>".format( "</tr>\n<tr>".join(cols))
			
	with io.open('/home/ExchangeData/' + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
		outfileShortRead = outfileShort.read() 
		ShortList = json.loads(outfileShortRead)
		coinAmount = len(ShortList)
	with io.open('/home/ExchangeData/' + 'APIMarketStats.json', 'r', encoding='utf8') as outFileMarketStats:	
		outFileMarketStatsRead = outFileMarketStats.read() 
		outFileMarketStatsList = json.loads(outFileMarketStatsRead)
		TotalMarketcap = outFileMarketStatsList["TotalMarketcap"]
		TotalVolume = outFileMarketStatsList["TotalVolume"]
		BTCDominance = outFileMarketStatsList["BTCDominance"]
	context= {
		'exchangeLogo': image,
		'exchangeName': exchangeName,
		'exchangeVolumeUSD': exchangeVolumeUSD,
		'exchangeVolumeBTC': exchangeVolumeBTC,
		'exchangeChange': exchangeChange,
		'coinAmount': coinAmount,
		'TotalMarketcap': TotalMarketcap,
		'TotalVolume': TotalVolume, 
		'BTCDominance': BTCDominance,
		'ExchangeTable': ExchangeTable
		}
	return render(request, 'coininfo/exchangepage.html', context)