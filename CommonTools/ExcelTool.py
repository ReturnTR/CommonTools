import pandas as pd


def data2excel(data, des_file, columns=[]):
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