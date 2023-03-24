from tqdm import tqdm


from multiprocessing import Pool




class FileStream:
    """
    目标：文件的统一流处理，一个文件经数据处理后变成另一个文件
    架构：A流到B，对每一个项，采用一个函数进行处理，变成一个新的项

    最好能打印读取和保存信息
    """
    @staticmethod
    def multiprocess_data(data,fun,process_num):
        """使用多进程加速数据处理"""
        with Pool(processes = process_num) as pool:result = list(tqdm(pool.imap(fun, data), total=len(data)))
        return result

    def __init__(self,from_file,to_file,item_fun,num_workers=1):
        """
        from_file : 原文件
        to_file : 处理后的文件
        item_fun : 对文件里每一项的处理函数
        num_workers : 进程数量，默认单进程
        """
        self.from_file=from_file
        self.to_file=to_file
        self.item_fun=item_fun
        self.num_workers=num_workers

    def json_stream(self,list_in_line=True):
        """item不记录返回空"""
        from .JsonTool import load_json,save_json
        data=load_json(self.from_file)

        if self.num_workers==1:
            new_data=[]
            for item in tqdm(data):
                item=self.item_fun(item)
                if item:new_data.append(item)
        else:
            new_data=self.multiprocess_data(data,self.item_fun,self.num_workers)
            new_data=[i for i in new_data if i is not None]

        print(len(new_data))
        save_json(new_data,self.to_file,list_in_line=list_in_line)

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