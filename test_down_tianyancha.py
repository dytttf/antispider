#coding:utf-8
import os
import re
import time
import zlib
import random
import urllib
import urllib2
import cookielib
import json
import requests

sogou = ["6", "b", "t", "f", "l", "5", "w", "h", "q", "i", "s", "e", "c", "p", "m", "u", "9", "8", "y", "2", "z", "k", "j", "r", "x", "n", "-", "0", "3", "4", "d", "1", "a", "o", "7", "v", "g"]
v= '33,102,117,110,99,116,105,111,110,40,110,41,123,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,61,39,116,111,107,101,110,61,97,57,51,98,98,56,50,50,57,101,57,50,52,55,102,49,57,56,48,97,98,54,100,97,52,55,101,54,55,55,101,55,59,112,97,116,104,61,47,59,39,59,110,46,119,116,102,61,102,117,110,99,116,105,111,110,40,41,123,114,101,116,117,114,110,39,51,44,50,57,44,49,44,51,49,44,48,44,49,50,44,48,44,49,55,44,51,48,44,48,44,49,57,44,50,55,44,50,57,44,49,55,44,49,54,44,53,44,49,54,44,49,55,44,50,55,44,53,44,51,44,51,50,44,51,48,44,51,44,50,55,44,49,44,49,54,44,51,52,44,50,55,44,51,52,44,53,44,49,50,39,125,125,40,119,105,110,100,111,119,41,59'
s = ''.join([chr(int(x)) for x in v.split(',')])
utm = re.search("return'([\d,]+)", s).group(1)
utm = "".join([sogou[int(x)] for x in utm.split(',')])

def get_token(data, company_id): 
    sogou_list = [
            ["6", "b", "t", "f", "l", "5", "w", "h", "q", "i", "s", "e", "c", "p", "m", "u", "9", "8", "y", "2", "z", "k", "j", "r", "x", "n", "-", "0", "3", "4", "d", "1", "a", "o", "7", "v", "g"],
            ["1", "8", "o", "s", "z", "m", "b", "9", "f", "d", "7", "h", "c", "u", "n", "v", "p", "y", "2", "0", "3", "j", "-", "i", "l", "k", "t", "q", "4", "6", "r", "a", "w", "5", "e", "x", "g"],
            ["g", "a", "c", "t", "h", "u", "p", "f", "6", "x", "7", "0", "d", "i", "v", "e", "q", "4", "b", "5", "k", "w", "9", "s", "-", "j", "l", "y", "3", "o", "n", "z", "m", "2", "1", "r", "8"],
            ["s", "6", "h", "0", "y", "l", "d", "x", "e", "a", "k", "z", "u", "f", "4", "r", "b", "-", "p", "g", "3", "n", "m", "7", "o", "c", "i", "8", "v", "2", "1", "9", "q", "w", "t", "j", "5"],
            ["d", "4", "9", "m", "o", "i", "5", "k", "q", "n", "c", "s", "6", "b", "j", "y", "x", "l", "a", "v", "3", "t", "u", "h", "-", "r", "z", "2", "0", "7", "g", "p", "8", "f", "1", "w", "e"],
            ["z", "5", "g", "c", "h", "7", "o", "t", "2", "k", "a", "-", "e", "x", "y", "j", "3", "l", "1", "u", "s", "4", "b", "n", "8", "i", "6", "q", "p", "0", "d", "r", "v", "m", "w", "f", "9"],
            ["p", "x", "3", "d", "6", "5", "8", "k", "t", "l", "z", "b", "4", "n", "r", "v", "y", "m", "g", "a", "0", "1", "c", "9", "-", "2", "7", "q", "j", "h", "e", "w", "u", "s", "f", "o", "i"],
            ["q", "-", "u", "d", "k", "7", "t", "z", "4", "8", "x", "f", "v", "w", "p", "2", "e", "9", "o", "m", "5", "g", "1", "j", "i", "n", "6", "3", "r", "l", "b", "h", "y", "c", "a", "s", "0"],
            ["7", "-", "g", "x", "6", "5", "n", "u", "q", "z", "w", "t", "m", "0", "h", "o", "y", "p", "i", "f", "k", "s", "9", "l", "r", "1", "2", "v", "4", "e", "8", "c", "b", "a", "d", "j", "3"],
            ["1", "t", "8", "z", "o", "f", "l", "5", "2", "y", "q", "9", "p", "g", "r", "x", "e", "s", "d", "4", "n", "b", "u", "a", "m", "c", "h", "j", "3", "v", "i", "0", "-", "w", "7", "k", "6"]
        ]
    sogou = sogou_list[int(str(ord(str(company_id).decode('utf8')[0]))[1])]
    #print sogou
    v = data.get('data', {}).get('v')
    s = ''.join([chr(int(x)) for x in v.split(',')])
    #print s
    token = re.search("token=([^;]+)", s).group(1)
    utm = re.search("return'([\d,]+)", s).group(1)
    utm = "".join([sogou[int(x)] for x in utm.split(',')])
    #print token, ' ', utm
    return token, utm

company_id = "25696030"
proxies = {"http":"http://175.150.25.50:808"}
proxies = None
ts = time.time()
LOGINURL = 'http://www.tianyancha.com/tongji/%s.json?random=%s'%(company_id, int(ts * 1000))
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Host":"www.tianyancha.com",
        "Connection":"keep-alive",
        "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"application/json, text/plain, */*",
        "Cache-Control":"no-cache",
        "Tyc-From":"normal",
        "CheckError":"check",
        }


session = requests.Session()
resp1 = session.get(LOGINURL, headers=headers)
token, utm = get_token(resp1.json(), company_id)
print session.cookies
TYCID = session.cookies.get('TYCID')
tnet = session.cookies.get('tnet')
time.sleep(2)
cookie = 'token=%s; _utm=%s; TYCID=%s; tnet=%s;'%(token, utm, TYCID, tnet)


headers.update({
    "Cookie":cookie,
    "Referer":"http://www.tianyancha.com/company/%s"%company_id,
    })

resp = session.get('http://www.tianyancha.com/company/%s.json'%company_id,
                   headers=headers, proxies=proxies)

print resp
print resp.headers
print resp.history
print session.cookies
print resp.json().get("data").get("baseInfo").get("name")
