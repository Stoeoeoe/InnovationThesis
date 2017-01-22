import re

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

link = 'http://www.alstom.com/sitemap/'

driver = webdriver.PhantomJS(executable_path='../bin/phantomjs-2.1.1-windows/bin/phantomjs.exe', service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver.set_window_size(1920, 1080)
wait = WebDriverWait(driver, 5)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body")))

driver.get(link)
result = driver.page_source
result2 = requests.get(link).text

print(result)
print('--------------------------------------------------------------------------------')
print(result2)

driver.close()