# 处理文本的基本工具
import re


def strB2Q(ustring,use_num=True):
    """让阿拉伯数字为半角，其余为全角"""
    """use_num为True表示数字不包含在内"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    if not use_num:
        num_Qstr = "１２３４５６７８９０"
        num_Bstr = "1234567890"
        for i in range(10):
            rstring = rstring.replace(num_Qstr[i], num_Bstr[i])
    return rstring

def strQ2B(ustring):
    """把字符串全角转半角"""
    def Q2B(uchar):
        """单个字符 全角转半角"""
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e: #转完之后不是半角字符返回原来的字符
            return uchar
        return chr(inside_code)
    return "".join([Q2B(uchar) for uchar in ustring])


def filter_line(s):
    """
    对一行中文文本过滤，将无效的信息删除
    """
    if s:
        useless_note = " \n"
        for i in useless_note: s = s.replace(i, "")
        if s: return s

def filter_chinese(s):
    """只剩中文字符,但不包含数字"""
    res = re.findall("[\u4e00-\u9fa51234567890]", s)
    if res: return "".join(res)

def get_first_pattern(patterns, s):
    """返回模式列表中第一个匹配的模式，没有返回None"""
    if s:
        for pattern in patterns:
            ret = re.search(pattern, s)
            if ret:
                return ret.group()