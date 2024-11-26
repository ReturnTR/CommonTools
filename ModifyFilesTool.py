
"""
实现Python脚本自动化对文件的指定位置插入文本
支持多文件插入
具体插入方法查看yaml文件

运行方式：python3 ModifyFilesTool.py modify_files_tool.yaml

后续添加功能：
    1. 最好能有撤回的操作，这样比较清晰，而且撤回操作最好能够自动生成
    2. 删除文本功能
"""


import os  
import yaml
def insert_text_at_line(file_path, line_number, text_to_insert,encoding='utf-8'):  
    """
    line_number: 行号，1为第一行，-1为最后一行
    """
    # 检查文件是否存在  
    if not os.path.exists(file_path):  
        raise FileNotFoundError(f"The file {file_path} does not exist.")  
      
    # 读取文件内容  
    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:  
        lines = file.readlines()  
      
    # 处理负数行号，将其转换为正数行号  
    line_number = len(lines) + line_number + 1 if line_number < 0 else line_number - 1
      
    # 检查行号是否在有效范围内  
    if not (0 <= line_number <= len(lines)):  
        raise IndexError(f"The line number {line_number} is out of range for the file {file_path}.")  
      
    # 在指定位置插入文本  
    lines.insert(line_number, text_to_insert + '\n')  
      
    # 将修改后的内容写回文件  
    with open(file_path, 'w', encoding=encoding, errors='ignore') as file:  
        file.writelines(lines)  
  


def insert_by_yaml(yaml_path,encoding='gbk'):  
    """配置文件修改
    
    插入多行怎么办，这时行数会往下移，但是我又不想让他往下移，所以就只能按照排序大小进行偏移
    """

    with open(yaml_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        basepath = config["basepath"]

    for item in config["file_operation"]:

        if "content" in item:
            if os.path.exists(basepath+item["file"]):
                print("file already exists：",basepath+item["file"])
            else:
                with open(basepath+item["file"], 'w', encoding=encoding) as f:
                    content = "\n".join(item['content']) if isinstance(item["content"], list) else item['content']
                    f.write(content)
            print("file:{} insert success!".format(item["file"]))
        else:
            item["operations"].sort(key=lambda x: x["line"])
            add_line=0
            for operation in item["operations"]:         
                text = "\n".join(operation['text']) if isinstance(operation["text"], list) else operation['text']
                insert_text_at_line(basepath+item["file"], operation["line"]+add_line, text,encoding=encoding)
                add_line += len(operation['text']) if isinstance(operation["text"], list) else 1

            print("file:{} insert success!".format(item["file"]))


if __name__=="__main__":

    # yaml_path = "modify_files_tool.yaml"
    # insert_by_yaml(yaml_path)

    import sys
    if len(sys.argv) > 1:
        yaml_path = sys.argv[1]
        insert_by_yaml(yaml_path)


  

