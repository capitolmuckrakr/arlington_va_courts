# coding: utf-8
# scrape Arlington, VA court cases using Selenium and Firefox on Mac OSX
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import sleep
import os, logging

def driver(headless=False):
    fp = webdriver.FirefoxProfile()
    if headless:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options,firefox_profile=fp)
    else:
        driver = webdriver.Firefox(firefox_profile=fp)
    return driver

def captcha_start_page(driver=driver):
    start_url = 'https://eapps.courts.state.va.us/gdcourts/captchaVerification.do?landing=landing'
    driver.get(start_url)
    element = driver.find_element_by_name("accept")
    element.click()

def captcha_start_arlington_court(driver=driver):
    element = driver.find_element_by_id("txtcourts1")
    courtname = "Arlington General District Court"
    element.send_keys(courtname)
    element.click()
    driver.implicitly_wait(2)
    element.click()

def date_search(driver=driver,date = "08/03/2020"):
    try:
        element = driver.find_element_by_link_text("Hearing Date Search")
        element.click()
        driver.implicitly_wait(10)
        element = driver.find_element_by_id("txthearingdate")
    except NoSuchElementException:
        element = driver.find_element_by_id("datepickerele")
    element.send_keys(date)
    element.send_keys(Keys.ENTER)

def captcha_start_scrape_results_page(driver=driver):
    results = driver.find_element_by_tag_name("table").text[1036:][:-178]
    return results

def captcha_start_results_next_page(driver=driver):
    try:
        element = driver.find_element_by_name("caseInfoScrollForward")
        element.click()
        return True
    except NoSuchElementException:
        print("End of results")
        return False

