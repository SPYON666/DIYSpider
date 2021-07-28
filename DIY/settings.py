# Scrapy settings for DIY project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'DIY'
LOG_LEVEL = 'DEBUG'
SPIDER_MODULES = ['DIY.spiders']
NEWSPIDER_MODULE = 'DIY.spiders'

DOWNLOAD_DELAY = 0.1
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'DIY (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

FEED_EXPORT_ENCODING = 'gb18030'
SPLASH_URL = 'http://127.0.0.1:8050'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT =  'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36 Edg/91.0.864.64'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
# CLOSESPIDER_ITEMCOUNT = 400

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP =2
# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# COOKIES_DEBUG= True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
RETRY_TIMES = 3
RETRY_HTTP_CODECS = [500, 502, 503, 504, 408, 404, 403, 400]
# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Cookie':"bid=rMoDrjEnYEU; douban-fav-remind=1; push_noty_num=0; push_doumail_num=0; __utmv=30149280.24140; _ga=GA1.2.217124707.1625638151; __utmc=30149280; __utmz=30149280.1626066990.27.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __gads=ID=fb2d24e2ee5a7a11-2264d91d4cca0007:T=1626082271:RT=1626082271:S=ALNI_MZ_BKnR33COjZOmqaFJ7NwGnFGL2w; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1626153124%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.217124707.1625638151.1626143062.1626153126.33; __yadk_uid=x3YJ8yE1I7vQeH7NmKk5QHnmiCSpk9Hj; ap_v=0,6.0; __utmt=1; ck=47RI; _pk_id.100001.8cb4=d4a05eeabd5109ae.1625638151.33.1626159697.1626148108.; __utmb=30149280.47.9.1626159697699"
# }
# USER_AGENT ='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'scrapy_splash.SplashDeduplicateArgsMiddleware':100
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'DIY.middlewares.DIYDownloaderMiddleware': 543,
   'scrapy_splash.SplashCookiesMiddleware' : 725,
   'scrapy_splash.SplashMiddleware':723,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware':810
}
# ITEM_PIPELINES = {
#     'DouBan.pipelines.DoubanPipeline': 300
# }
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'DouBan.pipelines.DoubanPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
