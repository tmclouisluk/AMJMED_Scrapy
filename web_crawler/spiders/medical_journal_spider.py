import scrapy
from selenium import webdriver

class MedicalJournalSpider(scrapy.Spider):
    name = "medical_journal"
    urls = [
        'http://www.amjmed.com/issues',
    ]

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:\chromedriver.exe')

    def __del__(self):
        self.browser.close()

    def start_requests(self):
        self.browser.get(self.urls[0])
        req = scrapy.Request(url=self.urls[0], callback=self.parse)
        yield req

    def parse(self, response):
        print (self.browser.page_source)
        #list = list[0]

    #def parse_journal_list(self, response):
