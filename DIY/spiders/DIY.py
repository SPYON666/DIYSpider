import time

import scrapy
import re
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from copy import deepcopy
import json


class DIYSpider(scrapy.Spider):
    name = 'DIY'
    start_urls = []
    custom_settings = {}
    scroll = 0

    def __init__(self, theme=None, *args, **kwargs):
        self.theme = theme
        self.options = ChromeOptions()
        self.options.add_argument("--headless")  # => 为Chrome配置无头模式
        self.options.add_argument("--disable-gpu")
        self.options.add_experimental_option('excludeSwitches', ['disable-logging'])
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
            }
        }
        self.options.add_experimental_option('prefs', prefs)
        # self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") #采用debug模式，接管现有的浏览器应用程序，从而避免部分网站反爬检测selenium
        self.diybrowser = Chrome(options=self.options)
        super(DIYSpider, self).__init__(*args, **kwargs)
        f = open('url.txt', encoding='utf8')
        self.start_urls = f.readlines()
        f.close()
        f = open('content.json','r',encoding='utf8')
        js = json.load(f)
        self.content = js["content"]
        self.scroll = js["scroll"]
        f.close()
        itemContent = deepcopy(self.content)
        item = {}
        for key,value in itemContent.items():
            item[key] = scrapy.Field()
        self.DIYItem = type('DIYItem',(scrapy.Item,),item)


    def start_requests(self):
        # 登录之后用 chrome 的 debug 工具从请求中获取的 cookies
        # 携带 cookies 的 Request 请求
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
            )

    def parse(self, response):
        item = self.DIYItem()
        script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''
        self.diybrowser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.diybrowser.get(response.url)
        time.sleep(1)
        temp_height = 0
        scroll = self.scroll
        while scroll==-1 or scroll > 0:
            self.diybrowser.execute_script('window.scrollBy(0,5000)')
            time.sleep(0.5)
            check_height = self.diybrowser.execute_script(
                "return document.body.scrollHeight;")
            if check_height == temp_height:
                break
            temp_height = check_height
            if scroll > 0:
                scroll = scroll-1
            self.get_item(item,self.content)
        yield item


    def get_element(self,element,xpath):
        try:
            ele = element.find_element_by_xpath(xpath)
            return ele
        except:
            print('该元素不存在，填充为None','\n')
            ele = None
            return ele

    def get_item(self,item,content):
        for key,value in content.items():
            if type(value) is str:
                strarr = value.split('/')
                element = self.get_element(self.diybrowser,value.rstrip('/' + strarr[-1]))
                if element != None and strarr[-1].find('@') == 0:
                    item[key] = element.get_attribute((strarr[-1].split('@'))[-1])
                else:
                    if element != None and strarr[-1].find('text') != -1:
                        item[key] = element.get_attribute('textContent')
            else:
                elements = self.diybrowser.find_elements_by_xpath(value['xpath'])
                elementlist = []
                for element in elements:
                    map = {}
                    for innerkey, innervalue in value.items():
                        if innerkey == 'xpath':
                            continue
                        strarr = innervalue.split('/')
                        ele = self.get_element(element,innervalue.rstrip('/' + strarr[-1]))
                        if ele != None and strarr[-1].find('@') == 0:
                            map[innerkey] = ele.get_attribute((strarr[-1].split('@'))[-1])
                        else:
                            if ele != None and strarr[-1].find('text') != -1:
                                map[innerkey] = ele.get_attribute('textContent')
                    elementlist.append(map)
                item[key] = elementlist

