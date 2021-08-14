# -*- coding: utf-8 -*-
"""
Created on 2021-03-19 22:12:45
---------
@summary:
---------
@author: lanba
"""

import feapder
from items import *
import re
import json

class DetailSpider(feapder.BatchSpider):
    def start_requests(self, task):
        task_id, url = task
        yield feapder.Request(url, task_id=task_id, render=True)

    def parse(self, request, response):
        list_id=re.findall(r'\d+', request.url)[0]
        # job_name = response.xpath('//div[@class="job-name"]/@title').extract_first().strip()
        # detail = response.xpath('string(//div[@class="job-detail"])').extract_first().strip()
        bs=response.bs4()
        jdata=json.loads(bs.find("script",{"type":"application/ld+json"}).string)
        sale=response.xpath('//span[@class="wt-text-caption"]/text()').extract_first()
        review=response.xpath('//span[@class="wt-badge wt-badge--status-02 wt-ml-xs-2"]/text()').extract_first().strip()
        favorites=response.xpath('//div[contains(@class,"wt-align-items-baseline")]/div/a/text()').extract_first().strip()
        item = etsy_prodcut_detail_item.EtsyProdcutDetailItem()
        item.id = list_id
        item.category =jdata.get("category")
        item.favorites = favorites
        item.price = jdata.get("offers").get('lowPrice')
        item.rating =round( float( jdata.get("ratingValue")) ,2)
        item.review = review
        item.sales = sale
        item.shop = jdata.get("brand")
        item.tags = None
        item.title = jdata.get("name")
        item.description = jdata.get("description")
        item.batch_date = self.batch_date  # 获取批次信息，批次信息框架自己维护
        yield item  # 自动批量入库
        yield self.update_task_batch(request.task_id, 1)  # 更新任务状态


# if __name__ == "__main__":
#     spider = DetailSpider(
#         redis_key="feapder:etsy_detail",  # redis中存放任务等信息的根key
#         task_table="etsy_detail_task",  # mysql中的任务表
#         task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
#         task_state="state",  # mysql中任务状态字段
#         batch_record_table="etsy_detail_batch_record",  # mysql中的批次记录表
#         batch_name="详情爬虫(周全)",  # 批次名字
#         batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
#     )
#
#     # 下面两个启动函数 相当于 master、worker。需要分开运行
#     # spider.start_monitor_task() # 下发及监控任务
#     spider.start()  # 采集