from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import random

PATH = "C:\SeleniumDrivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get("https://orteil.dashnet.org/cookieclicker/")

driver.implicitly_wait(2)
def check_lang():
    try:
        driver.find_element(By.ID, "langSelect-EN")
    except NoSuchElementException:
        return False
    return True

if(check_lang):
    english = driver.find_element(By.ID, "langSelect-EN")
    english.click()

driver.implicitly_wait(2)

cookie_id = "bigCookie"
cookie_count = driver.find_element(By.ID, "cookies")
items = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(1,-1,-1)]
#list of productPrice1,productPrice0 -range iteration is stepping backwards
#this way we get the more expensive upgrades first
print(items)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
cookie = WebDriverWait(driver, 10.0)\
                        .until(EC.presence_of_element_located((By.ID, cookie_id)))

#addressing StaleElementReferenceException
#element changes once clicked- it gets clicked again before page refereshes
#now the clicked element is stale since a new element is loaded

actions = ActionChains(driver)#an empty queue of actions
actions.click(cookie)#adding an action to the queue


for i in range(5000):
    actions = ActionChains(driver).click(cookie).perform()#whole action chain must be looped
    #I think it may all need to be in here because a new cookie instance appears on the page?
    count = int(cookie_count.text.split(" ")[0])
    print(count)
    for item in items:
        value = int(item.text)
        if value <= count:
            upgrade_actions = ActionChains(driver).move_to_element(item).click().perform()