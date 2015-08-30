# -*- coding: utf-8 -*-
import urllib
from celery.task import task
import urllib2
import re
from bs4 import BeautifulSoup
from hellokitty.apps.torrentkitty.models import Rootport, Resources

__author__ = 'wangyiyang'


@task
def get_root_port():
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
            if not Rootport.objects.filter(link="http://www.torrentkitty.org{link}".format(link=link.get('href'))) :
                Rootport.objects.create(title=link.string, link="http://www.torrentkitty.org{link}".format(link=link.get('href')))


@task
def get_resources_and_page():
    for rp in Rootport.objects.all():
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        try:
            request = urllib2.Request(url=rp.link, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except:
            pass
        else:
            if content:
                soup = BeautifulSoup(content)
                page_num_div = soup.find_all("div", class_="pagination")
                if page_num_div:
                    page_num_div_str = BeautifulSoup(str(page_num_div[0]))
                    page_nums = page_num_div_str.find_all("a")
                    count = int(page_nums[-2].get('href'))
                    rp.page_num = count
                    rp.save()
                    get_sub_page_resources(link=rp.link, num=count)
                result = soup.find_all(href=re.compile("magnet"))
                for link in result:
                    if not len(Resources.objects.filter(link=link.get('href'))) and not len(Resources.objects.filter(title=link.get('title'))):
                        Resources.objects.create(title=link.get('title'), link=link.get('href'))
                keyworld_pages = soup.find_all(href=re.compile("information"))
                get_keyworld(keyworld_pages)


def get_keyworld(keyworld_pages):
    for keyworld_page in keyworld_pages:
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        try:
            request = urllib2.Request(url="http://www.torrentkitty.org{link}".format(link=keyworld_page.get("href")), headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except:
            pass
        else:
            if content:
                soup = BeautifulSoup(content)
                result = soup.find_all(href=re.compile("/search/"))
                for link in result:
                    rlink = "http://www.torrentkitty.org{link}".format(link=link.get('href'))
                    if not Rootport.objects.filter(link=rlink):
                        Rootport.objects.create(title=link.string, link="http://www.torrentkitty.org{link}".format(link=link.get('href')))


def get_sub_page_resources(link=None, num=None):
    for i in range(1, num+1):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        try:
            request = urllib2.Request(url="{link}{i}".format(link=link, i=i), headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except:
            pass
        else:
            if content:
                soup = BeautifulSoup(urllib.quote(content))
                result = soup.find_all(href=re.compile("magnet"))
                for sublink in result:
                    if not len(Resources.objects.filter(link=sublink.get('href'))) and not len(Resources.objects.filter(title=link.get('title'))):
                        Resources.objects.create(title=sublink.get('title'), link=sublink.get('href'))
                keyworld_pages = soup.find_all(href=re.compile("information"))
                get_keyworld(keyworld_pages)
