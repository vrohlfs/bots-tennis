## Import packages
import os
from os import times
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service

import time
from datetime import date, timedelta


########### INPUT PARAMETERS ###################
## Grab secrets
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
guest_name = os.environ['GUEST_NAME']
playing_time = os.environ['PLAYING_TIME']
t = os.environ['CONFIRM_TIME']


## Driver settings
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

actions = ActionChains(driver)
driver.get("https://wtc.clubautomation.com/")
wait = WebDriverWait(driver, timeout = 30)

## Details
game_date = date.today() + timedelta(days=2)
game_date = game_date.strftime("%m/%d/%Y") 

# Website Login
login_form = driver.find_element(By.ID, "caSignInLoginForm")
un = driver.find_element(By.NAME, "login")
un.send_keys(username)

actions.send_keys(Keys.TAB).perform()
pw = wait.until(EC.visibility_of_element_located((By.NAME,"password")))
pw.send_keys(password)

login_form.submit()

########### MAKE A NEW RESERVATION ###################
driver.get("https://wtc.clubautomation.com/event/reserve-court-new")

# Who will host? -> Add guest
# wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="addParticipant"]'))).click()
# wait.until(EC.element_to_be_clickable((By.ID,"addParticipant"))).click() 
# guest = wait.until(EC.visibility_of_element_located((By.ID,"guest_1")))
# guest.send_keys(guest_name)
# wait.until(EC.element_to_be_clickable((By.ID,"ui-id-3"))).click()
guest_field = driver.find_element(By.XPATH, '//*[@id="guest_1-wrapper"]/span[1]/span')
guest_field.send_keys(guest_name)
# driver.execute_script('arguments[0].innerHTML = guest_name;', element)


# When ? 
reservation_date = wait.until(EC.visibility_of_element_located((By.ID,"date")))
reservation_date.clear()
reservation_date.send_keys(game_date)
driver.find_element_by_class_name("last-child").click()
# wait.until(EC.element_to_be_clickable((By.ID,"interval-90"))).click()

# Search for available times
# From: option[7] = 7:00AM
selection_From_time = driver.find_element_by_xpath('//*[@id="timeFrom"]/option[7]')
driver.execute_script("arguments[0].setAttribute('selected', 'selected')", selection_From_time)
# To: option[23] = 11:00PM
selection_To_time = driver.find_element_by_xpath('//*[@id="timeTo"]/option[23]')
driver.execute_script("arguments[0].setAttribute('selected', 'selected')", selection_To_time)

## Click Search
search = wait.until(EC.visibility_of_element_located((By.ID,"reserve-court-search")))
actions.click(search).perform()
 
# Choose Time'
# wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="times-to-reserve"]/tbody/tr/td[1]/a[1]'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="times-to-reserve"]/tbody/tr/td[1]/a[text()[contains(.,"' + t +'" )]]'))).click()

# Confirm
wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="confirm"]'))).click()

# close entire browser
#driver.quit()

print("Win the match now. From: your tennis bot!")
