from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

filenameCSV = input("Enter csv file name: ")

browser = webdriver.Firefox()

browser.get('https://www.crunchbase.com/login')
assert 'Log In' in browser.title

# Linkedin Log In Button
browser.find_element_by_css_selector("button.linkedin").click() 

# Switching to Linkedin's login window
for handle in browser.window_handles:
	browser.switch_to.window(handle)

# Waits for either 10s or when the username field is located
elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))

# Logging in Linkedin
elem.send_keys("username")
elem = browser.find_element_by_css_selector("input#password")
elem.send_keys("password")
browser.find_element(By.XPATH, '//button[text()="Sign in"]').click()

# Add in a assert func

time.sleep(3)
for handle in browser.window_handles:
	browser.switch_to.window(handle)

# Insert saved search link here
browser.get('https://www.crunchbase.com/discover/saved/all-small-saas/22edce87-8ef7-44c6-8f9d-3371c130e7d3')

time.sleep(3)
cleanedLinks = []

while True:
	elemList = browser.find_elements(By.XPATH, "//a[contains(@role, 'link')]")
	for elem in elemList:
		if "/organization/" in elem.get_attribute('href'):
			cleanedLinks.append(elem.get_attribute('href'))

	try:
		elem = browser.find_element(By.XPATH, "//a[contains(@aria-label, 'Next')]")
	except:
		break

	if elem.get_attribute('aria-disabled') == 'true':
		break

	browser.get(elem.get_attribute('href'))

	# Wait enough for elements to load
	time.sleep(5)


print("{} Links found".format(len(cleanedLinks)))

# Creating and adding the first row to CSV
csvfile = open(filenameCSV+'.csv', 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(['company_name', 'company_link', 'category'])

browser.implicitly_wait(1)
name = ''
for page in cleanedLinks:
	browser.get(page)

	try:
		name = browser.find_element_by_css_selector("span.profile-name").text
	except:
		pass

	try:
		name = browser.find_element_by_css_selector("h1.profile-name").text
	except:
		pass

	try:
		link = browser.find_element(By.XPATH, "//a[contains(@role, 'link')]").get_attribute('href')
	except:
		break
	
	print("{} {}".format(name, link))
	c.writerow([name, link])

csvfile.close()
print('Write done to CSV')