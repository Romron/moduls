import sys



'''
	Сборник общих функций для файлов модуля ParsProxy

'''


def choose_geckodriver_file():
	'''
		Проверяет Битность системы 
	'''
	if sys.maxsize < 2**31 :
		name_file_geckodriver = 'geckodriver-win32.exe'
	else:
		name_file_geckodriver = 'geckodriver-win64.exe'

	return name_file_geckodriver

def create_LogFile():
	'''
		Получить имя файла 
		Проверить наличие файла с таким именем
		Если такого файла нет, создать
		Если есть 
	'''






