import requests 
import re 
import os 
import os.path
import sys
from selenium import webdriver	# импортирую модуль вебдрайвера
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import selenium.common.exceptions
import time
import json
import keyboard
import tkinter                 #  библиотека для графических интерфейсов 

# подключаю свои модули:
sys.path.append(os.path.dirname( __file__ ))
import general_functions 






result_listProxy = []
result = []
timeout = 5		# время ожидания, в секундах, нажатия клавиши для повторного перебора result_listProxy при попаданиии страницы каптчи

pathFile = os.path.dirname(__file__)	

listProxyPagesURLs	 = [
	'http://free-proxy.cz/en/',						# по этому URLу всё работает но только 5 страниц дальше без каптчи не пускает!
	'http://www.freeproxylists.net/ru/',			    # по этому URLу всё работает но сам сайт блокируеться по IP изначально!
	# 'https://hidemy.name/ru/proxy-list/',
	# 'http://foxtools.ru/Proxy',		# нет ссылки "Следующая"
	# 'https://htmlweb.ru/analiz/proxy_list.php?perpage=50#%D0%9A%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B8%20%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8', # нет ссылки "Следующая"
	# 'https://hidester.com/proxylist/',
	]

listProxyPages = [    				# для тестов
		# 'Proxy_pages/captcha_page from free-proxy.cz.html',  
		# 'Proxy_pages/freeproxylists.net.html',
		# 'Proxy_pages/free-proxy.cz.html',		
		# 'Proxy_pages/foxtools.ru.html',			
		# 'Proxy_pages/htmlweb.ru.html',			
	 	# 'Proxy_pages/foxtools.ru.txt',
	 	# 'Proxy_pages/hidester.com.txt',
		]

# result_listProxy = [				# для тестов
	# '195.154.39.255:5836', 
	# '206.127.88.18:80', 
	# ]

# test_IP_URL = 'https://2ip.ru/'		# слишком долго грузиться
# test_IP_URL = 'https://myip.ru/'






def get_ProxyList(path_dir_for_result_file):
	'''
		Собирает ip proxy с сайтов доноров
		записывает их в файл
		файл ложит в указанную папку
	'''
	# if os.path.exists(path_dir_for_result_file) == False:
	# 	print('Указан не корректный путь для сохранения файла результатов' )
	# 	return False


	driver = False
	link_NextPage = None

	# for fileName in listProxyPages:
	for URL in listProxyPagesURLs:
		
		flag_page_enumeration = 1
		count_ProxyIP = 0
		IP_proxy = ''

		print(URL)
		# print(fileName)
		
		while flag_page_enumeration:			# цикл продолжается пока есть ссылка на сл. страницу
			# для тестов:
			# with open(fileName,'r',encoding="utf-8") as file_handler:
			# 	html = file_handler.read()
			# 	flag_page_enumeration = 0

			if not link_NextPage:
				URL_Next_Page = URL

			arr_result = Get_HTML(URL_Next_Page,1,IP_proxy,1,driver)	# функция возвратит arr_result[html,driver]
			if type(arr_result) == bool:
				html = arr_result
			elif type(arr_result) == list:
				html = arr_result[0]
				try:			# на тот случай если Get_HTML() вернёт только arr_result[0]
					driver = arr_result[1]
				except IndexError:
					pass

			if check_CaptchaPage(html) == 'CAPTCHA' or html == False:
				try:			# если result_listProxy нет 
					if re.search('http://free-proxy.cz/en',URL_Next_Page):
						raise NameError			# генерирую исключение т.к. этот сайт не пускает дальше 5 страницы без каптчи
					if len(result_listProxy) == 0:   # если result_listProxy есть, но он равен нулю
						raise NameError			# генерирую исключение
					if count_ProxyIP < len(result_listProxy):			# Перебираю result_listProxy
						IP_proxy = result_listProxy[coиunt_ProxyIP]    
						count_ProxyIP += 1
						print(str(count_ProxyIP) + '. ' + IP_proxy)
					else:
						time1 = time.time()
						time2 = time.time()
						print("\n Перебор доступного списка прокси окончен. В списке было  " + count_ProxyIP + " прокси")
						print("Для повторного перебора нажмите Enter...")
						print("Для перехода к следующему сайту нажмите ПРОБЕЛ...\n")
						while time2 - time1 < timeout:
							if keyboard.is_pressed('Enter'):
								count_ProxyIP = 1
								break
							elif keyboard.is_pressed('space'):
								count_ProxyIP = False  # т.е. count_ProxyIP в данном случае используеться как флаг по которому программа выйдет из внешнего цыкла
								break
							time2 = time.time()
					if count_ProxyIP == False:	
						break
					continue # эта строка должна вернуть прогамму к обработке тогоже URLа но сдругим IP
			
				except NameError:
					print('Сайт заблокирован, списка прокси нет')
					html = False
					link_NextPage = ''	# для того чтобы на следующей итерации цыкла for обрабатывался именно новый URL а не значение link_NextPage из текущей итерации
					break 				# эта строка должна закончить оброботку текущего URLа и переходить к следующему 

			if html:
				listProxy = Get_ProxyIP(html)
				
				print(listProxy)		# для тестов

				for IP_Port in listProxy:
					result_listProxy.append(IP_Port)
				link_NextPage = Get_LinkNextPage(html)
				
				if link_NextPage:			
					URL_Next_Page = URL + link_NextPage

					print('\n' + URL_Next_Page)

				else:
					flag_page_enumeration = 0
					# driver.close()	# закрываю браузер

			else:

				continue
	
	if driver:	
		# driver.close()	# закрываю браузер если он всё ещё открыт
		driver.quit()	# закрываю браузер если он всё ещё открыт


	print('\n\n')
	print(result_listProxy)

	#============= Записываем полученные прокси в файл: ============
	if not os.path.exists(path_dir_for_result_file) :
		os.mkdir(path_dir_for_result_file)

	timePars = time.strftime("%d-%m-%Y %H.%M.%S", time.localtime())
	fileName = path_dir_for_result_file + '/proxylist '+ timePars +' .json'
	with open(fileName, 'w', encoding = 'utf-8') as f:
		json.dump(result_listProxy, f, indent = 2, ensure_ascii = False)	# json.dump() сама пишит в файл

def Get_HTML(URL,mode=1,IP_proxy='',flag_return_driver=0,driver=False):
	'''
		Функция должна: 
			получать страницу по переданому URL 
		Пременяет один из указанных способов, режимов, :
			Возможные способы, режимы, получения:
				1 - Библиотека requests:	
					контроль заголовков
					передача строки юзерагента
					КУКИ
				2 - Селениум
					Очень медлено!

				3 - Библиотека Splinter
					????????????
				
				4 - Библиотека MechanicalSoup
					????????????				

				5 - Библиотека RoboBrowser
					????????????

				6 - Библиотека Mechanize
						- не выполняет Javascript на страницах, которые он просматривает (проверить)

				7 - Библиотека Scrapy
					??????????????

		Возврт значений:
			если mode=1:
				пользователь имеет возможность получить экземпляр браузера для дальнейшего использования
				 вне этой ф-ции, но тогда он отвечает за закрытие этого экземпляра браузера. 
				Есть возможность вернут в ф-цию экземпляра браузера
	'''

  	# Проверка на корректность полученных данных
	if type(URL) != str:
		print('You must input only str')
		return False

	if mode == 1:
		# print('You choso Selenium:')

		if flag_return_driver == 0 or driver == False:

			r = tkinter.Tk()		# получаем объект для доступа к параметрам экрана

			# выбираю версию geckodriver в зависимости от разрядности Windows
			name_file_geckodriver = general_functions.choose_geckodriver_file()

			pathDriver = os.path.dirname(os.path.abspath(__file__)) + "\\" + name_file_geckodriver
			opts = Options()
			opts.set_preference("dom.webdriver.enabled", False)	# скрывает то что браузер управляеться автоматически
			opts.headless = False
			opts.add_argument('-width=' + str(r.winfo_screenwidth()/2))		# Устанавливаем ширину окна 
			opts.add_argument('-height=' + str(r.winfo_screenheight()/1.3))	# Устанавливаем высоту окна
			

			driver = webdriver.Firefox(executable_path=pathDriver,options=opts)	
			driver.set_window_position(r.winfo_screenwidth()/2, 0)	

			if IP_proxy:
				webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
				    "httpProxy": IP_proxy,
				    "ftpProxy": IP_proxy,
				    "sslProxy": IP_proxy,
				    "proxyType": "MANUAL",
					}
		try:
			driver.get(URL)

			try:
				WebDriverWait(driver, 5).until(lambda driver: 
					driver.find_elements_by_xpath("//*[.='IP адрес']"))  
			except Exception as errMess:
				pass
				# print('Элемент не найден')
				# print(errMess)

			html = driver.page_source


		# Оброботка исключний:
		except Exception as errMess:
			print('Текущий URL недоступен')
			html = False		
		
		# Вывод результатов в зависимости от значения flag_return_driver
		if flag_return_driver and html:
			arr_result = [html,driver]
			return arr_result

		# driver.close()	# закрываю браузер
		driver.quit()	# закрываю браузер
		return html



	elif mode == 2:
		print('You choso Requests lib')
		headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
		# response = requests.get(url,headers=headers,proxies=proxies,timeout=_timeout,verify=False)
		response = requests.get(URL,headers=headers)
		response.encoding = 'utf-8'
		html = response.text

	elif mode == 3:
		
		print('You choso Splinter')
	
	elif mode == 4:
		
		print('You choso MechanicalSoup')

	elif mode == 5:
		
		print('You choso RoboBrowser')

	elif mode == 6:
		
		print('You choso Mechanize')

	elif mode == 7:
		
		print('You choso Scrapy')

def Get_ProxyIP(html):
	''' Собрать IP прокси на странице
		Вернуть список собраных IP в формате IP:port
	'''

	result_listProxy = []

	# patternProxy = r'(?:[0-9]{1,5}\.){3}[0-9]{1,3}:[0-9]{2,5}'
	pattern = r'>((?:[0-9]{1,5}\.){3}[0-9]{1,3}(?::[0-9]{2,5})?)(?:(?:</[aspan]>)?</td>\n?.*?<td.*?>([0-9]{2,5})<)?'


	result = re.findall(pattern,html)

	q = 0
	while q < len(result):
		if re.search(':', result[q][0]) == None:
			result_listProxy.append(result[q][0] + ':' + result[q][1])
		else:
			result_listProxy.append(result[q][0]) 
		q += 1	


	return result_listProxy

def Get_LinkNextPage(html):
	''' Найти ссылку на следующую страницу 
		Вернуть найденную ссылку в формате URLа пригодного для использоваия в Get_HTML()
	'''
	
	# (? pattern = r'href=("(.)*?)">Следующая »</a>')
	# pattern = r'href="((?:/\w)*\.?/?[/\?][\w]+[/=]\d{1,2})">Следующая »</a>'	#работает
	# pattern = r'href="((?:/\w)*\.?/?[/\?][\w]+[/=]\d{1,2})">(?:Следующая)|(?:Next) »</a>' #работает только на первом	 
	# pattern = r'<a href="([\w\d/\?=\.]+)">(?:Следующая)|(?:Next) »</a>'	 
	pattern = r'"([\w\d/\?=\.]+)">(?=(?:Следующая)|(?:Next) »</a>)'	 

	href_ = re.findall(pattern,html)
	if len(href_) > 1:
		link_NextPage = re.sub(r'^[\./en]*','',href_[1])
	else:
		print('Следующей страницы НЕТ \n')
		link_NextPage = None
	return link_NextPage

def check_CaptchaPage(html):
	'''
		TODO: добавить патерны для разных страниц блокировки

	'''

	try: 
		if re.search('complete CAPTCHA to continue',html): 
			return 'CAPTCHA'
		# elif re.search('',html):
		# 	return 'CAPTCHA'

	except:
		print('check_CaptchaPage(): Блокировки сайта не найдено')

	return True


# ##################################################################################################################
# ##################################################################################################################

if __name__ == '__main__':

	'''
		если модуль запускаеться отдельно, не импорт, 
		результирующий файл будет в папке Proxylist 
		которая будет создана в той же папке что и файл скрипта
	'''

	path_dir_for_result_file = os.path.dirname(os.path.abspath(__file__)) +  "/Proxylist"	
	get_ProxyList(path_dir_for_result_file)