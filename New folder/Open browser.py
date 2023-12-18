import traceback
from selenium.webdriver.chrome.options import Options
import threading
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import chromedriver_autoinstaller
import time
import psutil
import json
import pandas as pd
import random
import csv

class BeenVerifiedScraping():
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--profile-directory=Default")
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--disable-plugins-discovery")
        self.chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

    def startChrome(self):
        return os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222')

    def closeBrowser(self):
        try:
            PROCNAME = "chromedriver.exe"
            userName = os.getlogin()
            for proc in psutil.process_iter():
                # check whether the process name matches

                if proc.name() == PROCNAME or proc.name() == 'chrome.exe':
                    if str(userName) in str(proc.username()):
                        print(str(proc.name()))
                        print(proc.username())
                        proc.kill()
        except Exception as ex:
            print(str(ex))


    def startScraping(self):
        path = chromedriver_autoinstaller.install(cwd=True)
        print(path)
        time.sleep(2)

        self.closeBrowser()
        time.sleep(2)

        th = threading.Thread(target=self.startChrome, args=())
        th.daemon = True
        th.start()
        time.sleep(3)

        driver = webdriver.Chrome(options=self.chrome_options)

        driver.get('https://www.rightmove.co.uk/properties/127254773#/?channel=RES_BUY')
        
if __name__ == '__main__':
    beenVerified=BeenVerifiedScraping()
    beenVerified.startScraping()
