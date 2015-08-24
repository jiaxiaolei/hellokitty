# -*- coding: utf-8 -*-
from celery.task import task
import urllib2
import re
from bs4 import BeautifulSoup
from hellokitty.apps.torrentkitty.models import Rootport, Resources

__author__ = 'wangyiyang'


@task
def get_root_port():
    rp_list = []
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
               'Referer': 'http://www.zhihu.com/articles'}
    request = urllib2.Request(
        url="http://www.torrentkitty.org/search/", headers=headers)
    response = urllib2.urlopen(request)
    content = response.read()
    if content:
        soup = BeautifulSoup(content)
        result = soup.find_all(href=re.compile("/search/"))
        for link in result:
            if not Rootport.objects.filter(link=link.get('href')):
                rp_list.append(Rootport(
                    title=link.string, link="http://www.torrentkitty.org{link}".format(link=link.get('href'))))
        Rootport.objects.bulk_create(rp_list)


@task
def get_resources_and_page():
    rp_list = []
    resources_list = []
    for rp in Rootport.objects.all():
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        request = urllib2.Request(url=rp.link, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read()
        if content:
            soup = BeautifulSoup(content)
            page_num_div = soup.find_all("div", class_="pagination")
            if page_num_div:
                page_num_div_str = BeautifulSoup(str(page_num_div[0]))
                page_nums = page_num_div_str.find_all("a")
                count =  int(page_nums[-2].get('href'))
                for page_num in range(count):
                    if not Rootport.objects.filter(link="{link}{page}".format(link=rp.link, page=page_num)):
                        rp_list.append(Rootport(
                            title=rp.title, link="{link}{page}".format(link=rp.link, page=page_num)))
                Rootport.objects.bulk_create(rp_list)
            result = soup.find_all(href=re.compile("magnet"))
            print result
            for link in result:
                if not Resources.objects.filter(link=link.get('href')):
                    resources_list.append(
                        Resources(title=link.get('title'), link=link.get('href')))
            Resources.objects.bulk_create(resources_list)
