from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
import csv

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

USERNAME = 'YOUR_USERNAME'
PASSWORD = 'YOUR_PASSWORD'

class FacebookScraper02(object):
    def __init__(self, url):
        self.url = url

        chrome_options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--start-fullscreen")
        self.driver = webdriver.Chrome('E:/ChromeDriver/chromedriver.exe', chrome_options=chrome_options)
        self.delay = 5

    def load_facebook_url(self, useName, passWord):
        self.driver.get(self.url)
        self.driver.find_element_by_id('email').send_keys(useName)
        self.driver.find_element_by_id('pass').send_keys(passWord)
        self.driver.find_element_by_id('loginbutton').click()

        time.sleep(5)
        # try:
        #     wait = WebDriverWait(self.driver, self.delay)
        #     wait.until(EC.presence_of_element_located((By.ID, "searchform")))
        #     print("Page is ready")
        # except TimeoutException:
        #     print("Loading took too much time")

    def extract_member_link(self):
        # all_member = self.driver.find_elements_by_xpath("//div[contains(@class, '_60ri')]")
        dictionaryMember = {}

        SCROLL_PAUSE_TIME = 5

        numberScroll = 1
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            print('scroll: {}'.format(numberScroll))
            numberScroll = numberScroll + 1
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            try:
                wait = WebDriverWait(self.driver, self.delay)
                # scroolValue = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a"))).get_attribute("role")
                scroolValue = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe"))).get_attribute("scrolling")
                # .get_attribute("scrolling")
                # aria-labelledby

                print(scroolValue)
                # print(scroolValue.text)
                print("Skip Scrolling")
            except TimeoutException:
                print("Loading took too much time")

            if new_height == last_height:
                break
            last_height = new_height


        print('end scroll')
        print('start get member')
        all_member = self.driver.find_elements_by_xpath("//div[contains(@class, '_60ri')]")
        for member in all_member:
            link = member.find_element_by_css_selector('a').get_attribute('href')
            # print(member.text)
            # print(all_link)
            dictionaryMember[link] = member.text

        print('end get member')
        csv_file = "Names.csv"
        csv_columns = ['Link', 'Name']

        print('start write data to csv')
        with open(csv_file, 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # writer.writerow(csv_columns)
            for link, name in dictionaryMember.items():
                writer.writerow([link, name])

        print('===End Game===')


# Eg: "https://www.facebook.com/groups/1234567890/members/"
url = "YOUR_LINK_FACEBOOK"

scraper = FacebookScraper02(url)
scraper.load_facebook_url(USERNAME, PASSWORD)
scraper.extract_member_link()