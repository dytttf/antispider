#coding:utf8
import re
import string
import urllib
import requests
import traceback
from collections import defaultdict

def get_char(js, replace_count):
    all_var = {}
    # 判断混淆 无参数 返回常量 函数
    if_else_no_args_return_constant_function_functions = []
    """
    function zX_() {
            function _z() {
                return '09';
            };
            if (_z() == '09,') {
                return 'zX_';
            } else {
                return _z();
            }
        }
    """
    constant_function_regex4 = re.compile("""
        function\s+\w+\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*else\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*
        \}
        """,
            re.X)
    l = constant_function_regex4.findall(js)
    for i in l:
        function_name = re.search("""
        function\s+(\w+)\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*else\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*
        \}
        """, i,
            re.X)
        if_else_no_args_return_constant_function_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b,c,d = function_name.groups()
        all_var["%s()"%a] = d if b == c else b


    # 判断混淆 无参数 返回函数 常量
    if_else_no_args_return_function_constant_functions = []
    """
    function wu_() {
            function _w() {
                return 'wu_';
            };
            if (_w() == 'wu__') {
                return _w();
            } else {
                return '5%';
            }
        }
    """
    constant_function_regex5 = re.compile("""
        function\s+\w+\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*else\s*\{\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*
        \}
        """,
            re.X)
    l = constant_function_regex5.findall(js)
    for i in l:
        function_name = re.search("""
        function\s+(\w+)\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*else\s*\{\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*
        \}
        """, i,
            re.X)
        if_else_no_args_return_function_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b,c,d = function_name.groups()
        all_var["%s()"%a] = b if b == c else d


    # var 参数等于返回值函数
    var_args_equal_value_functions = []
    """
    var ZA_ = function(ZA__) {
            'return ZA_';
            return ZA__;
        };
    """
    constant_function_regex1 = re.compile("var\s+[^=]+=\s*function\(\w+\)\{\s*[\'\"]return\s*\w+\s*[\'\"];\s*return\s+\w+;\s*\};")
    l = constant_function_regex1.findall(js)
    for i in l:
        function_name = re.search("var\s+([^=]+)", i).group(1)
        var_args_equal_value_functions.append(function_name)
        js = js.replace(i, "")
        # 替换全文
        a = function_name
        js = re.sub("%s\(([^\)]+)\)"%a, r"\1", js)

    # var 无参数 返回常量 函数
    var_no_args_return_constant_functions = []
    """
    var Qh_ = function() {
            'return Qh_';
            return ';';
        };
    """
    constant_function_regex2 = re.compile("""
            var\s+[^=]+=\s*function\(\)\{\s*
                [\'\"]return\s*\w+\s*[\'\"];\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
                \};
            """,
            re.X)
    l = constant_function_regex2.findall(js)
    for i in l:
        function_name = re.search("""
            var\s+([^=]+)=\s*function\(\)\{\s*
                [\'\"]return\s*\w+\s*[\'\"];\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
                \};
            """,
            i,
            re.X)
        var_no_args_return_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b = function_name.groups()
        all_var["%s()"%a] = b

    # 无参数 返回常量 函数
    no_args_return_constant_functions = []
    """
    function ZP_() {
            'return ZP_';
            return 'E';
        }
    """
    constant_function_regex3 = re.compile("""
            function\s*\w+\(\)\s*\{\s*
                [\'\"]return\s*[^\'\"]+[\'\"];\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*
        """,
        re.X)
    l = constant_function_regex3.findall(js)
    for i in l:
        function_name = re.search("""
            function\s*(\w+)\(\)\s*\{\s*
                [\'\"]return\s*[^\'\"]+[\'\"];\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*
        """,
        i,
        re.X)
        no_args_return_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b = function_name.groups()
        all_var["%s()"%a] = b


    # 无参数 返回常量 函数 中间无混淆代码
    no_args_return_constant_sample_functions = []
    """
    function do_() {
            return '';
        }
    """
    constant_function_regex3 = re.compile("""
            function\s*\w+\(\)\s*\{\s*
                return\s*[\'\"][^\'\"]*[\'\"];\s*
            \}\s*
        """,
        re.X)
    l = constant_function_regex3.findall(js)
    for i in l:
        function_name = re.search("""
            function\s*(\w+)\(\)\s*\{\s*
                return\s*[\'\"]([^\'\"]*)[\'\"];\s*
            \}\s*
        """,
        i,
        re.X)
        no_args_return_constant_sample_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b = function_name.groups()
        all_var["%s()"%a] = b

    # 字符串拼接时使无参常量函数
    """
    (function() {
                'return sZ_';
                return '1'
            })()
    """
    constant_function_regex6 = re.compile("""
            \(function\(\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*[\'\"][^\'\"]*[\'\"];?
            \}\)\(\)
        """,
        re.X)
    l = constant_function_regex6.findall(js)
    for i in l:
        function_name = re.search("""
            \(function\(\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*([\'\"][^\'\"]*[\'\"]);?
            \}\)\(\)
        """,
        i,
        re.X)
        js = js.replace(i, function_name.group(1))

    # 字符串拼接时使用返回参数的函数
    """
    (function(iU__) {
                'return iU_';
                return iU__;
            })('9F')
    """
    constant_function_regex6 = re.compile("""
            \(function\(\w+\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*\w+;
            \}\)\([\'\"][^\'\"]*[\'\"]\)
        """,
        re.X)
    
    l = constant_function_regex6.findall(js)
    for i in l:
        function_name = re.search("""
            \(function\(\w+\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*\w+;
            \}\)\(([\'\"][^\'\"]*[\'\"])\)
        """,
        i,
        re.X)
        js = js.replace(i, function_name.group(1))

    # 获取所有变量
    var_regex = "var\s+(\w+)\s*=\s*([\'\"].*?[\'\"]);\s"

    for var_name, var_value in re.findall(var_regex, js):
        var_value = re.sub("\s", "", var_value).strip("\'\" ")
        if "(" in var_value:
            var_value = ";"
        all_var[var_name] = var_value

    # 注释掉 此正则可能会把关键js语句删除掉
    #js = re.sub(var_regex, "", js)

    for var_name, var_value in all_var.items():
        js = js.replace(var_name, var_value)

    js = re.sub("[\s+']", "", js)

    # 寻找%E4%B8%AD%E5%80%92%E 密集区域
    #string_region = re.findall("((?:%\w\w)+)", js)
    string_region = re.findall("((?:%\w\w|[A-Za-z\d])+)", js)
    # 去重
    string_region = set(string_region)
    # 判断是否存在汉字
    chinese_flag = 0
    for string_ in string_region:
        if re.search("%\w\w", string_):
            chinese_flag = 1
    if not chinese_flag:
        # 可能混淆字符为纯英文 。。。尚未解决
        return []
    string_str = ""
    for string_ in string_region:
        if not re.search("%\w\w", string_):
            continue
        # 过滤 
        utf8_string = urllib.unquote(string_)
        if not utf8_string.isalpha():
            # 去掉可能匹配到的多余字符 \w+  建立在混淆字符串是排好序的 字母在汉字前
            utf8_string = utf8_string.rstrip(string.letters + string.digits + "_")
        try:
            unicode_string = utf8_string.decode("utf8")
        except:
            continue
        if len(unicode_string) < replace_count:
            continue
        if len(string_) > len(string_str):
            string_str = string_

    utf8_string = urllib.unquote(string_str)
    if not utf8_string.isalpha():
        # 去掉可能匹配到的多余字符 \w+  建立在混淆字符串是排好序的 字母在汉字前
        utf8_string = utf8_string.rstrip(string.letters + string.digits + "_")

    unicode_string = utf8_string.decode("utf8")

    # 当只有一个替换字符时 下面正则寻找失败 此时也不用寻找了
    if len(unicode_string) == 1:
        return [unicode_string]

    # 从 字符串密集区域后面开始寻找索引区域
    index_m = re.search("([\d,]+(;[\d,]+)+)", js[js.find(string_str) + len(string_str):])

    string_list = list(unicode_string)
    index_list = index_m.group(1).split(";")

    _word_list = []
    for word_index_list in index_list:
        _word = ""
        if "," in word_index_list:
            word_index_list = word_index_list.split(",")
            word_index_list = [int(x) for x in word_index_list]
        else:
            word_index_list = [int(word_index_list)]
        for word_index in word_index_list:
            _word += string_list[word_index]
        _word_list.append(_word)
    return _word_list

def get_complete_text_autohome(text):
    _types_info = defaultdict(list)
    types = re.findall('hs_kw(\d+_[^\'\"]+)', text)
    for item in types:
        idx, type = item.split("_")
        _types_info[type].append(idx)
    # 获取混淆字符个数
    types = {type: len(set(value)) for type, value in _types_info.items()}

    js_list = re.findall("<script>(\(function[\s\S]+?)\(document\);</script>", text.encode("utf8"))
    type_charlist = {}
    for js in js_list:
        for _type in types:
            if _type in js:
                break
        else:
            continue
        if not js:
            continue
        try:
            char_list = get_char(js, types[_type])
        except Exception as e:
            traceback.print_exc()
            continue
        type_charlist.update({_type: char_list})

    def char_replace(m):
        index = int(m.group(1))
        typ = m.group(2)
        char_list = type_charlist.get(typ, [])
        if not char_list:
            return m.group()
        char = char_list[index]
        return char
    text = re.sub("<span\s*class=[\'\"]hs_kw(\d+)_([^\'\"]+)[\'\"]></span>", char_replace, text)
    return text

debug_flag = 1

if 0 or debug_flag:
    # 论坛
    url = "http://club.autohome.com.cn/bbs/thread-c-3788-62403429-1.html"
    url = "http://club.autohome.com.cn/bbs/thread-c-2561-64686945-1.html"
    headers = {"User-Agent": "Mozilla/6.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    resp = requests.get(url, headers=headers)
    text = resp.content.decode("gbk")
    text = get_complete_text_autohome(text)
    data = re.search("<div\s*class=[\'\"]tz-paragraph[^\'\"]*?[\'\"]>([\s\S]+?)</div>", text).group(1)
    if debug_flag:
        if "hs_kw" not in data:
            print("%s ok !!" % url)

if 0 or debug_flag:
    # 口碑
    url = "http://k.autohome.com.cn/spec/27507/view_1524661_1.html?st=2&piap=1|27507|0|0|1|0|0|0|0|0|1"
    headers = {"User-Agent": "Mozilla/6.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    resp = requests.get(url, headers=headers)
    text = resp.content.decode("gbk")
    text = get_complete_text_autohome(text)
    text = re.sub("<style[^>]+?>[\s\S]+?</style>", "", text)
    text = re.sub("<script[^>]?>[\s\S]+?</script>", "", text)
    data = re.search("<div\s*class=[\'\"]text-con[\'\"][^>]*>([\s\S]+?)</div>", text).group(1)
    if debug_flag:
        if "hs_kw" not in data:
            print("%s ok !!" % url)


if 0 or debug_flag:
    # 参数配置
    url = "http://car.autohome.com.cn/config/spec/1001360.html"
    url = "http://car.autohome.com.cn/config/spec/1646.html" # 混淆字符存在英文
    headers = {"User-Agent": "Mozilla/6.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    resp = requests.get(url, headers=headers)
    text = resp.content.decode("gbk")
    text = get_complete_text_autohome(text)
    data = re.search('var config = (.*?);\r', text, re.DOTALL).group(1)
    if debug_flag:
        if "hs_kw" not in data:
            print("%s ok !!" % url)
