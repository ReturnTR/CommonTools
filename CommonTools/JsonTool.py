import json

def save_json(data,filename):
    """将数据保存在json文件中"""
    data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
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