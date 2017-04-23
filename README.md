# antispider
## 记录一下碰到过的反爬虫措施和解决办法，欢迎交流!!!
### 第二级目录无限制
- [http://www.sdstc.gov.cn/1/1000008990.htm](http://www.sdstc.gov.cn/1/1000008990.htm)

***

### 首次访问会出现js中间页跳转 估计是验证ip
- [http://www.qzfz.gov.cn/fzyw/index.html](http://www.qzfz.gov.cn/fzyw/index.html)

***

### 页面加载时间特长
- [http://www.hnprec.com/list.jsp?channelid=148](http://www.hnprec.com/list.jsp?channelid=148)    3分钟

***
### discuz论坛板块接口
- [http://bbs.rednet.cn/forum.php?mod=ajax&action=forumjump&jfid=undefined&inajax=1&ajaxtarget=fjump_menu](http://bbs.rednet.cn/forum.php?mod=ajax&action=forumjump&jfid=undefined&inajax=1&ajaxtarget=fjump_menu)

***
### 需要验证referer
- [http://www.mxwz.com/pingyi/wlhyr/py_list.aspx?type=ly](http://www.mxwz.com/pingyi/wlhyr/py_list.aspx?type=ly)
- [http://www.mxwz.com/pingyi/py_view.aspx?ID=491892](http://www.mxwz.com/pingyi/py_view.aspx?ID=491892)
***
### js跳转 [changde.py](https://github.com/duanyifei/antispider/blob/master/changde.py)
- [http://bbs.changde.gov.cn/](http://bbs.changde.gov.cn/)

***
### cookie加密验证天眼查  [test_down_tianyancha.py](https://github.com/duanyifei/antispider/blob/master/test_down_tianyancha.py)
- [http://tianyancha.com/company/3976673](http://tianyancha.com/company/3976673)
- [http://tianyancha.com/tongji/3976673.json?random=1470990214043](http://tianyancha.com/tongji/3976673.json?random=1470990214043)
- [http://tianyancha.com/company/3976673.json](http://tianyancha.com/company/3976673.json)

***
### 逗比验证码+%99验证失败
http://xygs.gsaic.gov.cn/gsxygs/pub!list.do

***
### 豆瓣FM及其他豆瓣网站 https 不严密的cookie参数 [test_down_douban.py](https://github.com/duanyifei/antispider/blob/master/test_down_douban.py)
- [https://douban.fm/](https://douban.fm/)
- [https://douban.fm/j/explore/genre?gid=%s&start=0&limit=1000](https://douban.fm/j/explore/genre?gid=%s&start=0&limit=1000)
- [http://douban.fm/j/explore/channel_detail?channel_id=9](http://douban.fm/j/explore/channel_detail?channel_id=9)

### js执行后url增加_dsign参数  [get_dsign.py](https://github.com/duanyifei/antispider/blob/master/get_dsign.py)
- [http://bbs.auto.ifeng.com/thread-2758815-1-1.html](http://bbs.auto.ifeng.com/thread-2758815-1-1.html)
- [http://wj.scdaily.scol.com.cn/thread-1754575-1-1.html](http://wj.scdaily.scol.com.cn/thread-1754575-1-1.html)
-js代码 

### 访问显示安全检查中... 5秒后经过js跳转到正常页面
- [http://hwsqnews.com/index.html](http://hwsqnews.com/index.html)
- js代码见 [jschl_answer.html](https://github.com/duanyifei/antispider/blob/master/jschl_answer.html)
- 破解代码见 [jschl_answer.py](https://github.com/duanyifei/antispider/blob/master/jschl_answer.py)

### 文字使用css样式代替
- [http://club.autohome.com.cn/bbs/thread-a-100024-62404423-1.html](http://club.autohome.com.cn/bbs/thread-a-100024-62404423-1.html)
- js代码见 [autohome.js](https://github.com/duanyifei/antispider/blob/master/autohome.js)
- 破解代码 见[autohome.py](https://github.com/duanyifei/antispider/blob/master/autohome.py)
