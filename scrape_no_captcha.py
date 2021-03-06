# coding: utf-8
# scrape Arlington, VA court cases using Selenium and Firefox on Mac OSX
from scrape_captcha import *
from time import sleep

driver = driver()

driver.get("https://eapps.courts.state.va.us/ocis/landing/false")
sleep(1)

element = driver.find_element_by_id("acceptTerms")
element.click()
sleep(0.5)

driver.find_element_by_id("searchBy").click()
sleep(2)

element = driver.find_element_by_css_selector("input[type='radio'][value='Hearing Date']").click()
sleep(1)

driver.find_element_by_id("searchBy").click()
sleep(0.6)

driver.find_element_by_id("courtLevelSelectBtn").click()
sleep(0.4)

driver.find_element_by_id("courtLevelLabel0").click()
sleep(1)

driver.find_element_by_id("courtLevelSelectBtn").click()
sleep(1)

driver.find_element_by_id("allCourtTitle").click()
sleep(0.5)

element = driver.find_element_by_id("courtSearch")
element.send_keys("Arlington")
sleep(0.4)

driver.find_element_by_id("selectCourtSpan0").click()
sleep(0.6)

driver.find_element_by_id("applyCourtBtn").click()
sleep(1)

date_search(driver)
driver.implicitly_wait(5)

element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results"))) 

def results_next_page(driver=driver):
    try:
        driver.implicitly_wait(5)
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loadMore")))
        except TimeoutException:
            print("End of results")
            return False
        sleep(5)
        element.click()
        return True
    except NoSuchElementException:
        print("End of results")
        return False

print(element.text[43:][:-25])
