# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
from ..items import DatasetsItem
class DataSpider(scrapy.Spider):
    name = 'data'
    allowed_domains = ['archive.ics.uci.edu']
    start_urls = ['http://archive.ics.uci.edu/ml/datasets.php?tdsourcetag=s_pctim_aiomsg']
    
    base_url_of_desc = 'http://archive.ics.uci.edu/ml/datasets/'   # 数据集描述页面
    base_url_of_data = 'https://archive.ics.uci.edu/ml/'        # 数据集页面

    def parse(self, response):
        page = etree.HTML(response.text)
        xpath = '//table/tr/td/a/@href'
        hrefs = page.xpath(xpath)
        paths = [x[9:] for x in hrefs]
        for path in paths:
            item = DatasetsItem()
            item['save_folder'] = path
            desc_url = self.base_url_of_desc + path
            yield scrapy.Request(url=desc_url, meta={'item': item}, callback=self.parse_desc)
    
    def parse_desc(self, response):
        item = response.meta['item']
        page = etree.HTML(response.text)
        xpath = '//table/tr/td/p/span//a[1]/@href'
        path = page.xpath(xpath)[0][3:]
        dataset_url = self.base_url_of_data + path
        yield scrapy.Request(url=dataset_url, meta={'item': item}, callback=self.parse_dataset)
    

    def parse_dataset(self, response):
        dataset_url = response.url
        dataset_url = dataset_url.strip('/') + '/'
        page = etree.HTML(response.text)
        xpath = '//ul/li/a/@href'
        paths = page.xpath(xpath)[1:]
        file_urls = [dataset_url + x for x in paths]

        former_item = response.meta['item']
        save_folder = former_item['save_folder']
        for i, file_url in enumerate(file_urls):
            item = DatasetsItem()
            item['save_folder'] = save_folder
            item['name'] = paths[i]
            item['file_urls'] = [file_url]
            yield item

       

