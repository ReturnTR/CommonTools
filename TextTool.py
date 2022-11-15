import re
"""
处理文本的基本工具
基本操作类别：
    字符串格式转换
        转换是相互的，有A转B就有B转A
    保留部分字符串
"""


class ConvertInterface:
    """
    字符串转换接口，需要指名A2B是哪一个，一般为最多使用的哪个
    """
    @staticmethod
    def A2B(s): pass
    @staticmethod
    def B2A(s): pass


class GetPartialOnly:

    @staticmethod
    def Chinese(s):
        """中文字符,不包含数字"""
        return re.sub(r'[^\u4e00-\u9fa5]+', '', s)

    @staticmethod
    def ASCII(s):
        """只保留ASCII"""
        return re.sub(r'[^\x00-\x7F]+', '', s)

    @staticmethod
    def English_letters(s):
        """只保留英文字符"""
        return re.sub(r'[^a-zA-z]+', '', s)

    @staticmethod
    def Chinese_and_numbers(s):
        return re.sub(r'[^\u4e00-\u9fa51234567890]+', '', s)

    @staticmethod
    def numbers(s):
        return re.sub(r'[^1234567890]+', '', s)

    @staticmethod
    def English_letter_and_underline(s):
        return re.sub(r'[^a-zA-z_]+', '', s)

    @staticmethod
    def Chinese_and_others(self,s,others):
        """只接受单个字符串"""
        return re.sub(r'[^\u4e00-\u9fa{}]+'.format(others), '', s)


class ConvertB2Q(ConvertInterface):
    """半角转全角"""
    @staticmethod
    def A2B(ustring,use_num=True):
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
    @staticmethod
    def B2A(ustring):
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


class ConvertChineseSimplified(ConvertInterface):
    """
    A2B : 繁体转简体
    """
    def __init__(self):
        from opencc import OpenCC
        self.a=OpenCC("t2s")
        self.b = OpenCC('s2t')
    def A2B(self,s):return self.a.convert(s)
    def B2A(self, s): return self.b.convert(s)


def get_first_pattern(patterns, s):
    """返回模式列表中第一个匹配的模式，没有返回None"""
    if s:
        for pattern in patterns:
            ret = re.search(pattern, s)
            if ret:
                return ret.group()


def del_chars(s,chars=",，、 "):
    """默认去掉停用词"""
    for i in chars:
        s=s.replace(i,"")
    return s



def get_first_envelope_str(s,sep):
    """
    对其依照分隔符进行分层,保存里面还有同样分隔符的情况
    分隔符用'*'分割起来
    从开头开始匹配，找到一个完整的包络情况
    找不到返回None
    正则表达式做不了，只能另写函数
    

    例：
    分隔符：{{*}}  左:'{{'  右:'}}'
    字符串：{{infobox {{USA}}}}{{hehe}}
    返回  ：{{infobox {{USA}}}}


    通常方式是先re一个字符串（{{xx[\s\S]*}}），然后再使用此方法将后面的无用信息去掉

    """
    sep=sep.split("*")
    len_left=len(sep[0])
    len_right=len(sep[1])
    count=0 #记录有多少个层
    flag=False #表示是否找到了标签
    i=0
    while i<len(s):
        if s[i:i+len_left]==sep[0]:
            count+=1
            flag=True
            i+=len_left
        elif s[i:i+len_right]==sep[1]:
            count-=1
            if flag and count==0:
                return s[:i+len_right]
            else:
                i+=len_right
        else:
            i+=1

if __name__=="__main__":
    res=get_first_envelope_str("{{infobox {{USA}}{{hehe}}}}","{{*}}")
    print(res)









