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
DATA_LOCAL = "./data"
MESSAGE_LOCAL = f"{DATA_LOCAL}/message.txt"
PLACES_LOCAL = f"{DATA_LOCAL}/places.txt"
PLACES_SPAMMED_LOCAL = f"{DATA_LOCAL}/places_spammed.txt"
PLACES_FAILED_LOCAL = f"{DATA_LOCAL}/places_failed.txt"

SEARCH_MODE = False
RET = 0

def setupCreds():
    global USERNAME, PASSWORD
    USERNAME = os.environ.get('HM_MAIL')
    PASSWORD = os.environ.get('HM_PASS')
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
    try:
        ## Headless
        # options = FirefoxOptions()
        # options.add_argument("--headless")
        # driver = webdriver.Firefox(options=options)
        
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
        os.system(f"cat {PLACES_LOCAL} >> {PLACES_SPAMMED_LOCAL}")
    except:
        return 0

    return 1

def doSearch(driver):
    global PLACES_LOCAL, CITIES_LOCAL
    
    places = list()
    try:
        with open(CITIES_LOCAL, 'r') as hc:
            cities = hc.read().splitlines()
        if '' in cities:
            cities.pop()
    except:
        return -6

    done = False
    
    for city in cities:
        # find places
        time.sleep(1)
        # append them to places
        try:
            with open(PLACES_LOCAL, 'a') as h:
                h.write(f"{place}\n")
        except:
            return -7
    
    try:
        os.system(f"cat {PLACES_LOCAL} >> {PLACES_SPAMMED_LOCAL}")
    except:
        return -8

    return 1

def runme():
    global SEARCH_MODE

    if not setupCreds():
        return -1
    
    if not setupMessage():
        return -2 
    
    driver = setupDriver()
    if not driver:
        return -3
    
    #login(driver)
        
    if SEARCH_MODE:
        doSearch(driver)
    if not doSpam(driver):
        return -4

    cleanupDriver(driver)
    
    return -5

    cleanupDriver(driver)
    return 0


def main():
    global RET, SEARCH_MODE
    if len(sys.argv) > 1:
        run = sys.argv[1]
    
    if run == "search":
        SEARCH_MODE = True
    elif run == "spam":
        SEARCH_MODE = False
    else:
        RET = 1
    
    if not RET:
        try:
            runme()
        except KeyboardInterrupt:
            return RET
    if RET:
        _msg = ""
        if RET == 1:
            _msg = f"Usage {sys.argv[0]} <mode spam/search>"
        elif RET == -1:
            _msg = "Error setting up credentials"
        elif RET == -2:
            _msg = "Error setting up copywriting message"
        elif RET == -3:
            _msg = "Error setting up webdriver"
        elif RET == -4:
            _msg = "Error s"
        elif RET == -5:
            _msg = "Error during webdriver execution"
        sys.stderr.write(f"[!] Return Code: {str(RET)}\n")
        if _msg:
            sys.stderr.write(f"[!] Error Message: {_msg}\n")
    return RET

if __name__ == '__main__':
    sys.exit(main())
