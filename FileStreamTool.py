from tqdm import tqdm

class FileStream:
    """
    目标：文件的统一流处理，一个文件经数据处理后变成另一个文件
    架构：A流到B，对每一个项，采用一个函数进行处理，变成一个新的项

    最好能打印读取和保存信息
    """


    def __init__(self,from_file,to_file,item_fun):
        """
        from_file : 原文件
        to_file : 处理后的文件
        item_fun : 对文件里每一项的处理函数
        """
        self.from_file=from_file
        self.to_file=to_file
        self.item_fun=item_fun

    def json_stream(self):
        """item不记录返回空"""
        from .JsonTool import load_json,save_json
        data=load_json(self.from_file)
        new_data=[]
        for item in tqdm(data):
            item=self.item_fun(item)
            if item:new_data.append(item)
        save_json(new_data,self.to_file)

    def json_stream_key(self,attribute):
        """
        每一个item是一个字典
        在字典的特定属性中改变属性值
        """
        from .JsonTool import load_json, save_json
        data=load_json(self.from_file)
        new_data=[]
        for item in tqdm(data):
            if attribute in item:item[attribute]=self.attribute_fun(item[attribute])
            new_data.append(item)
        save_json(data,self.to_file)