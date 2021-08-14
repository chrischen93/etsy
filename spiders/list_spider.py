# -*- coding: utf-8 -*-
"""
Created on 2021-03-19 20:49:40
---------
@summary:
---------
@author: lanba
"""

import feapder
from items import *


class ListSpider(feapder.Spider):
    def start_requests(self):
        yield feapder.Request('https://www.etsy.com/c/jewelry-and-accessories?ref=catnav-10855',render=True)

    def parse(self, request, response):
        product_list=response.xpath('//li[contains(@class,"wt-list-unstyled")]')
        for product in product_list:
            list_url=product.xpath('.//a[contains(@class, "listing-link")]/@href').extract_first()
            temp=list_url.find('?')
            list_url=list_url[:temp]
          
            # 详情任务
            
            detail_task_item = etsy_detail_task_item.EtsyDetailTaskItem()
            detail_task_item.url = list_url
            yield detail_task_item  # 直接返回，框架实现批量入库


# if __name__ == "__main__":
#     # redis_key="feapder:lagou_list"
#     spider = ListSpider(redis_key='test')
#     spider.start()
