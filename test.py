from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path="C:/chromedriver.exe")

browser.get("http://www.amjmed.com/issues")
t_selector = Selector(text=browser.page_source)
print (t_selector.css(".tm-price::text").extract())
# print (browser.page_source)
browser.quit()

