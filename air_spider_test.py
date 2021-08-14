# -*- coding: utf-8 -*-
"""
Created on 2021-08-13 19:33:05
---------
@summary:
---------
@author: lanba
"""

import feapder
import json


class AirSpiderTest(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://www.etsy.com/listing/674434128/natural-wild-flowers-laptop-skin-macbook", render=True)#, render=True

    def parse(self, request, response):
        bs=response.bs4()
        jdata=json.loads(bs.find("script",{"type":"application/ld+json"}).string)
        category =jdata.get("category")
        print(category )


if __name__ == "__main__":
    AirSpiderTest().start()