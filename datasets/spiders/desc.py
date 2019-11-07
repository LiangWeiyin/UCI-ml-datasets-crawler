# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from ..items import DatasetsItem

class DescSpider(scrapy.Spider):
    name = 'desc'
    allowed_domains = ['archive.ics.uci.edu']
    start_urls = ['http://archive.ics.uci.edu/ml/datasets.php?tdsourcetag=s_pctim_aiomsg']

    base_url_of_desc = 'http://archive.ics.uci.edu/ml/datasets/'   # 数据集描述页面

    def parse(self, response):
        page = etree.HTML(response.text)
        xpath = '//table/tr/td/a/@href'
        hrefs = page.xpath(xpath)
        paths = [x[9:] for x in hrefs]
        for path in paths:
            desc_url = self.base_url_of_desc + path
            item = DatasetsItem()
            item['save_folder'] = path
            item['name'] = '{}.pdf'.format(path)
            item['file_urls'] = [desc_url]
            yield item
