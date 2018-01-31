import scrapy
from scrapy import Selector

class MedicalJournalSpiderDebug(scrapy.Spider):
    name = "medical_journal_debug"
    urls = [
        'http://www.amjmed.com/article/S0002-9343(16)30598-8/fulltext',
    ]

    def start_requests(self):
        req = scrapy.Request(url=self.urls[0], callback=self.parse)
        req.meta['ChromeJS'] = True
        yield req

    def parse(self, response):
        showReference = response.css(".showReferences.tabtitle::text").extract_first()

        if showReference is not None:
            title = response.css(".articleTitle::text").extract_first()
            authors = response.css(".author a.openAuthorLayer::text").extract()
            pubDate = response.css(".pubDatesRow::text").extract_first()
            if pubDate is None:
                pubDate = response.css(".artBib a::text").extract_first()
            content = "".join(response.css(".fullText .body .content p::text").extract())
            yield {
                'title': title,
                'authors': authors,
                'pubDate': pubDate,
                'content': content,
                'collection': 'medical_journal'
            }

        # \32 f1be74d-242b-49c7-ade4-2ab90069ea88 > div > div > div > div:nth-child(1)

    def parseIssues(self, response):
        article_list = response.css('.article-details').extract()

        if article_list is not None:
            for article in article_list:
            #if article_list[0] is not None:
                #article = article_list[0]
                selector = Selector(text=article)
                formats = selector.css(".formats a::text").extract()
                if "Full-Text HTML" in formats:
                    link = selector.css(".formats a:not(.pdfLink)::attr(href)").extract_first()
                    yield response.follow(link, self.parseArticle, meta=dict(ChromeJS=True))
                    #title = selector.css(".title a::text").extract_first()
                    #author = selector.css(".authors").extract_first()

    def parseArticle(self, response):
        showReference = response.css(".showReferences.tabtitle::text").extract_first()

        if showReference is not None:
            title = response.css(".articleTitle::text").extract_first()
            authors = response.css(".author a.openAuthorLayer::text").extract()
            pubDate = response.css(".pubDatesRow::text").extract_first()
            if pubDate is None:
                pubDate = response.css(".artBib a::text").extract_first()
            content = "".join(response.css(".fullText .body .content p::text").extract())
            yield {
                'title': title,
                'authors': authors,
                'pubDate': pubDate,
                'content': content,
                'collection': 'medical_journal'
            }
