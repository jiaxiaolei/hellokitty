import urllib2
from sgmllib import SGMLParser
import re
from bs4 import BeautifulSoup

# for rp in Rootport.objects.all():
cp_list = []
rp_list = []
cr_list = []
resources_list = []
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
           'Referer': 'http://www.zhihu.com/articles'}
request = urllib2.Request(url="http://www.torrentkitty.org/search/ipz 166/", headers=headers)
response = urllib2.urlopen(request)
content = response.read()
if content:
    soup = BeautifulSoup(content)
    page_num_div = soup.find_all("div", class_="pagination")
    if page_num_div:
        page_num_div_str = BeautifulSoup(str(page_num_div[0]))
        page_nums = page_num_div_str.find_all("a")
        count = int(page_nums[-2].get('href'))
        print count
            # for page_num in range(1, count):
            #     if not Rootport.objects.filter(link="{link}{page}".format(link="http://www.torrentkitty.org/search/ipz 166/", page=page_num)) and "{link}{page}".format(link="http://www.torrentkitty.org/search/ipz 166/", page=page_num) not in cp_list:
            #         rp_list.append(Rootport(
            #             title=rp.title, link="{link}{page}".format(link="http://www.torrentkitty.org/search/ipz 166/", page=page_num)))
            #         cp_list.append("{link}{page}".format(link="http://www.torrentkitty.org/search/ipz 166/", page=page_num))
            # Rootport.objects.bulk_create(rp_list)