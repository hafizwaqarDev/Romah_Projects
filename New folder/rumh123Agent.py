import requests , json
import cloudscraper, csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import  service
from googletrans import Translator
from lxml.html import fromstring

class rumh123Scraper():
    def __init__(self) -> None:
        pass
    
    def header(self):
        open(file='rumh123Agent.csv',mode='a').close()
        header = ['Agent Name','Agent Address','Phone Number','Watsapp Number','Email']
        with open(file='rumh123Agent.csv',mode='r') as file:
            readData = csv.reader(file)
            if header not in readData:
                with open(file='rumh123Agent.csv',mode='a',newline='',encoding='UTF-8') as file:
                    csv.writer(file).writerow(header)

    def openBrowser(self,inputUserAgent):
        driver = webdriver.Chrome()
        search = f'https://www.rumah123.com/agen-properti/?q={inputUserAgent}&sort=NEW_LISTING'
        driver.get(search)
        return driver
    
    def inputSearch(self):
        inputUserAgent = input('enter your Agent Name:- ')
        return inputUserAgent

    def scrollDown(self,driver):
        time.sleep(5)
        for page in range(7):
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        
    def loadmore(self,driver):
        try:
            clickElement = driver.find_element(By.XPATH,'//button[@class="load-more"]')
            clickElement.click()
            time.sleep(1)
        except: pass

    def pageResp(self,driver):
        self.scrollDown(driver)
        self.loadmore(driver)
        time.sleep(1)
        self.scrollDown(driver)
        self.loadmore(driver) 
        driver.page_source
        soupTree = fromstring(driver.page_source)
        urlsTag = soupTree.xpath('//a[@class="title"]')
        agentLink = ['https://www.rumah123.com' + url.get('href') for url in urlsTag]
        return agentLink
    
    def find_telephone(self,data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "telephone":
                    return value
                if isinstance(value, (dict, list)):
                    result = self.find_telephone(value)
                    if result is not None:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = self.find_telephone(item)
                if result is not None:
                    return result
        return None
    
    def translate_indonesian_to_english(self,text):
        translator = Translator()
        translated = translator.translate(text, src='id', dest='en')
        return translated.text
    
    def parseData(self,agentLink):
        for link in agentLink:  
            time.sleep(2)  
            agentscraper = cloudscraper.CloudScraper()
            AgentpageResponse = agentscraper.get(link)
            html_content = AgentpageResponse.text
            agentSoupTree = fromstring(html_content)
            try: 
                agentNameTag = agentSoupTree.find('.//div[@class="agency__name"]').text_content().strip()
                agentName = self.translate_indonesian_to_english(agentNameTag)
            except:
                agentname = agentSoupTree.find('.//div[@class="top-section__card__column-1 separator"]/h1').text_content().strip()
                agentName = self.translate_indonesian_to_english(agentname)
            try: 
                agentAdresst = agentSoupTree.find('.//p[@class="agency__address"]').text_content()
                # city = agentAdress.split()[-2]
                agentAdress = self.translate_indonesian_to_english(agentAdresst)
            except: 
                # city = ''
                agentAdress = ''
            soup = BeautifulSoup(html_content, 'html.parser')
            section = soup.find('section')
            script = section.find_next_sibling('script')
            if script:
                json_data = json.loads(script.string)
            else:
                print("Script tag not found.")
            phoneNumber = self.find_telephone(json_data)
            watsappNumber = phoneNumber
            box = agentSoupTree.find('.//div[@class="top-section__card__column-1 separator"]').text_content().split()
            email = ''
            for data in box:
                if '@' in data:
                    emailt = data
                    email = self.translate_indonesian_to_english(emailt)
                    break
                else:
                    email = ''
            print(f'[Info] Getting data of this agent:- {agentName}')
            row = [agentName,agentAdress,phoneNumber,watsappNumber,email]
            self.saveData(row)

    def saveData(self,row):
        with open(file='rumh123Agent.csv',mode='a',newline='',encoding='UTF-8') as file:
            csv.writer(file).writerow(row)
    
    def run(self):
        inputUserAgent = self.inputSearch()
        driver = self.openBrowser(inputUserAgent)
        agenLink = self.pageResp(driver)
        self.parseData(agenLink)

myclass = rumh123Scraper()
myclass.header()
myclass.run()

    