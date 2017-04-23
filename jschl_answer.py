#coding:utf8
import re
import time
import urlparse

url = 'http://hwsqnews.com/index.html'

js_template = '''
<!DOCTYPE HTML>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1" />
  <meta name="robots" content="noindex, nofollow" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
  <title>安全检查中...</title>
  <style type="text/css">
    html, body {width: 100%; height: 100%; margin: 0; padding: 0;}
    body {background-color: #ffffff; font-family: Helvetica, Arial, sans-serif; font-size: 100%;}
    h1 {font-size: 1.5em; color: #404040; text-align: center;}
    p {font-size: 1em; color: #404040; text-align: center; margin: 10px 0 0 0;}
    #spinner {margin: 0 auto 30px auto; display: block;}
    .attribution {margin-top: 20px;}
  </style>

    <script type="text/javascript">
  //<![CDATA[
  (function(){
    var a = function() {try{return !!window.addEventListener} catch(e) {return !1} },
    b = function(b, c) {a() ? document.addEventListener("DOMContentLoaded", b, c) : document.attachEvent
("onreadystatechange", b)};
    b(function(){
      var a = document.getElementById('yjs-content');a.style.display = 'block';
      setTimeout(function(){
        var s,t,o,p,b,r,e,a,k,i,n,g,f, JoXcllR={"zEEyJVSsCWzZ":+((+!![]+[])+(+[]))};
        t = document.createElement('div');
        t.innerHTML="<a href='/'>x</a>";
        t = t.firstChild.href;r = t.match(/https?:\/\//)[0];
        t = t.substr(r.length); t = t.substr(0,t.length-1);
        a = document.getElementById('jschl-answer');
        f = document.getElementById('challenge-form');
        ;JoXcllR.zEEyJVSsCWzZ-=+!![];JoXcllR.zEEyJVSsCWzZ+=+((!+[]+!![]+!![]+!![]+[])+(!+[]+!![]+!![
]+!![]+!![]+!![]));a.value = parseInt(JoXcllR.zEEyJVSsCWzZ, 10) + t.length; '; 121'
        f.submit();
      }, 4000);
    }, false);
  })();
  //]]>
</script>


</head>
<body>
  <table width="100%" height="100%" cellpadding="20">
    <tr>
      <td align="center" valign="middle">
          <div class="yjs-browser-verification yjs-im-under-attack">
  <noscript><h1 data-translate="turn_on_js" style="color:#bd2426;">请打开浏览器的javascript，然后刷新浏览器</h1></noscript
>
  <div id="yjs-content" style="display:none">
    <div>
      <div class="bubbles"></div>
      <div class="bubbles"></div>
      <div class="bubbles"></div>
    </div>
    <h1>hwsqnews.com <span data-translate="checking_browser">浏览器安全检查中...</span></h1>
    <p data-translate="process_is_automatic"></p>
    <p data-translate="allow_5_secs">还剩 5 秒&hellip;</p>
  </div>
  <form id="challenge-form" action="/cdn-cgi/l/chk_jschl" method="get">
    <input type="hidden" name="jschl_vc" value="80a5a308fe3eb3a3ea510b681d6c0e50"/>
    <input type="hidden" name="pass" value="1478443220.375-qUH6DBM2Eo"/>
    <input type="hidden" id="jschl-answer" name="jschl_answer"/>
  </form>
</div>


          <div class="attribution"><a href="http://su.baidu.com/" target="_blank" style="font-size: 12px
;"></a></div>
      </td>
    </tr>
  </table>
</body>
</html>
'''

def get_answer(js, url):
    # js规则转换
    # !+[] == 1
    # !![] == 1
    # [] == '0'

    js_convert_dict = [
        (re.compile('\!\+\[\]'),'1'),
        (re.compile('\!\!\[\]'),'1'),
        (re.compile('\[\]'),'0'),
        ]

    # 计算代码规律 有 +()![] 组成
    cal_pattern = '[\+\(\)\!\[\]]+'

    js = re.sub('\s*', '', js)

    # 寻找变量名
    obj = re.search('var(?:\w,)+(?P<obj_name>\w+)\=\{\"(?P<obj_attr>\w+)\"\:(?P<obj_value>%s)\};'%cal_pattern, js)
    #print obj.groupdict()

    # 替换掉 替换掉对象名和属性名为 answer
    js = js.replace(obj.group('obj_name') + '.' + obj.group('obj_attr'), 'answer')

    # 寻找计算代码
    new_cal_pattern = re.compile('answer([\*\+\-]\=%s)'%cal_pattern)
    cal_list = new_cal_pattern.findall(js)

    # 加入初值
    cal_list = [obj.group('obj_value')] + cal_list

    # 对计算代码进行化简 使用 js_convert_dict
    def convert(cal_str):
        for pattern,repl in js_convert_dict:
            cal_str = re.sub(pattern, repl, cal_str)
        return cal_str
        
    cal_list = [convert(x) for x in cal_list]

    # 转换后一般为一下两种格式
    # *=+1     这种可替换掉第一个 + 号后 使用 eval 直接执行
    # +=+((1+1+0)+(1+1+1+1+1+1+1+1+1))  这种需要先计算前后两个括号中的数字 然后使用字符串加法，再使用 eval 执行
    # 类型分辨 使用 算式最后一位是否为 0 来区分

    # 先替换掉 = 号后的 + 号
    cal_list = [x.replace('=+', '=') for x in cal_list]

    # 第二次化简
    def convert_2(cal_str):
        # 寻找子算式
        sub_cal_list = re.findall('(\([\+\d]+\))', cal_str)
        #
        for sub_cal in sub_cal_list:
            if '0)' in sub_cal:
                cal_str = cal_str.replace(sub_cal, '"' + str(eval(sub_cal)) + '"')
            else:
                cal_str = cal_str.replace(sub_cal, str(eval(sub_cal)))
        # 化简 将存在字符串类型的按照字符串相加
        # 由于仅出现了 字符串 + 数字类型的 所以我就不考虑 数字 + 数字 + 字符串 等更复杂的情况了
        if '"' in cal_str:
            cal_str = cal_str.replace('"+', '')
            cal_str = cal_str.replace('"', '')
        return cal_str
    cal_list = [convert_2(x) for x in cal_list]

    # 开始 计算
    scope = {}
    for cal_str in cal_list:
        if '=' not in cal_str:
            cal_str = "=" + cal_str
        cal_str = 'answer' + cal_str
        exec(cal_str, scope)

    answer = scope['answer']


    # js代码中还增加了一个 t.length 其实就是当前页面的url的域名部分的长度 hwsqnews.com
    answer += len(urlparse.urlparse(url).netloc)
    return answer

def get_direct_url(html, answer):
    u'''从js页面获取跳转需要的参数'''
    jschl_vc = re.search('name="jschl_vc"\s*value="([^\"]+)"', html).group(1)
    pass_str = re.search('name="pass"\s*value="([^\"]+)"', html).group(1)
    direct_url = 'http://hwsqnews.com/cdn-cgi/l/chk_jschl?jschl_vc=%s&pass=%s&jschl_answer=%s'%(
           jschl_vc,  pass_str, answer
        )
    return direct_url


def test():
    import requests
    cookie = ''
    # 最好把头部写全
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        'Cookie':cookie,
        "Host":urlparse.urlparse(url).netloc,
        "Referer":url,
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf8'
    print re.search('<title>([^<]+)', resp.text, re.I).group(1)
    print u'首次访问返回 %s'%resp
    cookie += '__cfduid=%s；'%resp.cookies['__cfduid']
    answer = get_answer(resp.content, url)
    direct_url = get_direct_url(resp.content, answer)
    print u"跳转 url: %s"%direct_url
    headers.update({
        "Cookie":cookie,
        "Referer":url,
        })
    # 这很重要 必须等待 4 秒以上
    print u'等待 5 秒...'
    time.sleep(5)
    #
    print u'开始访问跳转页面'
    direct_resp = requests.get(direct_url, headers=headers)
    # 此处直接跳转到 正常页面
    # 打印跳转历史
    print u'跳转历史: %s'%direct_resp.history
    # 跳转后 返回码
    print u'跳转结束后回到正常页面: %s, url: %s'%(direct_resp, direct_resp.url)
    direct_resp.encoding = 'gbk'
    print re.search('<title>([^<]+)', direct_resp.text, re.I).group(1)
    return direct_resp
    

if __name__ == "__main__":
    test()
    #print get_answer(js_template, url)
