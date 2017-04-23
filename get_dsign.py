#coding:utf8
import re
def get_dsign(js):  
    #去标签  
    js = re.sub('<[^>]+>', '', js)  
    #去getName  
    js = js.replace("function getName(){var caller=getName.caller;if(caller.name){return caller.name} var str=caller.toString().replace(/[\s]*/g,\"\");var name=str.match(/^function([^\(]+?)\(/);if(name && name[1]){return name[1];} else {return '';}}", "")  
    #处理常量函数  
    constant_function_regex1 = re.compile("\(function\(\)\{'return [^\']+';return '[^\']+'\}\)\(\)")  
    l = constant_function_regex1.findall(js)  
    for i in l:  
        js = js.replace(i, "'%s'"%(re.search("'return [^\']+';return '([^\']+)'", i).group(1)))      
    #  
    constant_function_regex2 = re.compile("function \w+\(\)\{'[^\']+';function [^\']+\(\)\{return '[^\']+'\}; return \w+\(\);\}")  
    l = constant_function_regex2.findall(js)  
    for i in l:  
        a = re.search("function (\w+)\(\)\{'[^\']+';function [^\']+\(\)\{return '([^\']+)'\}; return \w+\(\);\}", i)  
        js = js.replace(i, "%s='%s';"%(a.group(1), a.group(2)))  
    #  
    constant_function_regex3 = re.compile("\w+=function\(\)\{'return \w+';return '[^\']+';\};")  
    l = constant_function_regex3.findall(js)  
    for i in l:  
        a = re.search("(\w+)=function\(\)\{'return \w+';return '([^\']+)';\};", i)  
        js = js.replace(i, "%s='%s';"%(a.group(1), a.group(2)))  
    #  
    constant_function_regex4 = re.compile("\w+=function\(\)\{'\w+';var \w+=function\(\)\{return '[^\']+'\}; return \w+\(\);\};")  
    l = constant_function_regex4.findall(js)  
    for i in l:  
        a = re.search("(\w+)=function\(\)\{'\w+';var \w+=function\(\)\{return '([^\']+)'\}; return \w+\(\);\};", i)  
        js = js.replace(i, "%s='%s';"%(a.group(1), a.group(2)))  
    #  
    constant_function_regex5 = re.compile("((?:function \w+\(\w+\)\{)+function \w+\(\)\{return getName\(\);\}.*?return.*?return.*?\})")  
    l = constant_function_regex5.findall(js)  
    for i in l:  
        a = re.search("^function (\w+)\(\w+\)", i)  
        b = re.search("function (\w+)\(\)\{return getName", i)  
        js = js.replace(i, "%s='%s';"%(a.group(1), b.group(1)))  
    #  
    constant_function_regex6 = re.compile("\(function\([^\)]+\)\{'return [^\']+';return [^\}]+\}\)\('[^\']+'\)")  
    l = constant_function_regex6.findall(js)  
    for i in l:  
        a = re.search("\(function\([^\)]+\)\{'return [^\']+';return [^\}]+\}\)\('([^\']+)'\)", i)  
        js = js.replace(i, "'%s'"%(a.group(1)))  
    #  
    constant_function_regex6 = re.compile("\(function\(\w+\)\{return \(function\(\w+\)\{return \w+;\}\)\(\w+\);\}\)\('[^\']+'\)")  
    l = constant_function_regex6.findall(js)  
    for i in l:  
        a = re.search("\(function\(\w+\)\{return \(function\(\w+\)\{return \w+;\}\)\(\w+\);\}\)\('([^\']+)'\)", i)  
        js = js.replace(i, "'%s'"%(a.group(1)))  
    #  
    constant_function_regex7 = re.compile("\(function\(\)\{'return [^\']+';return \(function\(\)\{return '[^\']+';\}\)\(\);\}\)\(\)")  
    l = constant_function_regex7.findall(js)  
    for i in l:  
        a = re.search("\(function\(\)\{'return [^\']+';return \(function\(\)\{return '([^\']+)';\}\)\(\);\}\)\(\)", i)  
        js = js.replace(i, "'%s'"%(a.group(1)))  
    #  
    constant_function_regex9 = re.compile("\w+=function\(\w+\)\{var \w+=function\(\w+\)\{'return \w+';return \w+;\}; return \w+\(\w+\);\};")  
    l = constant_function_regex9.findall(js)  
    for i in l:  
        a = re.search("(\w+)=function\(\w+\)\{var \w+=function\(\w+\)\{'return \w+';return \w+;\}; return \w+\(\w+\);\};", i)  
        js = js.replace(i, "%s='*';"%(a.group(1)))  
    #  
    constant_function_regex8 = re.compile("\w+=function\(\w+\)\{'return \w+';return \w+;\};")  
    l = constant_function_regex8.findall(js)  
    for i in l:  
        a = re.search("(\w+)=function\(\w+\)\{'return \w+';return \w+;\};", i)  
        js = js.replace(i, "%s='*';"%(a.group(1)))  
    #  
    constant_function_regex9 = re.compile("function \w+\(\)\{'return \w+';return '[^\']+'\}")  
    l = constant_function_regex9.findall(js)  
    for i in l:  
        a = re.search("function (\w+)\(\)\{'return \w+';return '([^\']+)'\}", i)  
        js = js.replace(i, "%s='%s';"%(a.group(1), a.group(2)))  
    #  
    js = re.sub('\s*=\s*', '=', js)  
    #变量处理  
    var_regex = re.compile("(\w+='[^\']+')")  
    var_list = var_regex.findall(js)  
    t_var_list = []  
      
    for var in var_list:  
        i = var.find('=')  
        k,v = var[0:i], var[i+1:]  
        t_var_list.append((k,v))  

    t_var_list.sort(key=lambda x:len(x[0]))  
    t_var_list.reverse()  

    for k,v in t_var_list:  
        if v == "'*'":  
            js = re.sub("%s\(('[^\']+')\)?"%k, "\\1", js)  
        else:  
            js = re.sub('%s\(\'[^\']+\'\)'%k, v, js)  
            js = re.sub('%s\(\)'%k, v, js)  
            js = re.sub('%s'%k, v, js)  

    js = ''.join([x for x in js.split(';') if '+' in x])  
    #js = re.sub("\([^\)]+\)", "", js)  
    js = re.sub("'\+[^\']*'", "", js)  

    _dsign = re.findall('ign=([a-z\d]+)', js)
    if _dsign:
        _dsign = _dsign[-1]
    else:
        _dsign = ''
    return _dsign

with open('_dsign.js') as f:
    js = f.read()

print get_dsign(js)
