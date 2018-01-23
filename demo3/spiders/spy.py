import scrapy
import re
import json

from scrapy import Selector
from selenium import webdriver

from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from demo3.items import Demo3Item




class demo3(CrawlSpider):
    name = "demo"

    # def __init__(self, *args, **kwargs):
    #     super(demo3, self).__init__(*args, **kwargs)
    #
    #     self.start_urls = [kwargs.get('start_url')]

    allowed_domains = ["muditasol.weebly.com"]
    start_urls = ["http://muditasol.weebly.com/"]
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)


    def parse_items(self, response):

        items = []

        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            if is_allowed:
                item = Demo3Item()
                item['url_from'] = response.url
                item['url_to'] = link.url
                items.append(item)

        #print(response.xpath("//label/text()|//div/text()|//p/text|//h2/text()|//span/text()").re(r'(?!\s)[\w]+'))

        #driver = webdriver.Chrome("C:\\Users\\Virus\\Downloads\\Compressed\\chromedriver_win32\\chromedriver.exe")

        #print(response.xpath("//label/text()|//div/text()|//p/text|//h2/text()|//span/text()").re(r'(?!\s)[\w]+'))
        with open('at.json', 'r') as f:
            dis_dict = json.load(f)
        for i in dis_dict:
            try:
                #driver.get(response.url)
                #next = driver.find_element_by_name(i['Name'])
                next = response.xpath('//input[@type="text"]|//input[@type="email"]|//input[@type="password"]').extract()
                if next:
                    driver = webdriver.Chrome("C:\\Users\\Virus\\Downloads\\Compressed\\chromedriver_win32\\chromedriver.exe")
                    driver.get(response.url)

                    inp = driver.find_elements_by_css_selector('input')
                    for el in inp:
                        #driver.find_element_by_name(distro['Name']
                        for distro in dis_dict:
                            if el.get_attribute('name')==distro['Name']:
                                el.send_keys(distro['value'])

                    #for distro in dis_dict:
                        #driver.find_element_by_name(distro['Name']).send_keys(distro['value'])
                    #driver.find_element_by_class_name("wsite-button").click()
                    bt=driver.find_element_by_css_selector('input')
                    for ele in bt:
                        if ele.getAttribute('type')== 'submit':
                            ele.click()
                    #page = response.url.split("/")[-1]
                    #if page == '':
                    #    filename = 'quotes-Home%s.html' % page
                    #else:
                    #    filename = 'quotes-%s.html' % page
                    #print("FileName: ", filename)

                    #with open(filename, 'wb') as f:
                    #    f.write(response.body)
                    #self.log('Saved file %s' % filename)
                    driver.close()
            except:
                driver.close()
                break
        ar = response.xpath("//label/text()|//div/text()|//p/text()|//h2/text()|//span/text()").re(r'(?!\s)[\w]+')
        thefile = open('test.txt', 'w+')
        for item in ar:
            thefile.write("%s\n" % item)
        page = response.url.split("/")[-1]
        if page == '':
            string = 'Home%s.html' % page
            filename =''.join(e for e in string if e.isalnum())


        else:
            string = '%s.html' % page
            filename = ''.join(e for e in string if e.isalnum())

        print("FileName: ", filename)

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        return items