# DIYSpider
**功能**：根据输入的XPATH和URL自动进行页面爬取

**URL.txt**：填写要爬取的页面的URL地址

**context.json**：填写特定格式的json结构，用来表明爬取的内容

**json文件格式说明**：

page：选择true或false表明是否需要翻页

scroll：-1表示下滑到底部，0表示不需要下滑，n>0表示下滑n次

content：表明要抓取的字段名以及对应的声明

    当说明为XPATH字符串：在对应页面只需要捕获一次该元素，比如页面大标题
    当说明为json格式：在对应页面中需要循环捕获多个相似元素，比如视频列表，话题列表，该json中需要填充
    xpath：相同元素构成的列表的xpath
    列表中每个子元素需要抓取内容的字段名以及该内容相对于该子元素的XPATH
    比如：content中的Video元素列表声明：
    "Video": {
      "xpath":"//li[@class='video-item matrix']",
      "data":".//span[@title='观看']/text()",
      "title":".//a[@class='title']/text()"
    }

