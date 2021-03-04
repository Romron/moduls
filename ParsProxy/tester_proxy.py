 #  Чекер proxy с помощью библиотеки Requests

 #  для запросов через SOCKS протоколы необходимо установить зависимости: $ pip install requests[socks]
import requests
from requests.exceptions import *
from urllib3.exceptions import *
from bs4 import BeautifulSoup
import re 

from proxylist import *


print("test 3.py     Чекер proxy с помощью библиотеки Requests \n")

countProxy = 0
countAnonymousProxy = 0
countTransparentProxy = 0

# url = "https://httpbin.org"

# url = "https://www.kinopoisk.ru/"
# url = "http://yandex.ru/"
url = "https://2ip.ua/ru"

listHeaders = [
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'},	# Microsoft Edge (Win 10 x64):
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; ASU2JS; rv:11.0) like Gecko'},	# Internet Explorer 11 (Win 8.1 x64):
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; rv:11.0) like Gecko'},		# Internet Explorer 11 (Win 10 x64):
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'},	# Apple Safari 5.1 (Win 8 x64):
	# {'User-Agent' : 'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.17'},		# Opera 12.17 (Win 8 x64): 
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36 OPR/40.0.2308.62'},	#Opera 40 (Win 10 x64)
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT  6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'},		# Google Chrome 40 (Win 8.1 x64):
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'},
	# {'User-Agent' : 'Mozilla/5.0 (Windows NT  6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'},
	{'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
]


# for headers in listHeaders:
# 	PROXY = "145.255.28.2:58193"

for PROXY in proxyList_1:
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

	countProxy += 1

	# proxyIP = 'https://' + PROXY
	proxyIP = PROXY
	http_proxy = "http://" + proxyIP
	https_proxy = "https://" + proxyIP 

	try:
		# proxies = {"http": proxyIP}
		proxies = {"http": http_proxy,
				   "https":https_proxy}
		# response = requests.get(url,headers=headers,proxies=proxies,verify=False)
		response = requests.get(url,headers=headers,proxies=proxies)
		response.encoding = 'utf-8'

	# Парсим полученную страницу:
		soup = BeautifulSoup(response.text, 'lxml')
		div_ip = soup.find('div', class_='ip' )
		realIP = div_ip.text.rstrip().lstrip()		# Удаление пробелов в начале и конце строки
		div_User_Agent = soup.find('div', text='Браузер:')
		div_Location = soup.find('div', text='Местоположение:')

	# Вывод результата:

		print(str(countProxy) + ". " + str(response))
		print('      proxyIP:  ' + proxyIP)		
		print('      realIP:   ' + realIP)		
		print('      Браузер: ' + div_User_Agent.nextSibling.text)		
		print('      Местоположение: ' + div_Location.nextSibling.nextSibling.text)
		
		# if (realIP == PROXY):
		# 	print(str(countProxy) + ". " + str(response) + '    proxy is anonymous')
		# 	print('      proxyIP:  ' + proxyIP)		
		# 	print('      realIP:   ' + realIP)		
		# 	print('      Браузер: ' + div_User_Agent.nextSibling.text)		
		# 	print('      Местоположение: ' + div_Location.nextSibling.nextSibling.text)
		# else:
		# 	print(str(countProxy) + ". " + str(response) + '   код ответа сервера:   ' + response.status_code +  'ProxyIP = ' + PROXY + '     proxy is transparent')
		# 	countTransparentProxy += 1
		# 	continue

# Оброботка исключний:
	except TimeoutError:
		print(str(countProxy) + ". TimeoutError")
		continue	

	except ConnectionError:
		print(str(countProxy) + ". ConnectionError")
		# print(str(countProxy) + ". ConnectionError" + "    Код ответа сервера: " + response.status_code)
		continue

	except NewConnectionError:
		print(str(countProxy) + ". NewConnectionError")
		continue

	except MaxRetryError:
		print(str(countProxy) + ". MaxRetryError")
		continue	

	# except HTTPSConnectionPool:
	# 	print(str(countProxy) + ". HTTPSConnectionPool")
	# 	continue	

	except Exception as err:
		print(str(countProxy) + ". Неизвестная ошибка соединения" )
		continue

	countAnonymousProxy += 1

print('Всего проверено: '+ str(countProxy))
print('  Найденно:')
print('    прозрачных: '+ str(countTransparentProxy))
print('    анонимных:  '+ str(countAnonymousProxy) + '  или  ' + str(round(countAnonymousProxy/countProxy*100, 1)) + ' %' )








