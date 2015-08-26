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
            if not Rootport.objects.filter(link="http://www.torrentkitty.org{link}".format(
                    link=link.get('href'))) and "http://www.torrentkitty.org{link}".format(
                link=link.get('href')) not in rp_list:
                rp_list.append(Rootport(
                    title=link.string, link="http://www.torrentkitty.org{link}".format(link=link.get('href'))))
        Rootport.objects.bulk_create(rp_list)


@task
def get_resources_and_page():
    for rp in Rootport.objects.all():
        cr_list = []
        resources_list = []
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
                count = int(page_nums[-2].get('href'))
                rp.pagenum = count
                rp.save()
                get_sub_page_resources(rp.link, count)
            result = soup.find_all(href=re.compile("magnet"))
            for link in result:
                if not len(Resources.objects.filter(link=link.get('href'))) and link.get(
                        'href') not in cr_list and not len(Resources.objects.filter(title=link.get('title'))):
                    resources_list.append(Resources(title=link.get('title'), link=link.get('href')))
                    cr_list.append(link.get('href'))
            Resources.objects.bulk_create(resources_list)
            keyworld_pages = soup.find_all(href=re.compile("information"))
            get_keyworld(keyworld_pages)


def get_keyworld(keyworld_pages):
    for keyworld_page in keyworld_pages:
        rp_list = []
        ck_list = []
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        request = urllib2.Request(url="http://www.torrentkitty.org%s" % keyworld_page.get("href"), headers=headers)
        response = urllib2.urlopen(request)
        content = response.read()
        if content:
            soup = BeautifulSoup(content)
            result = soup.find_all(href=re.compile("/search/"))
            for link in result:
                rlink = "http://www.torrentkitty.org{link}".format(link=link.get('href'))
                if not Rootport.objects.filter(link=rlink) and rlink not in ck_list and link.get('title'):
                    rp_list.append(Rootport(title=link.get('title'), link=rlink))
                    ck_list.append(rlink)
            Rootport.objects.bulk_create(rp_list)


def get_sub_page_resources(link, num):
    for i in range(1, num):
        cr_list = []
        resources_list = []
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        request = urllib2.Request(url="%s%s" % (link, i), headers=headers)
        response = urllib2.urlopen(request)
        content = response.read()
        if content:
            soup = BeautifulSoup(content)
            result = soup.find_all(href=re.compile("magnet"))
            for link in result:
                if not len(Resources.objects.filter(link=link.get('href'))) and link.get(
                        'href') not in cr_list and not len(Resources.objects.filter(title=link.get('title'))):
                    resources_list.append(Resources(title=link.get('title'), link=link.get('href')))
                    cr_list.append(link.get('href'))
            Resources.objects.bulk_create(resources_list)
            keyworld_pages = soup.find_all(href=re.compile("information"))
            get_keyworld(keyworld_pages)
