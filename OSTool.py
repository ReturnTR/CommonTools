import os

def get_files_list():
    """获取当前目录下的所有文件"""
    path = os.getcwd()
    all_files = [f for f in os.listdir(path)]
    return all_files