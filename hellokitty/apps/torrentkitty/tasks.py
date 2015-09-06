# -*- coding: utf-8 -*-
import urllib
from celery.task import task
import urllib2
import re
from bs4 import BeautifulSoup
from hellokitty.apps.torrentkitty.models import Rootport, Resources
from hellokitty.common.appconfig import BF_ROOT, BF_RESOURCES

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
        results = soup.find_all(href=re.compile("/search/"))
        for result in results:
            link = result.get('href')
            title = result.string
            bfs = BF_ROOT.add(link)
            if bfs is False:
                Rootport.objects.create(
                    title=title, link="http://www.torrentkitty.org{link}".format(link=link))


@task
def get_resources_and_page():
    for rp in Rootport.objects.select_related("link"):
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
                results = soup.find_all(href=re.compile("magnet"))
                for result in results:
                    link = result.get('href')
                    title = result.get('title')
                    bfr = BF_RESOURCES.add(link)
                    if bfr is False:
                        Resources.objects.create(title=title, link=link)
                keyworld_pages = soup.find_all(href=re.compile("information"))
                get_keyworld(keyworld_pages)
        rp.status = True
        rp.save()


def get_keyworld(keyworld_pages):
    for keyworld_page in keyworld_pages:
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        try:
            request = urllib2.Request(url="http://www.torrentkitty.org{link}".format(link=keyworld_page.get("href")),
                                      headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except:
            pass
        else:
            if content:
                soup = BeautifulSoup(content)
                results = soup.find_all(href=re.compile("/search/"))
                for result in results:
                    print result
                    link = result.get('href')
                    title = result.get('title')
                    bfs = BF_ROOT.add(link)
                    if bfs is False and title is not None:
                        Rootport.objects.create(
                            title=title, link="http://www.torrentkitty.org{link}".format(link=link))


def get_sub_page_resources(link=None, num=None):
    for i in range(1, num + 1):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        try:
            request = urllib2.Request(
                url="{link}{i}".format(link=link, i=i), headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except:
            pass
        else:
            if content:
                soup = BeautifulSoup(urllib.quote(content))
                results = soup.find_all(href=re.compile("magnet"))
                for result in results:
                    sublink = result.get('href')
                    title = result.get('title')
                    bfr = BF_RESOURCES.add(sublink)
                    if bfr is False:
                        Resources.objects.create(title=title, link=sublink)
                keyworld_pages = soup.find_all(href=re.compile("information"))
                get_keyworld(keyworld_pages)
