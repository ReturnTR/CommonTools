import json
import re
from tqdm import tqdm

"""Json"""


def dumps(data,list_in_line):
    """json 格式转换，有分隔符"""
    def remove_return(matched):
        """去掉换行"""
        s=matched.group()
        return s.replace("\n","").replace("    ","")
    data = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
    if list_in_line:
        data = re.sub(r'\[[^\]\[]*?\]', remove_return, data)
    return data

def save_json(data,filename,list_in_line=True):
    """
    将数据保存在json文件中
    :param:list_in_line 最内部的列表数据以一行表示,不再换行
    """

    data=dumps(data,list_in_line=list_in_line)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def load_json(filename):
    """读取json文件"""
    file = open(filename, 'r', encoding='utf-8')
    data = json.loads(file.read())
    file.close()
    return data

def get_json_indexs(data_file,start,end,des_file=None,is_print=True,list_in_line=False):
    """
    截取json文件中的部分内容
    要求data_file的第一个类型为列表
    """
    data=load_json(data_file)
    data=data[start:end]
    if not isinstance(data,list):raise("json的最外层格式不是list")
    if des_file is not None: save_json(data,des_file)
    if is_print:
        print(dumps(data,list_in_line=list_in_line))
        
def get_infobox_statistics(filename,des_file,infobox_key="infobox"):
    """查看infobox基本信息"""
    from .BasicTool import DictCount
    data=load_json(filename)
    key_count=DictCount()
    for item in data:
        if infobox_key in item:
            for key in item[infobox_key]:
                key_count.add(key)
    key_count=key_count.get()
    all_count=sum(key_count.values())
    temp_count=0
    for item in key_count:
        temp_count+=key_count[item]
        res=[]
        res.append(int(key_count[item]/len(data)*10000)/100)
        res.append(key_count[item])
        res.append(int(temp_count/all_count*10000)/100)
        key_count[item]=res
    save_json(key_count,des_file)

def get_attribute_statistics(filename,des_file,attribute_name):
    """处理特定属性值的信息"""
    from .BasicTool import DictCount
    data=load_json(filename)
    key_count=DictCount()
    for item in data:
        if attribute_name in item:
            key_count.add(item[attribute_name])
    key_count=key_count.get()
    all_count=sum(key_count.values())
    temp_count=0
    for item in key_count:
        temp_count+=key_count[item]
        res=[]
        res.append(int(key_count[item]/len(data)*10000)/100)    # 占总数量百分比
        res.append(key_count[item])                             # 数量
        res.append(int(temp_count/all_count*10000)/100)         # 占所有属性数量百分比
        key_count[item]=res
    save_json(key_count,des_file)


####################
"""
Jsonl模式，相比于json更有读取保存更有优势，支持大文件

节省内存的有：


"""

class JsonlIterator():
    """Jsonl，采用迭代器实现
    
    用法：
    data = JsonlIterator(filename)
    for item in data : process(item)
    
    """
    
    def __init__(self,filename):
        self.f=open(filename,'r',encoding='utf-8')
    
    def __iter__(self):
        return self

    def __next__(self):
        line = self.f.readline()
        if line:
            return json.loads(line)
        else:
            self.f.close()
            raise StopIteration

def head_jsonl(filename,n=5,list_in_line=False):
    """查看jsonl的前几行文件，默认为5行"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        for _ in range(n):
            s=json.loads(f.readline())
            s=dumps(s,list_in_line=list_in_line)
            print(s)
    
            

def save_jsonl(data,filename):
    """
    将数据保存在jsonl文件中
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item,ensure_ascii=False)+"\n") 

def json2jsonl(filename):
    data=load_json(filename)
    save_jsonl(data,filename[:-5]+".jsonl")

def jsonl2json(filename):
    """处理内存占用减少"""
    import os
    data=JsonlIterator(filename)
    with open(filename[:-6]+".json", 'w', encoding='utf-8') as f:
        f.write("[\n")
        for item in data:
            f.write(json.dumps(item,ensure_ascii=False)+",\n")
    # 去掉末尾字符
    with open(filename[:-6]+".json", "rb+") as f:
        f.seek(-2 ,os.SEEK_END)
        f.truncate()
    # 补充完整
    with open(filename[:-6]+".json","a+",encoding='utf-8')as f:
        f.write("\n]")

def load_jsonl(filename):
    """读取json文件"""
    return [item for item in tqdm(JsonlIterator(filename))]

def get_jsonl_indexs(filename,start=0,end=None,des_file=None,is_print=True,list_in_line=False):
    """
    截取jsonl文件中的部分内容，并以json格式导出
    相对于json的优点是不用全部导入，节省内存与时间
    :param
        start:开始索引,从0开始，默认为0
        end: 结束索引，最长为n-1，默认为n-1
        des_file: 保存区间地址，默认不保存
        is_print: 是否对区间进行打印，默认不打印
        is_json:  是否以json作为输出结果，否则是jsonl，默认是json
    注：是否越界不做判断
    
    """
    
    with open(filename, 'r', encoding='utf-8')as f:
        for _ in range(start):next(f, None)

        if end is None:
            data=[json.loads(line) for line in f]
        else:
            data=[json.loads(f.readline()) for _ in range(end-start)]
        
    if des_file is not None: save_json(data,des_file)
    
    data = dumps(data,list_in_line=list_in_line)
    
    if is_print: print(data)

def get_jsonl_num(filename):
    """获取item数量, 如果只想要数量推荐此函数，这样比较快"""
    
    count=0
    with open(filename, 'r', encoding='utf-8')as f:
        for _ in f: count+=1
    print(count)
    return count

def a_jsonl_data(data,filename,batch=False):
    """向文件末尾追加数据
    
    :param
        batch: 是否为批量导入，默认为False
    """

    with open(filename, 'a', encoding='utf-8')as f:
        if batch:
            for item in data: f.write(json.dumps(item,ensure_ascii=False)+"\n")
        else:
            f.write(json.dumps(data,ensure_ascii=False)+"\n")
        
