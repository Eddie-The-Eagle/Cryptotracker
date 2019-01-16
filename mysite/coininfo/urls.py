from django.urls import re_path, include, path
from . import views
import io
import json
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.homepage, name='homepage'),
	path('coin/<str:coinLong>/', views.coinPage, name='coinPage'),
	path('Coin/<str:coinLong>/', views.coinPage, name='coinPage'),
	path('exchanges/', views.exchangesOverview, name='exchangesOverview'),
	path('exchange/<str:exchangeName>/', views.exchangePage, name='exchangePage'),
	path('Exchange/<str:exchangeName>/', views.exchangePage, name='exchangePage'),
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('coininfo/img/coinLogos/favicon.png'), ),name="favicon")
]

# with io.open('/home/ExchangeData/' + 'APIShort.json', 'r', encoding='utf8') as outfileShort:	
	# outfileShortRead = outfileShort.read() 
	# ShortList = json.loads(outfileShortRead)
	# for i in ShortList:
		# coin = ShortList[i]['Name'].lower()
		# coinShort = ShortList[i]['Short']
		# if coin != '???':
			# urlpatterns.append(re_path(r"(?i)" + coin + "/", views.index, name='index' {'coin': coinShort}))
# urlpatterns.append(re_path(r"(<str:coin>)", views.index, name='index')
# urlpatterns.append(re_path(r"(?i)", views.homepage, name='homepage')) 
# urlpatterns.append(re_path(r"(?i)", views.exchangepage, name='exchangepage')) 