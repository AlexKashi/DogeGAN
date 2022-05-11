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




BASE_URL = "https://stanford.rimeto.io/search/"
# browser = webdriver.PhantomJS('/usr/local/bin/phantomjs')
# driver = webdriver.Chrome("chromedriver")


driver = webdriver.Chrome("chromedriver.exe")#, chrome_options=set_chrome_option()



data = []


# driver.get("https://login.stanford.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s2")

driver.get(BASE_URL)

time.sleep(45)

# print(driver.page_source)
# content = driver.find_element_by_class_name("ln3oxu-0 eWdwoJ")
# print(content)


page = 0

fieldnames = ["Name", "Title", "Email W", "Slack S", "Phone W","Mobile M", "Custom SI", "Email MC", "Fax W"]

with open('undergrads-new.csv', 'w+', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    while True:
        curIndex = 0
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


        try:
            while True:
                span = driver.find_element_by_xpath("//div[@id='search-result-webdriver-selector-{0}']".format(curIndex))#/span[@class='ln3oxu-0 eWdwoJ']".format(0))

                dataTypes = []
                elements = span.find_elements(By.TAG_NAME, 'img')
                for element in elements:
                    dataTypes.append(element.get_attribute("alt").split(" ")[0])

                # print(dataTypes)

                items = span.text.split("\n")
                # print(items)

                line = {"Name" : items[0]}

                prefixes = ["W:", "S:", "SI:", "MC:", "M:"]


                startIndex = -1
                if len(items) > 1:

                    if items[1] in prefixes:
                        line["Title"] = ""
                        startIndex = 1
                    else:
                        line["Title"] = items[1]
                        startIndex = 2


                    for i in range(len(dataTypes)):
                    	
                    	line[dataTypes[i] + " "+ items[startIndex + i * 2][:-1]] = items[startIndex + i * 2 + 1]


                print(line)
                curIndex+=1
                print(curIndex)
                writer.writerow(line)
        except:
            print("Finished parsing page {0}".format(page))
            page +=1
            nextButton = driver.find_element_by_xpath("//div[@class='mixnv3-1 kDAhyi']")

            nextButton.click()

            pass

