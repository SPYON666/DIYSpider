import random
import time

import scrapy
from lxml import etree
from pydispatch import dispatcher
from scrapy import signals
from scrapy.signalmanager import SignalManager
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from copy import deepcopy
from  DIY.middlewares import DIYDownloaderMiddleware
import json


class DIYSpider(scrapy.Spider):
    name = 'DIY'
    start_urls = []
    custom_settings = {}
    scroll = 0
    page = False

    def __init__(self, *args, **kwargs):
        self.options = ChromeOptions()
        # self.options.add_argument("--headless")  # => 为Chrome配置无头模式
        # self.options.add_argument("--disable-gpu")
        # self.options.add_experimental_option('excludeSwitches', ['disable-logging'])
        # self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.options.add_experimental_option('useAutomationExtension', False)
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         'images': 2,
        #     }
        # }
        # self.options.add_experimental_option('prefs', prefs)
        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") #采用debug模式，接管现有的浏览器应用程序，从而避免部分网站反爬检测selenium
        self.diybrowser = Chrome(executable_path='chromedriver.exe',options=self.options)
        super(DIYSpider, self).__init__(*args, **kwargs)


        f = open('url.txt', encoding='utf8')
        self.start_urls = f.readlines()
        f.close()
        f = open('content.json','r',encoding='utf8')
        js = json.load(f)
        self.content = js["content"]
        self.scroll = js["scroll"]
        self.page = js["page"]
        f.close()

        itemContent = deepcopy(self.content)
        item = {}
        for key,value in itemContent.items():
            item[key] = scrapy.Field()
        self.DIYItem = type('DIYItem',(scrapy.Item,),item)

        SignalManager(dispatcher.Any).connect(
            self.closed_handler, signal=signals.spider_closed)


    def closed_handler(self, spider):
        self.diybrowser.quit()


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
        self.item_init(item,self.content)
        self.diybrowser.execute_cdp_cmd("Emulation.setUserAgentOverride", {
            "userAgent": random.choice(DIYDownloaderMiddleware.user_agent_list)
        })
        self.diybrowser.get(response.url)
        time.sleep(1)
        page = self.page
        while True:
            try:
                WebDriverWait(self.diybrowser, 2).until(
                    EC.presence_of_element_located((By.XPATH,'//*[text() = "1"]'))
                )
                tree = etree.HTML(self.diybrowser.page_source)
                element_name = tree.xpath('local-name(//*[text() = "1"])')
                element = self.get_element(self.diybrowser,'//%s[text() = "1"]/../..//%s[last()]'%element_name)
            except:
                print('已到达最后一页或未找到翻页按钮','\n')
                page = False
            finally:
                self.get_page(item)
                time.sleep(random.uniform(0.5,1))
                if page == False:
                    break
                element.click()
        yield item


    def get_element(self,element,xpath):
        try:
            ele = element.find_element_by_xpath(xpath)
            return ele
        except:
            print('该元素不存在，填充为None','\n')
            ele = None
            return ele


    def get_page(self,item):
        temp_height = 0
        scroll = self.scroll
        while scroll == -1 or scroll > 0:
            self.diybrowser.execute_script('window.scrollBy(0,5000)')
            time.sleep(0.25)
            check_height = self.diybrowser.execute_script(
                "return document.body.scrollHeight;")
            if check_height == temp_height:
                break
            temp_height = check_height
            if scroll > 0:
                scroll = scroll - 1
        self.get_item(item, self.content)


    def item_init(self,item,content):
        for key,value in content.items():
            if type(value) is not str:
                item[key] = []

    def get_item(self,item,content):
        for key,value in content.items():
            if type(value) is str:
                strarr = value.split('/')
                element = self.get_element(self.diybrowser,value.rstrip('/' + strarr[-1]))
                if element != None and strarr[-1].find('@') == 0:
                    item[key] = element.get_attribute((strarr[-1].split('@'))[-1]).strip()
                else:
                    if element != None and strarr[-1].find('text') != -1:
                        item[key] = element.get_attribute('textContent').strip()
            else:
                elements = self.diybrowser.find_elements_by_xpath(value['xpath'])
                for element in elements:
                    map = {}
                    for innerkey, innervalue in value.items():
                        if innerkey == 'xpath':
                            continue
                        strarr = innervalue.split('/')
                        ele = self.get_element(element,innervalue.rstrip('/' + strarr[-1]))
                        if ele != None and strarr[-1].find('@') == 0:
                            map[innerkey] = ele.get_attribute((strarr[-1].split('@'))[-1]).strip()
                        else:
                            if ele != None and strarr[-1].find('text') != -1:
                                map[innerkey] = ele.get_attribute('textContent').strip()
                    item[key].append(map)

