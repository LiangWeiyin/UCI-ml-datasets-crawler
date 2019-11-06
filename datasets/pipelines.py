# -*- coding: utf-8 -*-
from scrapy.pipelines.files import FilesPipeline
import scrapy

class DatasetsFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        name = item['name']
        save_folder = item['save_folder']
        return '%s/%s' % (save_folder, name)