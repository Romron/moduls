import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import json
import sys
import time
import random

# подключаю свои модули:
sys.path.append(os.path.dirname( __file__ ))
sys.path.append(os.path.join( os.path.dirname( __file__ ), '../../../moduls' ))
import general_functions
import ParsProxy.pars_proxy as ParsProxy



# def run_ThroughProxy(function,proxyList):
def run_ThroughProxy(proxyList,function,URL,flag_check_Captcha=False,flag_headless=False,flag_sond=False):

	'''
		
	'''

	count_proxyIP = 0
	count_FailStart = 1
	count_SuccesStart = 1

	# выбираю версию geckodriver в зависимости от разрядности Windows
	name_file_geckodriver = general_functions.choose_geckodriver_file()
	pathDriver = os.path.dirname(os.path.abspath(__file__)) + "\\" + name_file_geckodriver
	

	options = Options()
	options.set_preference("dom.webdriver.enabled", False)	# скрыть что браузер под управлением webdriver

	if flag_headless == True:		# запуск в безголовом режиме
		options.headless = True
	firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
	firefox_capabilities["marionette"] = True

	if flag_sond == True:		# запуск в беззвучном режиме
		profile = webdriver.FirefoxProfile()
		profile.set_preference("media.volume_scale", "0.0")

	while count_proxyIP < len(proxyList):
		proxyIP = proxyList[count_proxyIP]
		count_proxyIP += 1
		print(count_proxyIP,'. ',proxyIP,'  ',end='  ')

		try:
			if proxyIP:
				firefox_capabilities['proxy'] = {
				    "proxyType": "MANUAL",
				    "httpProxy":  proxyIP,
				    "ftpProxy":  proxyIP,
				    "sslProxy":  proxyIP,
					}

			browser = webdriver.Firefox(
				executable_path=pathDriver,
				options=options,
				firefox_profile=profile,
				proxy=proxyIP)
			browser.set_page_load_timeout(900)	# ожидание загрузки страницы 15 минут
		except Exception as e:
			raise e
		else:

			# проверка полученой страницы на Captcha
			if flag_check_Captcha == True :
				try:
					browser.get(URL)
					browser.implicitly_wait(15)
					# element = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
				except Exception as e:
					# raise e
					print('Proxy ERR: ')
					browser.close()
					browser.quit()	
					continue				
				else:
					html = browser.page_source
					if ParsProxy.check_CaptchaPage(html) == 'CAPTCHA' :
						time.sleep(random.uniform(1,10))
						browser.close()
						browser.quit()
						continue

			result = function(browser)

			browser.close()
			browser.quit()

			if result == True :
				print('    Успешный запуск № ', (count_SuccesStart))
				count_SuccesStart += 1
			else:
				print('    Не удачный запуск № ', count_FailStart)
				count_FailStart += 1


			time.sleep(random.uniform(1,5))		# случайное число с плавающей точкой	







if __name__ == '__main__':
	print('Этот модуль предназначен только для импорта т.к. неимеет интерфейса для работы с пользователем')