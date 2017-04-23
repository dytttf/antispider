#coding:utf-8
import os
import re
import time
import random
import json
import requests

def get_cookie():
    import string
    import random
    import time
    base = string.letters + string.digits + "_"
    bid = "".join(random.sample(base, 11))
    cookie = 'bid=%s; ac="%s"'%(bid, int(time.time()))
    return cookie

proxies = {"http":"http://175.151.205.202:808"}
LOGINURL = 'http://www.pss-system.gov.cn/sipopublicsearch/search/executeGeneralSearch-returnResultOnly.shtml'
LOGINURL = 'https://www.douban.com/location/world/'
#assert 1==2
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Cookie":get_cookie(),
        "Host":"douban.com",
        "Connection":"keep-alive",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cache-Control":"max-age=0",
        #"Cache-Control":"max-age=0",
        #"X-Forward-For":"222.130.132.163",
        }


session = requests.Session()
resp = session.get(LOGINURL, headers=headers)
print resp.headers
print resp
print session.cookies
resp.encoding = 'utf8'
text = resp.text

if re.search("window\.location\.href=\"https", text):
    url = re.search("window\.location\.href=\"([^;]+);", text).group(1)
    print url
    url = url.replace('"+d+"', 'navigator.platform|navigator.userAgent|navigator.vendor')
#print text
print len(text)

with open("aaa.html",'w') as f:
    f.write(text.encode('utf8'))

print resp.url
