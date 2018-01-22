from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

class chromeMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):

        if request.meta.get('ChromeJS'):
            try:
                driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
                driver.implicitly_wait(20)
                driver.get(request.url)
                content = driver.page_source.encode('utf-8')
                driver.quit()
                return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
            except TimeoutException:
                driver.quit()
