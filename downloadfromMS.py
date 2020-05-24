from selenium import webdriver
import time

SELENIUM_WEBDRIVERS = {
	‘default’: {
		‘callable’: webdriver.Chrome,
		‘args’: (),
		‘kwargs’: {},
	},
	‘firefox’: {
		‘callable’: webdriver.Firefox,
		‘args’: (),
		‘kwargs’: {},
	},
}

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
#options.binary_location = "D:\Projetos\ModeloAndre"
driver = webdriver.Chrome(options=options)
driver.get('https://covid.saude.gov.br/')

# click radio button
python_button = driver.find_elements_by_tag_name("ION-BUTTON")
python_button[3].ATTR = 'TXT:Arquivo<SP>CSV'
#python_button = driver.find_element_by_class_name('button-white')
fi = python_button[3].click()
time.sleep(60)
print(' ')

#TYPE=ION-BUTTON ATTR=TXT:Arquivo<SP>CSV