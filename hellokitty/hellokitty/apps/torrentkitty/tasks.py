# -*- coding: utf-8 -*-
from celery.task import task
import urllib2
import re
from bs4 import BeautifulSoup
from hellokitty.apps.torrentkitty.models import Rootport

__author__ = 'wangyiyang'


@task
def get_root_port():
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
               'Referer': 'http://www.zhihu.com/articles'}
    print "headers success"
    request = urllib2.Request(url="http://www.torrentkitty.org/search/", headers=headers)
    print "request = urllib2.Request(url='http://www.torrentkitty.org/search/', headers=headers)"
    response = urllib2.urlopen(request)
    print "response = urllib2.urlopen(request)"
    content = response.read()
    print response.read()
    if content:
        print "get success"
        soup = BeautifulSoup(content)
        result = soup.find_all(href=re.compile("/search/"))
        for link in result:
            if not Rootport.objects.filter(link=link.get('href')):
                rp = Rootport()
                rp.link = "http://www.torrentkitty.org{link}".format(link = link.get('href'))
                rp.title = link.string
                rp.save()
    else:
        print "get fail"