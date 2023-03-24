import os

def get_files_list():
    """获取当前目录下的所有文件"""
    path = os.getcwd()
    all_files = [f for f in os.listdir(path)]
    return all_files


def mkdir(path):
    """
    如果不存在则创建目录
    存在则打印信息
    """
    # 去除首位空格，去除尾部 \ 符号
    path=path.strip().rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path) # 创建目录操作函数
    else:
        print(path+' 目录已存在')