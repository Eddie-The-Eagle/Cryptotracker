from urllib.request import Request, urlopen
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


with io.open(prePath + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
	outfileShortRead = outfileShort.read() 
	ShortList = json.loads(outfileShortRead)
	for coin in ShortList:
		if ShortList[coin]['Website'] == '?':
			print(coin)
			coinLong = ShortList[coin]['Name'].replace('-', '')
			UrlList = ['http://www.'+coinLong+'.com', 'http://www.'+coinLong+'.org', 'http://www.'+coinLong+'.io', 'http://www.'+coinLong+'.network', 'http://www.'+coinLong+'.net, http://www.'+coinLong+'.tech', 'http://www.'+coinLong+'.foundation']
			for url in UrlList:
				try:
					req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
					web_byte = urlopen(req).read()
					webpage = web_byte.decode('utf-8')
					if 'blockchain' in webpage.lower():
						ShortList[coin]['Website'] = url.replace('http://www.','')
				except:
					pass
				
with io.open(prePath + 'APIShort.json', 'w', encoding='utf8') as outfileShort:
	str_ = json.dumps(ShortList,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
	outfileShort.write(to_unicode(str_))
