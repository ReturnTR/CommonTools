import pandas as pd
import numpy as np

def save_excel(data, des_file, columns=[]):
    """
    将数据有格式的保存在excel中
    默认格式为二维列表（最终都要转化成二维列表）
    """

    # list转dataframe

    if isinstance(data, dict):
        """
        二维字典
        要求字典的键格式必须一样
        """
        new_data = []
        columns = list(data[list(data.keys())[0]].keys())
        for key, value in data.items():
            item = [key]
            for key2 in columns:
                item.append(value[key2])
            new_data.append(item)
            data = new_data

    df = pd.DataFrame(data, columns=columns)
    df.to_excel(des_file, index=False)

def load_excel(filename,sheet_name="Sheet1"):
    data=pd.read_excel(filename,sheet_name=sheet_name).values
    for i in range(len(data)):
        for j in range(len(data[i])):
            if isinstance(data[i][j],float):
                if np.isnan(data[i][j]):data[i][j]=None
    return data


class Tool:
    def __init__(self,filename,sheet):
        # 不加sheet默认打开第一个sheet
        self.data= pd.read_excel(filename,sheet_name=sheet)
        print(self.data.values)
    def get_info(self):
        return self.data.values
    def get_columns(self,index1=0,index2=0):pass




