import os
from scrapy import cmdline
# os.popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="F:\chrom"')
cmdline.execute("scrapy crawl DIY -o DIY.csv".split())