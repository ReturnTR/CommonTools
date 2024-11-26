# coding=utf-8
# Time : 2022/10/12 22:52
# Description : pandas 的一些操作，包括csv与excel的数据读取

import pandas as pd



def df2list(df):
    return df.values.tolist()
    

def data2df(data,columns=None,index=None):
    """将数据格式转换为dataframe
    :param
        columns: 每列的名称，注意一定与列数相等
        index: 每行的名称，注意与行数相等
        data: 支持各种数据，包括：
        二维列表：[[],[]]
        字典列表：[{},{}]，            每一项字典的键必须一样，键作为每一列的名称，即columns
        列表字典：{key1:[],key2:[]}    DataFrame的默认方式，key代表每一列所有值，要求每一列数量都一样
        二维字典：{key_index_1:{key_columns_1:item,key_columns_2:item},key_index_2:{key_columns_1:item,key_columns_2:item}}   第一层键表示行，第二层键表示列，注意每一个列必须一样
    
    注：pandas对中文排版在打印时有问题，因此dict中的key尽量用英文
    """
    
    if isinstance(data, list):
        if isinstance(data[0],dict):
            new_data = []
            columns = list(data[0].keys())
            for item in data:
                new_data.append([item[key] for key in item])
            data = new_data
        else:pass
    elif isinstance(data[0],dict):
        index=list(data.keys())
        columns=list(data[index[0]].keys())
        data=[[data[key1][key2] for key2 in columns] for key1 in index]
    else:
        return pd.DataFrame(data, index=index)
        
                 
    return pd.DataFrame(data, columns=columns,index=index)
    

def load_df(filename,sep="\t",sheet_name="Sheet1"):
    """加载数据，转化为dataframe格式
    支持csv和excel
    """
    if filename[-4:]=="xlsx":
        df=pd.read_excel(filename,sheet_name=sheet_name)
    elif filename[-3:]=="csv":
        df=pd.read_csv(filename,sep=sep,nrows=None)
    else:
        print("无法找到已有格式文件："+filename)
    return df


def save_df(df,filename,sep="\t",sheet_name="Sheet1"):
    
    if filename[-4:]=="xlsx":
        # 多个表的存储
        if isinstance(df,list):
            with pd.ExcelWriter(filename) as writer:
                for i in range(len(df)):
                    temp_sheet_name = 'Sheet'+str(i) if sheet_name == "Sheet1" else sheet_name[i]
                    df[i].to_excel(writer, sheet_name=temp_sheet_name)  

        else: df.to_excel(filename, index=False,sheet_name=sheet_name)
    elif filename[-3:]=="csv":
        df.to_csv(filename, index=False,sep=sep)
    else:
        print("无法找到已有格式文件："+filename)
    
    
if __name__ == "__main__":

    print("hello")
