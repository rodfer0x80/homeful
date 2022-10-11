#!/usr/bin/python3
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from .logger import *

class Bot:
    def __init__(self, run_mode="spam"):
        self.DATA_LOCAL = "data"
        self.MESSAGE_LOCAL = f"{self.DATA_LOCAL}/message.txt"
        self.PLACES_LOCAL = f"{self.DATA_LOCAL}/places.txt"
        self.PLACES_SEARCH_LOCAL = f"{self.DATA_LOCAL}/places_search.txt"
        self.PLACES_SPAMMED_LOCAL = f"{self.DATA_LOCAL}/places_spammed.txt"
        self.PLACES_FAILED_LOCAL = f"{self.DATA_LOCAL}/places_failed.txt"

        self.logger = Logger()

        try:
            self.USERNAME = os.environ.get('HM_MAIL')
            self.PASSWORD = os.environ.get('HM_PASS')
        except:
            _msg = "[x] (1) Error reading credentials from env vars\n"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
            sys.exit(-1)
        
        try:
            with open(self.MESSAGE_LOCAL, 'r') as h:
                self.MESSAGE = h.read()
        except:
            _msg = "[x] (2) Error reading from message file\n"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
            sys.exit(-2)
        
        try:
            ## Headless
            # options = FirefoxOptions()
            # options.add_argument("--headless")
            # driver = webdriver.Firefox(options=options)
            self.DRIVER = webdriver.Firefox()
        except:
            _msg = "[x] (3) Error setting up browser driver\n"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
            sys.exit(-3)

        if run_mode == "search" or run_mode == "Search":
            self.SEARCH_MODE = True
        else:
            self.SEARCH_MODE = False

        return None

    def cleanupDriver(self):
        try:
            self.DRIVER.close()
        except:
            _msg = "[x] (4) Error closing browser driver\n"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
        return 0

    def login(self):
        try:
            uri = "https://www.spareroom.co.uk/flatshare/mythreads_beta.pl"
            self.DRIVER.get(uri)
            time.sleep(1)
            time.sleep(1)
            self.DRIVER.find_element('id', "onetrust-accept-btn-handler").click()
            time.sleep(1)
            self.DRIVER.find_element('id', "loginemail").send_keys(self.USERNAME)
            self.DRIVER.find_element('id', "loginpass").send_keys(self.PASSWORD)
            self.DRIVER.find_element('id', "sign-in-button").click()
            time.sleep(1)
        except:
            _msg = "[x] (5) Error logging in with browser driver\n"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
        return 0

    def spam(self):
        places = list()
        try:
            with open(self.PLACES_LOCAL, 'r') as h:
                places = h.read().splitlines()
        except FileNotFoundError:
            _msg = "[x] (7) Error reading from places.txt"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
            return 0
        if '' in places:
            places.pop()
        i = 0
        neg_i = 0
        for place in places:
            i = i + 1
            time.sleep(1)
            self.DRIVER.get(place)
            time.sleep(1)
            self.DRIVER.find_element('xpath', "//a[@title='Email advertiser']").click()
            time.sleep(1)
            try:
                self.DRIVER.find_element('id', "message").send_keys(self.MESSAGE)
                time.sleep(1)
            except:
                continue
            try:
                self.DRIVER.find_element('xpath', "//button[@class='button button--large button--wide']").click()
                sys.stdout.write(f"[{i - neg_i}] Message delivered successfully\n")
            except:
                with open(self.PLACES_FAILED_LOCAL, 'a') as hf:
                    hf.write(f"{place}\n")
                neg_i = neg_i + 1
                sys.stdout.write(f"[{neg_i}] Message failed\n")
            time.sleep(1)

        try:
            with open(self.PLACES_LOCAL, 'r') as hp:
                with open(self.PLACES_SPAMMED_LOCAL, 'a') as hpp:
                    hpp.write(hp.read())
            os.remove(self.PLACES_LOCAL)
        except:
            _msg = "[x] (7) Error cleaning up places_spammed.txt"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
            return 0
        return 0

    def search(self):
        search_uri = "https://www.spareroom.co.uk/flatshare/search.pl"
        places = list()
        try:
            with open(self.PLACES_SEARCH_LOCAL, 'r') as hc:
                cities = hc.read().splitlines()
            if '' in cities:
                cities.pop()
        except FileNotFoundError:
            _msg = "[x] (8) Error cleaning up places.txt"
            self.logger.log(_msg)
            sys.stderr.write(_msg)
            return 0
        done = False
        for city in cities:
            done = False
            self.DRIVER.get(search_uri)
            time.sleep(1)
            self.DRIVER.find_element('id', "search_by_location_field").send_keys(city)
            time.sleep(1)
            try:
                self.DRIVER.find_element('xpath', "//div[@class='autocomplete-suggestion']").click()
            except:
                continue
            #time.sleep(1)
            self.DRIVER.find_element('id', "search-button").click()
            while not done:
                places = list()
                #i = 10
                try:
                    elems = self.DRIVER.find_elements('xpath', "//a[@href]")
                    links = [elem.get_attribute('href') for elem in elems]
                    for link in links:
                        if "flatshare_detail.pl" in link:
                            places.append(link)
                    try:
                        with open(self.PLACES_LOCAL, 'a') as h:
                            for place in places:
                                h.write(f"{place}\n")
                            places = list()
                    except FileNotFoundError:
                        _msg = "[x] (8) Error appending to places.txt"
                        self.logger.log(_msg)
                        sys.stderr.write(_msg)
                        sys.exit(0)
                    try:
                        # click a id paginationNextPageLink
                        # ?offset={i}
                        # driver.find_element('xpath', "//div[@class='autocomplete-suggestion']").click()
                        self.DRIVER.find_element('id', "paginationNextPageLink").click()
                        time.sleep(1)
                        # i += 10
                    except:
                        done = True
                        continue
                except KeyboardInterrupt:
                    _msg = "[!] Gracefully quitting"
                    self.logger.log(_msg)
                    sys.stdout.write(_msg)
                    sys.exit(0)
        return 0

    def runme(self):
        self.login()
        if self.SEARCH_MODE:
            self.search()
        else:
            self.spam()
        self.cleanupDriver()
        return 0


