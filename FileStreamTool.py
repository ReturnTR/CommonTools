from tqdm import tqdm

class FileStream:
    """
    目标：文件的统一流处理，一个文件经数据处理后变成另一个文件
    架构：A流到B，对每一个项，采用一个函数进行处理，变成一个新的项
    """
    @staticmethod
    def json_stream(from_file,to_file,item_fun):
        """item不记录返回空"""
        from .JsonTool import load_json,save_json
        data=load_json(from_file)
        new_data=[]
        for item in tqdm(data):
            item=item_fun(item)
            if item:new_data.append(item)
        save_json(new_data,to_file)

    @staticmethod
    def json_stream_key(from_file,to_file,attribute,attribute_fun):
        """
        每一个item是一个字典
        在字典的特定属性中改变属性值
        """
        from .JsonTool import load_json, save_json
        data=load_json(from_file)
        new_data=[]
        for item in tqdm(data):
            if attribute in item:item[attribute]=attribute_fun(item[attribute])
            new_data.append(item)
        save_json(data,to_file)