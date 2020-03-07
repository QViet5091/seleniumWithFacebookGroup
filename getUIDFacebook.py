import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

import time

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class GetUIDFacebook(object):
    def __init__(self,url):
        self.url = url
        chrome_options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome('E:/ChromeDriver/chromedriver.exe', chrome_options=chrome_options)
        self.delay = 3

    def getUID(self, url):

        csv_file = "Names.csv"
        csv_write_file_success = "Result1.csv"
        csv_write_file_false = "False1.csv"

        with open(csv_file, 'r', encoding='utf-8') as csv_file:
            with open(csv_write_file_success, 'w', encoding='utf-8') as csv_write_file_success:
                with open(csv_write_file_false, 'w', encoding='utf-8') as csv_write_file_false:
                    writerFasle = csv.writer(csv_write_file_false)
                    writer = csv.writer(csv_write_file_success)
                    reader = csv.reader(csv_file, delimiter=',')
                    for row in reader:
                        if len(row) > 0:
                            print(row[1])
                            self.driver.get(self.url)
                            time.sleep(1.5)
                            self.driver.find_element_by_name('url').send_keys(row[0])
                            self.driver.find_element_by_css_selector(".btn-primary").click()

                            time.sleep(1.5)
                            code = self.driver.find_element_by_css_selector("code")
                            print(code.text)
                            if 'https://www.facebook.com/' in code.text:
                                writerFasle.writerow([row[0], row[1], code.text])
                            else:
                                writer.writerow([row[0], row[1], code.text])

        csv_file.close()
        csv_write_file_success.close()
        csv_write_file_false.close()
        self.driver.close()



url = "https://findmyfbid.com/"
transformer = GetUIDFacebook(url)
transformer.getUID(url)