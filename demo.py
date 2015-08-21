import urllib2
from sgmllib import SGMLParser
import re
from bs4 import BeautifulSoup

headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  ,
                        'Referer':'http://www.zhihu.com/articles' }   
request = urllib2.Request(url = "http://macshuo.com/",headers = headers)
response = urllib2.urlopen(request)
content =  response.read()

soup = BeautifulSoup(content,"html5lib")
found = BeautifulSoup(str(soup.find_all(id="archives-2")[0]))
result = found.find_all("a")
for link in result:
	print "a"
	print link.get('href')

