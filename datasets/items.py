# -*- coding: utf-8 -*-
import scrapy

class DatasetsItem(scrapy.Item):
    
    name = scrapy.Field()           # 文件名
    save_folder = scrapy.Field()    # 文件保存到哪个文件夹
    file_urls = scrapy.Field()      # 文件的下载链接， FilesPipeline 需要用到
    files = scrapy.Field()          # 用来保存文件的字段， FilesPipeline需要用到
