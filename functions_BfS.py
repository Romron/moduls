






def main_bot_PF_1(URL,browser):

	try:
		browser.get(URL)
		browser.implicitly_wait(10)
		
	except Exception as e:
		raise
	else:

		list = browser.find_elements_by_tag_name('a')	# поличить список всех ссылок на главной странице сайта
		
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
				print(count_try_clicks_links, '. попытка кликнуть случайную ссылку' )
				print(e)




		# Собрать все ссілки на страницы фильмов
		list_elements = browser.find_elements_by_xpath('//html/body/div[1]/div/div/div/article/div/div/div/a/h2')
		time.sleep(random.uniform(1,30))		# случайное число с плавающей точкой

		count_try_clicks_films = 0
		rnd_film = random.choice(list_elements)
		while True:
			try:
				element_Wait = WebDriverWait(browser, 30).until(
					EC.element_to_be_clickable((By.XPATH, '//html/body/div[1]/div/div/div/article/div/div/div/a/h2'))
				)

				time.sleep(random.uniform(1,10))		# случайное число с плавающей точкой
				scroll_element(rnd_film,browser)
				time.sleep(random.uniform(1,10))		# случайное число с плавающей точкой

				rnd_film.click()	# выбор случайной ссылки из списка и переход по ней на страницу фильма
				break
			except Exception as e:
				# raise e
				count_try_clicks_films += 1
				print(count_try_clicks_films, '. попытка кликнуть случайный фильм' )
				print(e)

		# запускаю плеер
		time.sleep(random.uniform(1,30))		# случайное число с плавающей точкой

		try:
			element = browser.find_element_by_xpath('//*[@id="yohoho"]')
			element.click()
			time_look_filme = random.uniform(60,2400)
			print('Установленное время просмотра фильма: ', round(time_look_filme/60), ' минут')
			time.sleep(time_look_filme)		# случайное число с плавающей точкой
		except Exception as e:
			print(e) 
			print('Ошибка запуска плеера')


	finally:
		pass

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

