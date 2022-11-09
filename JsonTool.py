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


def format_change(filename):
    """
    对特定json文件格式进行修改
    """
    pass


def get_infobox_statistics(filename,des_file,infobox_key="infobox"):
    from .BasicTool import DictCount
    data=load_json(filename)
    key_count=DictCount()
    for item in data:
        if infobox_key in item:
            for key in item[infobox_key]:
                key_count.add(key)
    key_count=key_count.get()

    for item in key_count:
        key_count[item]=str(int(key_count[item]/len(data)*10000)/100)+"%"+"("+str(key_count[item])+")"
    save_json(key_count,des_file)

