# 快速读取/保存文件

import pickle


def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def save_pickle(data,filename):
    with open(filename,'wb') as f:
        pickle.dump(data,f)