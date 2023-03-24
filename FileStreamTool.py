from tqdm import tqdm


from multiprocessing import  Process,Queue,Pool

def multiprocess_data(data,fun,process_num=1):
    """
    fun: 单项处理函数
    data: 列表，处理的数据
    process_num: 进程数量
    return : 有序返回，处理函数为空的情况删除
    """
    def cut_data(data,num):
        """平均将data切分成num个，返回二维列表"""
        new_data=[]
        one_data_len=round(len(data)/num)
        for i in range(num):
            if i==num-1:
                new_data.append(data[i*one_data_len:])
            else:
                new_data.append(data[i*one_data_len:(i+1)*one_data_len])
        return new_data
    
    def process_fun(data,q,bar_q):
        """把空的地方去掉"""
        new_data=[]
        for item in data:
            item=fun(item)
            if item is not None:new_data.append(item)
            bar_q.put(0)
        q.put(new_data)
        
    def pbar_process(bar_q):

        pbar=tqdm(total=len(data))
        while True:
            bar_q.get()
            pbar.update(1)

    bar_q=Queue()
    pbar_p=Process(target=pbar_process,args=(bar_q,))
    pbar_p.start()

    if process_num==1:
        data=[fun(i) for i in data]
        data=[i for i in data if i is not None]
        return data
    
    data=cut_data(data,process_num)
    queues=[]
    processes=[]

    for data_i in data:
        q=Queue()
        p=Process(target=process_fun,args=(data_i,q,bar_q))
        processes.append(p)
        queues.append(q)
        p.start()
    

    new_data=[]
    for i in range(len(processes)):
        new_data+=queues[i].get()
        processes[i].join()
    
    pbar_p.terminate()
    pbar_p.join()
    
    return new_data

def multiprocess_data_pool(data,fun,process_num=1):
    with Pool(processes = process_num) as pool:result = list(tqdm(pool.imap(fun, data), total=len(data)))
    return result

class FileStream:
    """
    目标：文件的统一流处理，一个文件经数据处理后变成另一个文件
    架构：A流到B，对每一个项，采用一个函数进行处理，变成一个新的项

    最好能打印读取和保存信息
    """


    def __init__(self,from_file,to_file,item_fun,process_num=1):
        """
        from_file : 原文件
        to_file : 处理后的文件
        item_fun : 对文件里每一项的处理函数
        """
        self.from_file=from_file
        self.to_file=to_file
        self.item_fun=item_fun
        self.process_num=process_num

    def json_stream(self,list_in_line=True):
        """item不记录返回空"""
        from .JsonTool import load_json,save_json
        data=load_json(self.from_file)

        new_data=multiprocess_data_pool(data,self.item_fun,self.process_num)


        # new_data=[]
        # for item in tqdm(data):
        #     item=self.item_fun(item)
        #     if item:new_data.append(item)
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