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

# Bringing up advance search
# browser.get('https://www.crunchbase.com/discover/organization.companies/')
# browser.get('https://www.crunchbase.com/searches')


# WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@title,'Small Saas in Sweden (SSS)')]")))

# # Find & print the saved searches
# elemList = browser.find_elements_by_partial_link_text('/discover/saved/')
# print(elemList)
# savedLink = 'https://www.crunchbase.com/discover/saved/small-saas-in-sweden-sss/d6e78ad2-4b8f-41ac-a8e4-9442092f5545'

# Insert saved search link here
browser.get('https://www.crunchbase.com/discover/saved/all-small-saas/22edce87-8ef7-44c6-8f9d-3371c130e7d3')

# WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@aria-describedby, 'ui-id-')]//span[@class='ui-button-text' and text()='Continue']"))).click()
# WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, 'Next')]")))
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
	time.sleep(5)


print("{} Links found".format(len(cleanedLinks)))

# Creating and adding the first row to CSV
# Change CSV file name here
csvfile = open(filenameCSV+'.csv', 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(['company_name', 'company_link', 'category'])
browser.implicitly_wait(1)
# category_text = ''
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
		try:
			assert 'Access to this page has been denied' in browser.title
			done = input("press & hold")
		except:
			pass



	# categories = browser.find_elements(By.XPATH, "//a[@class='cb-overflow-ellipsis'][@_ngcontent-client-app-c189='']")
	# categories = browser.find_elements(By.XPATH, "//div[@class='layout-row layout-align-start-center']//div[@class='cb-overflow-ellipsis']]")


	# for category in categories:
	# 	category_text += category.text + " "

	
	print("{} {}".format(name, link))
	c.writerow([name, link])

csvfile.close()
print('Write done to CSV')