import json
import re
def save_json(data,filename,list_in_line=True):
    """
    将数据保存在json文件中
    :param:list_in_line 列表数据以一行表示,不再换行，注：只将最内部的列表变成一行
    """

    def remove_return(matched):
        """去掉换行"""
        s=matched.group()
        return s.replace("\n","").replace("    ","")

    data = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
    if list_in_line:
        data = re.sub(r'\[[^\]\[]*?\]', remove_return, data)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def save_json_list_in_line(data,filename):
    """将数据保存在json文件中"""

    def _remove_return(matched):
        """去掉换行"""
        s=matched.group()
        return s.replace("\n","")
    import re
    data = json.dumps(data, sort_keys=False, indent=0, separators=(',', ': '), ensure_ascii=False)
    data=re.sub(r'\[[^\]\[]*?\]',_remove_return,data)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def load_json(filename):
    """读取json文件"""
    file = open(filename, 'r', encoding='utf-8')
    data = json.loads(file.read())
    file.close()
    return data

def get_json_index(data_file,des_file,start,end):
    """
    截取json文件中的部分内容
    要求data_file的第一个类型为列表
    """
    data=load_json(data_file)
    if not isinstance(data,list):raise("json的最外层格式不是list")
    save_json(data[start:end],des_file)

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

def get_json_num(filename):
    """获取item数量"""
    print(len(load_json(filename)))

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
Jsonl模式，相比于json更有读取优势
"""


def json2jsonl(filename):
    data=load_json(filename)
    save_jsonl(data,filename[:-5]+".jsonl")


def jsonl2json(filename,list_in_line="True"):
    data=load_jsonl(filename)
    save_json(data,filename[:-6]+".json")


def save_jsonl(data,filename,list_in_line=True):
    """
    将数据保存在json文件中
    :param:list_in_line 列表数据以一行表示,不再换行，注：只将最内部的列表变成一行
    """

    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(data)+"\n")

def load_jsonl(filename):
    """读取json文件"""
    f = open(filename, 'r', encoding='utf-8')
    data=[]
    for line in f: data.append(json.loads(line))
    f.close()
    return data

def get_jsonl_index(data_file,start,end,des_file=None,is_print=True,is_json=True):
    """
    截取jsonl文件中的部分内容
    :param
        start:开始索引
        end: 结束索引
        des_file: 保存区间地址，默认不保存
        is_print: 是否对区间进行打印，默认不打印
        is_json:  是否以json作为输出结果，否则是jsonl，默认是json
    注：是否越界不做判断
    
    """
    f = open(filename, 'r', encoding='utf-8')
    for _ in range(start):f.readline()
    data=[]
    for _ in range(end-start):data.append(f.readline())
    if is_json:
        data = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        if is_print:
            print(data)
        if des_file is not None:
            save_json(data,des_file)
    else:
        if des_file is not None:
            save_jsonl(data,des_file)
        if is_print:
            print("\n".join(data))

def get_jsonl_num(filename):
    """获取item数量"""
    f = open(filename, 'r', encoding='utf-8')
    count=0
    for line in f: count+=1
    print(count)
    return count


def a_jsonl_data(data,filename,batch=False):
    """向文件末尾追加数据
    
    :param
        batch: 是否为批量导入，默认为False
    """

    f = open(filename, 'a', encoding='utf-8')

    if batch:
        for item in data:
            f.write(json.dumps(item,ensure_ascii=False)+"\n")
    else:
        f.write(json.dumps(data,ensure_ascii=False)+"\n")

    f.close()



####################

"""
txt2json
"""
def txt2json(filename,save_filename):
    """按行转换，最后生成json列表的形式"""
    with open(filename,'r',encoding='utf-8')as f:
        save_json(f.readlines(),save_filename)
