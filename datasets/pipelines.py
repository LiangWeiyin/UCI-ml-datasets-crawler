# -*- coding: utf-8 -*-

import scrapy
import pdfkit
import os
from scrapy.pipelines.files import FilesPipeline

class DatasetsFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        name = item['name']
        save_folder = item['save_folder']
        return '%s/%s' % (save_folder, name)

class DatasetsDescPdfPipeline(object):    # 下载数据集的描述页面，并转换为pdf
    def process_item(self, item, spider):
        folder = "D:\\E-pan\\scrapy\\Datasets\\%s" % item['save_folder']
        path = "D:\\E-pan\\scrapy\\Datasets\\%s\\%s" % (item['save_folder'], item['name'])
        if not os.path.exists(folder):
            os.makedirs(folder)
        pdfkit.from_url(item['file_urls'], path)