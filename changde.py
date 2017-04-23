#coding:utf8
import re
import requests

def everySystem(number, system):
    '''
    实现数字向任意进制的转换
    base = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '''
    base = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = base[:system]
    chars = []
    while 1:
        number, mod = divmod(number, system)
        if number < system:
            chars.append(base[mod])
            chars.append(base[number])
            break
        else:
            chars.append(base[mod])
    chars.reverse()
    chars = [str(x) for x in chars]
    return "".join(chars)

def packed(p, a, c, k, e, d):
    def e(c):
        c_1 = ''
        if c >= a:
            c_1 = e(int(c / a))
        c = c % a
        c_2 = chr(c+32) if c > 32 else everySystem(c, 33)
        return c_1.lstrip('0') + c_2.lstrip('0')

    k += [0] * 1000
    while c > 0:
        d[e(c)] = k[c] or e(c)
        c -= 1
    def kk(e):
        return d.get(e.group(), "")
    p = re.sub("\\b\\w+\\b", kk, p)
    return p

#wzwschallenge="RANDOMSTR9819";
#wzwschallengex="STRRANDOM9819";
#template=3;
#encoderchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

def KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU(s, encoderchars):
    le = len(s)
    i = 0
    out = ''
    while i < le:
        c1 = ord(s[i]) & 0xff
        i += 1
        if i == le:
            out += encoderchars[c1 >> 2]
            out += encoderchars[(c1 & 0x3) << 4]
            out += "=="
            break
        c2 = ord(s[i])
        i += 1
        if i == le:
            out += encoderchars[c1>>2]
            out += encoderchars[((c1 & 0x3) << 4) | ((c2 & 0xf0) >> 4)]
            out += encoderchars[(c2 & 0xf) << 2]
            out += "="
            break
        c3 = ord(s[i])
        i += 1
        out += encoderchars[c1 >> 2]
        out += encoderchars[((c1 & 0x3) << 4) | ((c2 & 0xf0) >> 4)]
        out += encoderchars[((c2 & 0xf) << 2) | ((c3 & 0xc0) >> 6)]
        out += encoderchars[c3 & 0x3f]
    return out

def QWERTASDFGXYSF(wzwschallenge, wzwschallengex, hc, CONFIRM_PREFIX):
    tmp = wzwschallenge + wzwschallengex
    hash = 0
    for i in range(len(tmp)):
        hash += ord(tmp[i])
    hash *= hc
    hash += 111111
    return CONFIRM_PREFIX + str(hash)

def HXXTTKKLLPPP5(wzwschallenge, wzwschallengex, template, encoderchars, hc, CONFIRM_PREFIX):
    cookieString = ""
    cookieString += "wzwstemplate=" + KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU(str(template), encoderchars) + ";";
    confirm = QWERTASDFGXYSF(wzwschallenge, wzwschallengex, hc, CONFIRM_PREFIX)
    cookieString += "wzwschallenge=" + KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU(str(confirm), encoderchars) + ";";
    return cookieString


def parse_script(text):
    m = re.search("p\}\(\'(?P<p>[^\']+)\',(?P<a>\d+),(?P<c>\d+),\'(?P<k>[^\']+)\'\.split\(\'\|'\)", text)
    if not m:
        print u"解析js失败"
        return ""
    p = m.group('p')
    a = int(m.group('a'))
    c = int(m.group('c'))
    k = m.group('k').split('|')
    e = 0
    d = {}
    eval_p = packed(p,a,c,k,e,d)
    #eval_p = 'var dynamicurl="/";var wzwschallenge="RANDOMSTR2556";var wzwschallengex="STRRANDOM2556";var template=8;var encoderchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";function KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU() {var out, i, len;var c1, c2, c3;len = .length;i = ;out = "";while (i < len) {c1 = .charCodeAt(i++) & 0xff;if (i == len) {out += encoderchars.charAt(c1 >> 2);out += encoderchars.charAt((c1 & 0x3) << 4);out += "==";break;}c2 = .charCodeAt(i++);if (i == len) {out += encoderchars.charAt(c1 >> 2);out += encoderchars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xf0) >> 4));out += encoderchars.charAt((c2 & 0xf) << 2);out += "=";break;}c3 = .charCodeAt(i++);out += encoderchars.charAt(c1 >> 2);out += encoderchars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xf0) >> 4));out += encoderchars.charAt(((c2 & 0xf) << 2) | ((c3 & 0xc0) >> 6));out += encoderchars.charAt(c3 & 0x3f);}return out;}function findDimensions(){var w= window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth;var h= window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight;if (w*h <= 120000) {return true;}var x = window.screenX;var y = window.screenY;if (x + w <=  || y + h <=  || x >= window.screen.width || y >= window.screen.height) {return true;}return false;}function QWERTASDFGXYSF(){var tmp = wzwschallenge+wzwschallengex;var hash = ;var i = ;for(i = ; i < tmp.length; i++) {hash += tmp.charCodeAt(i);}hash *= 23;hash += 111111;return "WZWS_CONFIRM_PREFIX_LABEL8"+hash;}function HXXTTKKLLPPP5(){if(findDimensions()) {} else {var cookieString = "";    cookieString = "wzwstemplate="+KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU(template.toString()) + "; path=/";document.cookie = cookieString;    var confirm = QWERTASDFGXYSF();cookieString = "wzwschallenge="+KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU(confirm.toString()) + "; path=/";document.cookie = cookieString;    window.location=dynamicurl;}}HXXTTKKLLPPP5();'
    #print eval_p
    wzwschallenge = re.search("wzwschallenge=[\'\"]([^\'\"]+)", eval_p).group(1)
    wzwschallengex = re.search("wzwschallengex=[\'\"]([^\'\"]+)", eval_p).group(1)
    template = re.search("=(\d+);var encoderchar", eval_p).group(1)
    encoderchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    hc = int(re.search("hash \*= (\d+)", eval_p).group(1))
    CONFIRM_PREFIX = re.search("(WZWS_CONFIRM_PREFIX_LABEL\d+)", eval_p).group(1)
    #print wzwschallenge, wzwschallengex, template, encoderchars, hc, CONFIRM_PREFIX

    cookie = HXXTTKKLLPPP5(wzwschallenge, wzwschallengex, template, encoderchars, hc, CONFIRM_PREFIX)
    return cookie

def main():
    url = 'http://bbs.changde.gov.cn/'
    resp = requests.get(url)
    text = resp.text
    print text
    cookie = parse_script(text)
    cookie += "wzwsconfirm=%s;"%resp.cookies.get("wzwsconfirm")
    #print cookie
    resp = requests.get(url, headers={"Cookie":cookie})
    print resp.text
    #print resp.cookies
    #print resp.headers
    #"V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDUxMzYwNDU="
    return 


if __name__ == "__main__":
    p = '''15 D="k";15 1a="i";15 1b="l";15 11=d;15 F = "e+/=";J g(10) {15 U, N, R;15 o, p, q;R = 10.S;N = 0;U = "";17 (N < R) {o = 10.s(N++) & 6;O (N == R) {U += F.r(o >> a);U += F.r((o & 1) << b);U += "==";n;}p = 10.s(N++);O (N == R) {U += F.r(o >> a);U += F.r(((o & 1) << b) | ((p & 5) >> b));U += F.r((p & 4) << a);U += "=";n;}q = 10.s(N++);U += F.r(o >> a);U += F.r(((o & 1) << b) | ((p &5) >> b));U += F.r(((p & 4) << a) | ((q & 3) >> c));U += F.r(q & 2);}W U;}J H(){15 16= 19.Q||B.C.u||B.m.u;15 K= 19.P||B.C.t||B.m.t;O (16*K <= 8) {W 14;}15 1d = 19.Y;15 1e = 19.Z;O (1d + 16 <= 0 || 1e+ K <= 0 || 1d >= 19.X.18 || 1e >= 19.X.M) {W 14;}W G;}J h(){15 12 = 1a+1b;15 L = 0;15 N    = 0;I(N= 0; N < 12.S; N++) {L += 12.s(N);}L *= 9;L += 7;W "j"+L;}J f(){O(H()) {} E {15 A = "";    A = "1c="+g(11.13()) + "; V=/";B.w = A;    15 v = h();A = "1a="+g(v.13()) + "; V=/";B.w = A;    19.T=D;}}f();'''
    a = 59
    c = 74
    k = '''0|0x3|0x3f|0xc0|0xf|0xf0|0xff|111111|120000|19|2|4|6|7|ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|HXXTTKKLLPPP5|KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU|QWERTASDFGXYSF|RANDOMSTR870|WZWS_CONFIRM_PREFIX_LABEL7|/|STRRANDOM870|body|break|c1|c2|c3|charAt|charCodeAt|clientHeight|clientWidth|confirm|cookie|cookieString|document|documentElement|dynamicurl|else|encoderchars|false|findDimensions|for|function|h|hash|height|i|if|innerHeight|innerWidth|len|length|location|out|path|return|screen|screenX|screenY|str|template|tmp|toString|true|var|w|while|width|window|wzwschallenge|wzwschallengex|wzwstemplate|x|y'''.split('|')
    e = 0
    d = {}
    #print packed(p,a,c,k,e,d)
    #print KTKY2RBD9NHPBCIHV9ZMEQQDARSLVFDU('3')
    #print HXXTTKKLLPPP5()
    main()
    #print QWERTASDFGXYSF("RANDOMSTR6093", "STRRANDOM6093", 29)
