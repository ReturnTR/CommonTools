# 实现多进程运行重复代码
from multiprocessing import  Process,Queue,Pipe,Pool
from tqdm import tqdm
import time

# 通信方式：管道、消息队列
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


def process_fun_bar(data,fun,process_num=0):
    """
    fun: 目标函数
    data: 列表，处理的数据
    process_num: 进程数量
    """

    pbar=tqdm(total=len(data))

    def process_fun(data,q):
        for i in data:
            i=fun(i)
            if i is not None:q.put(i)


    if process_num==0:process_num=len(data)
    data=cut_data(data,process_num)
    processes=[]
    q=Queue()
    for data_i in data:
        p=Process(target=process_fun,args=(data_i,q))
        processes.append(p)
        p.start()
    
    new_data=[]
    while True:
        new_data.append(q.get())
        print(new_data)
        pbar.update(1)
    # res=[]
    # for i in range(len(processes)):
    #     res+=queues[i].get()
    #     processes[i].join()
    



    
    
    
    return res

def process_fun_pool(data,fun,process_num=0):


    # def process_fun(item,q):
    #     q.put()


    # pool = Pool(processes = process_num)
    # for item in data:
    #     pool.apply_async(fun, (item,))
    # pool.close()
    # pool.join()

    # pool.imap 返回迭代器
    """
    pool = Pool()
    iter = pool.imap(func, iter)，ret表示结果
    # 无论下面执不执行，上面都会开始
    for ret in iter:
        # do something
    pool.close()
    
    """

    with Pool(processes = process_num) as pool:result = list(tqdm(pool.imap(fun, data), total=len(data)))
    return result

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
    # 进度条速度不匹配

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


def fun(data):
    time.sleep(0.2)
    return data+1
if __name__=="__main__":
    data=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    res=process_fun_pool(data,fun,process_num=5)
    print(res)





"""
心路历程：

写出来了无敌
开始想用tqdm
用管道，pbar保存在主进程，但是管道传递消息时需要等待，需要建立n个等待消息队列，这不可能实现
用队列，pbar保存在主进程，采用主进程传递队列，判断is_alive时会有僵尸进程
用队列，pbar保存在子进程，子进程无法采用is_alive来判断
用队列，pbar保存在子进程，同时在人物全部结束时终止pbar进程，该方法能运行，但是由于自称之间的速度导致pbar速度不一样，没有效果
用线程池，不知道怎么做
参考教程，会做了


"""