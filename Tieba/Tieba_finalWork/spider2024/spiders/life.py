import scrapy
from scrapy import Selector
from spider2024.items import TiebaItem

class LifeSpider(scrapy.Spider):
    name = 'life'
    allowed_domains = ['tieba.baidu.com']
    start_urls = []

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # 定义不同类型的URL和对应的类型
        url_patterns = [
            ('https://tieba.baidu.com/f/index/forumpark?cn=&ci=0&pcn=%E9%9F%B3%E4%B9%90&pci=0&ct=1&st=new&pn={}', '音乐歌曲'),
            ('https://tieba.baidu.com/f/index/forumpark?pcn=%E6%B8%B8%E6%88%8F&pci=0&ct=1&rn=20&pn={}', '游戏'),
            ('https://tieba.baidu.com/f/index/forumpark?pcn=%E4%BD%93%E8%82%B2%E8%BF%B7&pci=275&ct=0&rn=20&pn={}', '体育运动'),
            ('https://tieba.baidu.com/f/index/forumpark?pcn=%E5%9C%B0%E5%8C%BA&pci=0&ct=1&rn=20&pn={}', '地区'),
            ('https://tieba.baidu.com/f/index/forumpark?pcn=%E5%8A%A8%E6%BC%AB%E5%AE%85&pci=206&ct=0&rn=20&pn={}', '动漫漫画'),
            ('https://tieba.baidu.com/f/index/forumpark?pcn=%E5%B0%8F%E8%AF%B4&pci=161&ct=0&rn=20&pn={}', '小说'),
            ('https://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn={}', '娱乐明星'),
            ('https://tieba.baidu.com/f/index/forumpark?cn=&ci=0&pcn=%E7%A4%BE%E4%BC%9A&pci=0&ct=1&st=new&pn={}', '社会生活')
        ]

        for pattern, category in url_patterns:
            for page in range(1, 31):  # 循环生成1到30页的URL
                url = pattern.format(page)
                yield scrapy.Request(url, headers=headers, meta={'type': category})

    def parse(self, response):
        self.log(response.text)
        sel = Selector(response)
        list_items = sel.css("#ba_list > div")
        print(f"Found {len(list_items)} items")
        for list_item in list_items:
            tieba_item = TiebaItem()
            tieba_item["name"] = list_item.css("a > div > p.ba_name::text").get()
            tieba_item["member"] = list_item.css("a > div > p.ba_num.clearfix > span.ba_m_num::text").get()
            tieba_item["comment"] = list_item.css("a > div > p.ba_num.clearfix > span.ba_p_num::text").get()
            tieba_item["main"] = list_item.css("a > div > p.ba_desc::text").get()
            tieba_item["type"] = response.meta.get('type')  # 从meta中获取类型
            print("能够抓取到：" + str(tieba_item))
            yield tieba_item