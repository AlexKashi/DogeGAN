# import requests
# from bs4 import BeautifulSoup
# import selenium 
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# path = "/usr/bin/chromedriver"

# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)


# driver = webdriver.Chrome(path)

# driver.get("https://opensea.io/collection/cryptopunks")

# WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//a[@role = 'gridcell']")))
# #wait = WebDriverWait(driver, 10, poll_frequency=1)

# cells = driver.find_elements_by_xpath("//a[@role = 'gridcell']")

# print(cells)

# # for image in image_elements:
# # 	src = image.get_attribute('src')
# # 	print(src)
# # # print(image_elements)






from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import http.cookiejar
import time
import csv
import sys
import traceback
from selenium.common.exceptions import NoSuchElementException


def set_chrome_option():
	"""
	set chrome options
	:return: chrome_options
	"""
	chrome_options = webdriver.ChromeOptions()

	# set headless model
	# chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("user-data-dir=selenium") 


	return chrome_options


jar = http.cookiejar.CookieJar()
path = "/usr/bin/chromedriver"



BASE_URL = "https://opensea.io/collection/cryptopunks"
BASE_URL = "https://opensea.io/collection/boredapeyachtclub"
BASE_URL = "https://opensea.io/collection/azuki"

output = "boredapeyachtclub.csv"
output = "azuki.csv"
driver = webdriver.Chrome(path)


def getUnit(cell):
	try:
		return cell.find_elements(by=By.XPATH, value="//div[@cursor = 'pointer']//img")[0].get_attribute("alt")
	except:
		return "None"

def getAmmount(cell):
	try:
		return cell.find_element(by=By.CLASS_NAME,value="Price--amount" ).text
	except:
		return "-1"

data = []

urls = set()
# driver.get("https://login.stanford.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s2")

driver.get(BASE_URL)

time.sleep(3)

fieldnames = ["name", "url", "unit",  "amount"]

with open(output, 'w+', newline='', encoding="utf-8") as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	while True:
		try: 
			cells = driver.find_elements(by=By.XPATH, value="//div[@role = 'gridcell']")
			prevCount = len(urls)
			for cell in cells:
				img = cell.find_element(by=By.CLASS_NAME,value="Image--image" )
				amount = getAmmount(cell)
				unit = getUnit(cell)
				url = img.get_attribute("src")
				name = img.get_attribute("alt")
				if url is not None:
					if url not in urls:
						writer.writerow({"name" : name, "url" : url, "unit" : unit ,"amount" : amount})
					urls.add(url)
			print(f"total {len(urls)} pageSize {len(urls) - prevCount}")
			# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			driver.execute_script("window.scrollBy(0,750);")
			time.sleep(2)
		except:
			print("Cant Find element, SLOW DOWN!")
			driver.execute_script("window.scrollBy(0,100);")
			time.sleep(3)
