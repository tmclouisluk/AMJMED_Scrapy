import scrapy


class MedicalJournalSpider(scrapy.Spider):
    name = "medical_journal"

    def start_requests(self):
        urls = [
            'http://www.amjmed.com/issues',
        ]
        for i, url in enumerate(urls):
            req = scrapy.Request(url=url, callback=self.parse)
            #req.headers['Cookie'] = 'js_enabled=true; is_cookie_active=true;'
            yield req

    def parse(self, response):

        list = response.css('.width_1_2')
        #list = list[0]

    #def parse_journal_list(self, response):
