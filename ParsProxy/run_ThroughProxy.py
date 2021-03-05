import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import sys

# def run_ThroughProxy(function,proxyList):
def run_ThroughProxy(proxyList,function,URL):

	count_proxyIP = 0



	pathDriver = os.path.dirname(os.path.abspath(__file__)) + "\\geckodriver.exe"
	options = Options()
	options.set_preference("dom.webdriver.enabled", False)
	firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
	firefox_capabilities["marionette"] = True


	while count_proxyIP < len(proxyList):
		proxyIP = proxyList[count_proxyIP]

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
				proxy=proxyIP)

		except Exception as e:
			count_proxyIP += 1
			raise e
		else:

			function(URL,browser)

			browser.close()
			browser.quit()

			print('Запуск № ' + count_start_of_bot)
			count_start_of_bot += 1
			time.sleep(random.uniform(1,5))		# случайное число с плавающей точкой	







if __name__ == '__main__':
	print('Этот модуль предназначен только для импорта т.к. неимеет интерфейса для работы с пользователем')