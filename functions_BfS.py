
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import random
import time






def bot_PF_1(browser):

	'''
		Все необходимые подготовительные операции:
			обращение через прокси
			установлени соединения
			проверка на CAPTCHA
			и др.
		выполняються в предидущих функциях
		сюда передаёться browser 
		на страницах которого можно выполнять нужные действи
	'''

	# try:
	# 	browser.get(URL)
	# 	browser.implicitly_wait(10)
		
	# except Exception as e:
	# 	raise
	# else:

	list = browser.find_elements_by_tag_name('a')	# поличить список всех ссылок на главной странице сайта
	if len(list) == 0 :
		print('\n    ','ссылки на главной странице сайта не найдены')
		return False

	count_try_clicks_links = 0
	while True:
		rnd_link = random.choice(list)
		try:
			time.sleep(random.uniform(1,10))		# случайное число с плавающей точкой
			
			scroll_element(rnd_link,browser)

			time.sleep(random.uniform(1,10))		# случайное число с плавающей точкой
			rnd_link.click()	# выбор случайной ссbылки из списка и переход по ней
			break
		except Exception as e:
			# raise e
			count_try_clicks_links += 1
			print('\n    ',count_try_clicks_links, '. попытка кликнуть случайную ссылку',end='')
			# print(e)
			# ограничитель попыток
			if count_try_clicks_links > 5 :
				break


	# Собрать все ссылки на страницы фильмов
	list_elements = browser.find_elements_by_xpath('//html/body/div[1]/div/div/div/article/div/div/div/a/h2')
	if len(list_elements) == 0 :
		print('\n    ','ссылки на страницы фильмов не найдены')
		return False
	time.sleep(random.uniform(1,30))		# случайное число с плавающей точкой

	count_try_clicks_films = 0
	while True:
		rnd_film = random.choice(list_elements)
		try:
			element_Wait = WebDriverWait(browser, 30).until(
				EC.element_to_be_clickable((By.XPATH, '//html/body/div[1]/div/div/div/article/div/div/div/a/h2'))
			)

			# убрал так как перемотка делает выбранный элемент не видимым
			# после чего клик на него приводит к ошибке
			# доработать ф-цию scroll_element()
			# time.sleep(random.uniform(1,10))		# случайное число с плавающей точкой
			# scroll_element(rnd_film,browser)
			time.sleep(random.uniform(1,10))		# случайное число с плавающей точкой

			rnd_film.click()	# выбор случайной ссылки из списка и переход по ней на страницу фильма
			break
		except Exception as e:
			# raise e
			count_try_clicks_films += 1
			print('\n    ',count_try_clicks_films, '. попытка кликнуть случайный фильм',end='')
			print(rnd_film)
			# print(e)
			# ограничитель попыток
			# если за указаное кол-во попыток перейти на страницу фильма не удалось
			# печатаю соответствующую ошибку,
			# прекращаю выполнение функции и закрываю браузер 
			if count_try_clicks_films > 5 :
				print('\n    ','Ошибка прехода на страницу фильма')
				return False


	# запускаю плеер
	time.sleep(random.uniform(1,30))		# случайное число с плавающей точкой

	try:
		element = browser.find_element_by_xpath('//*[@id="yohoho"]')
		element.click()
		time_look_filme = random.uniform(60,2400)
		print('\n    ','Установленное время просмотра фильма: ', round(time_look_filme/60), ' минут')
		time.sleep(time_look_filme)		# случайное число с плавающей точкой

		print('    Success!!')
		return True

	except Exception as e:
		# print(e) 
		print('\n    ','Ошибка запуска плеера')
		return False


def scroll_element(target_element, browser, scroll_element='body'):
	'''
		плавная прокрутка окна до указанных заданного элемента
	'''
	rect_elenent = target_element.rect

	x = 0
	y = 0
	x_end = rect_elenent["x"]
	y_end = rect_elenent["y"]

	js_scroll = 'window.scrollTo(' + repr(x_end) + ',' + repr(y_end) + ', document.' + scroll_element + '.scrollHeight);'
	browser.execute_script(js_scroll)

	# добавить плавность прокрутки
	# этот вариант плавной прокрутки не работает
	# while (x < x_end):
	# 	js_scroll = 'window.scrollTo(' + repr(x) + ',' + repr(y) + ', document.' + scroll_element + '.scrollHeight);'
	# 	browser.execute_script(js_scroll)
	# 	time.sleep(random.uniform(5,10))		# случайное число с плавающей точкой
	# 	x += 1

	# 	print("js_scroll:  ", js_scroll)
	# 	print('x = ', x)




if __name__ == '__main__':
	print('Этот модуль предназначен только для импорта т.к. неимеет интерфейса для работы с пользователем')