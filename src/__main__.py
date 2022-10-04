#!/usr/bin/python3
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions


USERNAME = ""
PASSWORD = ""
MESSAGE = ""
MESSAGE_LOCAL = "data/message.txt"
PLACES_LOCAL = "data/places.txt"
PLACES_FAILED_LOCAL = "data/places_failed.txt"

def setupCreds():
    global USERNAME, PASSWORD
    USERNAME = "rodrigolf080@gmail.com"
    PASSWORD = os.environ.get('SR_PASSWD')
    if not PASSWORD or not USERNAME:
        return 0
    return 1

def setupMessage():
    global MESSAGE, MESSAGE_LOCAL
    try:
        with open(MESSAGE_LOCAL, 'r') as h:
            MESSAGE = h.read()
    except:
        return 0
    return 1

def setupDriver():
    #options = FirefoxOptions()
    #options.add_argument("--headless")
    #driver = webdriver.Firefox(options=options)
   
    try:
        driver = webdriver.Firefox()
    except:
        return None

    return driver


def cleanupDriver(driver):
    driver.close()
    return 0

def login(driver):
    uri = "https://www.spareroom.co.uk/flatshare/mythreads_beta.pl"
    driver.get(uri)
    time.sleep(2)
    driver.find_element('id', "onetrust-accept-btn-handler").click()
    time.sleep(1)
    driver.find_element('id', "loginemail").send_keys(USERNAME)
    driver.find_element('id', "loginpass").send_keys(PASSWORD)
    driver.find_element('id', "sign-in-button").click()
    time.sleep(1)
    return 0

def doSpam(driver):
    global MESSAGE, PLACES_LOCAL, PLACES_FAILED_LOCAL
    places = list()
    with open(PLACES_LOCAL, 'r') as h:
        places = h.read().splitlines()
    if '' in places:
        places.pop()
    i = 0
    neg_i = 0
    for place in places:
        i = i + 1
        time.sleep(1)
        driver.get(place)
        time.sleep(1)
        driver.find_element('xpath', "//a[@title='Email advertiser']").click()
        time.sleep(1)
        try:
            driver.find_element('id', "message").send_keys(MESSAGE)
        #time.sleep(1)
        except:
            continue
        try:
            driver.find_element('xpath', "//button[@class='button button--large button--wide']").click()
            sys.stdout.write(f"[{i - neg_i}] Message delivered successfully\n")
        except:
            with open(PLACES_FAILED_LOCAL, 'a') as hf:
                hf.write(f"{place}\n")
            neg_i = neg_i + 1
            sys.stdout.write(f"[{neg_i}] Message failed\n")
        time.sleep(1)

    try:
        os.remove(PLACES_LOCAL)
    except:
        return 0

    return 1


def main():
    if not setupCreds():
        return -1
    
    if not setupMessage():
        return -2 

    driver = setupDriver()
    if not driver:
        return -3
    
    try:
        login(driver)
   
        doSpam(driver)
    except KeyboardInterrupt:
        cleanupDriver(driver)
        return -4

    cleanupDriver(driver)
    return 0


if __name__ == '__main__':
    ret = main()
    if ret:
        ret_msg = ""
        if ret == -1:
            ret_msg = "Error setting up credentials"
        elif ret == -2:
            ret_msg = "Error setting up copywriting message"
        elif ret == -3:
            ret_msg = "Error setting up webdriver"
        elif ret == -4:
            ret_msg = "Error during webdriver execution"
        sys.stderr.write(f"[!] Return Code: {str(ret)}\n")
        if ret_msg:
            sys.stderr.write(f"[!] Error Message: {ret_msg}\n")
    sys.exit(main())
