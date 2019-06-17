# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from collections import defaultdict
import redis
from scrapy.exceptions import NotConfigured


class RandomProxyDownloadMiddleware(object):
    def __init__(self, proxies):
        self.proxies = proxies
        self.max_failed = 3
        self.stats = defaultdict(int)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        proxies = crawler.settings.get('PROXIES')
        if not proxies:
            raise NotConfigured
        return cls(proxies)

    def process_request(self, request, spider):
        if 'proxy' not in request.meta:
            request.meta['proxy'] = random.choice(self.proxies)
            spider.logger.info('use proxy %s ' % request.meta['proxy'])

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        cur_proxy = request.meta['proxy']
        spider.logger.warn('proxy %s occur error %s' % (cur_proxy, exception))
        del request.meta['proxy']
        self.stats[cur_proxy] += 1
        if self.stats[cur_proxy] >= self.max_failed:
            self.remove_proxy(cur_proxy, spider)
        return request

    def remove_proxy(self, cur_proxy, spider):
        if cur_proxy in self.proxies:
            self.proxies.remove(cur_proxy)
            spider.logger.warn('remove proxy %s from proxies list' % cur_proxy)


class RedisProxyDownloadMiddleware(object):
    def __init__(self, proxies):
        self.r = redis.Redis(host="www.chenzhuangzhuang.club",port=6379,password='chen1999')
        self.max_failed = 3

    @property
    def proxies(self):
        return [p.decode('utf-8') for p in self.r.lrange('proxies', 0, -1)]

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        proxies = crawler.settings.get('PROXIES')
        if not proxies:
            raise NotConfigured
        return cls(proxies)

    def process_request(self, request, spider):
        if 'proxy' not in request.meta:
            request.meta['proxy'] = random.choice(self.proxies)
            spider.logger.info('use proxy %s ' % request.meta['proxy'])

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        cur_proxy = request.meta['proxy']
        spider.logger.warn('proxy %s occur error %s' % (cur_proxy, exception))
        del request.meta['proxy']
        self.r.hincrby('stats', cur_proxy, 1)
        if self.get_stats(cur_proxy) >= self.max_failed:
            self.remove_proxy(cur_proxy, spider)
        return request

    def remove_proxy(self, cur_proxy, spider):
        if cur_proxy in self.proxies:
            self.r.lrem('proxies', 1, cur_proxy)
            self.r.lpush('proxies_trash', cur_proxy)
            spider.logger.warn('remove proxy %s from proxies list' % cur_proxy)

    def get_stats(self, proxy):
        num = self.r.hget('stats', proxy)
        if not num:
            return 0
        return int(num)
