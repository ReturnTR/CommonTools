import re
from tqdm import tqdm
from .BasicTool import DictCount
from .JsonTool import load_json,save_json


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
    
    @staticmethod
    def get_bihuan(s,note):
        """
        获取第一个闭环字符串
        从第一个字符开始计算
        建议先用正则表达式，否则可能出bug
        例：
            s="(sasd(sad)(dsada))dqda"
            note=["(",")"]
            return "(sasd(sad)(dsada))"
        """
        start=0
        flag=0
        bihuan=0
        i=0
        while i<len(s):
            if s[i:i+len(note[0])]==note[0]:
                if flag==0:
                    flag=1
                    start=i
                bihuan+=1
                i+=len(note[0])
            elif s[i:i+len(note[1])]==note[1]:
                bihuan-=1
                i+=len(note[1])
            else:
                i+=1
            if bihuan==0 and flag==1:
                return s[start:i]
        return ""


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


def get_pattern_info(pattern,content,is_file=True):
    """获取正则表达式结果

    :param
        is_file: content是否为文件，若是读取conent全部内容
    :return
        list
    
    """
    if is_file:
        f=open(content,'r',encoding='utf-8')
        data=f.read()
        f.close()
    else:
        data=content
    
    pattern=re.findall(pattern,data)
    print(len(pattern))
    return pattern




def get_words_distribution(sentences,save_filename,segmentation_tool="jieba"):
    """获取词语的分布
    
    :param
        sentences: 句子列表

    首先需要分词，因此需要选择分词工具
    
    """
    if segmentation_tool=="jieba":
        from .JiebaTool import cut
        
    words_count=DictCount()

    for sentence in tqdm(sentences):
        for word in cut(sentence):words_count.add(word)
        
    save_json(words_count.get(),save_filename)




def summary_evaluation(data,save_filename,stop_words_filename="CommonTools/stop_words/hlt_stopwords.json",):
    """简写评测方法

    以短句为中心，即用（，｜。）分割

    对每个句子建立指标：
        中心思想：分割，然后看分割的单元在不在里面
        分割方式：
            n-gram
            分词方式
        对于一些词不需要分析，即停用词

    :param
        data: 字典列表，字典包含两个键，content表示原文内容，summaries表示总结列表
        stop_words_filename: 停用词表文件，json格式   
    
    :return
        各种指标，包括：
        每句的存在率
        data里每个item存在率
    """

    from .JiebaTool import cut
    # from .DrawTool import Draw
    stop_words=set(load_json(stop_words_filename))

    def get_seg_rate(sentences,content):
        """分词指标
        先对句子分词，然后看里面的存在率
        """
        summary_rate=(0,0)
        for sentence in sentences:
            sentence_list=cut(sentence)
            sentence_list=[i for i in sentence_list if i not in stop_words]    # 去掉停用词    
            exist_sentence_list=[i for i in sentence_list if i in content]
            summary_rate = tuple(x + y for x, y in zip(summary_rate, (len(exist_sentence_list),len(sentence_list))))
        return summary_rate
    

    res=[]

    for item in tqdm(data):
        item_res=[]
        whole_small_sen_num=0
        whole_seg_rate=(0,0)
        for sentence in item["summaries"]:
            # 切分成短句
            small_sentences= re.split(",|，|。",sentence)
            # 短句数量作为指标的分母
            small_sentence_num=len(small_sentences)
            
            # 短句的总结率作为分子，总结率以(分子，分母)的形式给出，便于累积计算

            # 分词
            seg_rate=get_seg_rate(small_sentences,item["content"])

            # 1-gram

            # 2-gram

            # 3—gram
            
            # 求和并记录
            whole_small_sen_num+=small_sentence_num
            whole_seg_rate = tuple(x + y for x, y in zip(whole_seg_rate, seg_rate))
            item_res.append(["small_sen_num",small_sentence_num,"seg_rate",seg_rate[0],seg_rate[1]])
        item_res.append(["whole_small_sen_num",whole_small_sen_num,"whole_seg_rate",whole_seg_rate[0],whole_seg_rate[1]])
        res.append(item_res)


    
    save_json(res,save_filename,list_in_line=True)
    
    # draw=Draw()
    # draw.configure()
    # draw.distribution_bar([i[-1][-2]/i[-1][-1] for i in res])


if __name__=="__main__":
    res=get_first_envelope_str("{{infobox {{USA}}{{hehe}}}}","{{*}}")
    print(res)
    









