from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(options=options)
driver.get('https://covid.saude.gov.br/')

python_button = driver.find_elements_by_tag_name("ION-BUTTON")
python_button[3].ATTR = 'TXT:Arquivo<SP>CSV'
fi = python_button[3].click()
time.sleep(60)
