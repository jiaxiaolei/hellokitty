import urllib2
from sgmllib import SGMLParser
import re
from bs4 import BeautifulSoup

headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  ,
                        'Referer':'http://www.zhihu.com/articles' }
print "headers success"   
request = urllib2.Request(url = "http://www.torrentkitty.org/search/",headers = headers)
response = urllib2.urlopen(request)
content =  response.read()
print "get success"
soup = BeautifulSoup(content)
result = soup.find_all(href=re.compile("/search/"))
# result = found.find_all("a")
for link in result:
	print link.get('href')



