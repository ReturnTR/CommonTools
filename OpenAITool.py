# coding=utf-8
import os
import time
import traceback
from tqdm import tqdm
from multiprocessing import Pool

import openai
openai.api_key = 'xxx'
openai.api_base = "xxx"

from CommonTools.JsonTool import *



def get_create_from_prompt(prompt):
    """调用ChatGPT代码，尝试五次失败后退出"""

    count = 0
    while True:
        count += 1
        try:
            if count > 5:
                break
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "user", "content": prompt},
                ]
            )
            time.sleep(5) # qps 太快会抱错
            result = response['choices'][0]['message']['content']
            return result
        except:
            print('error, trace=' + traceback.format_exc())


def get_prompt_fun(data):
    """Prompt生成方法，需要在data给出保存文件地址，这样可以并行操作
    """
    save_file,prompt=data
    res=get_create_from_prompt(prompt)
    a_jsonl_data({"prompt":prompt,"generation":res},save_file)  # 直接在文件中追加
    time.sleep(5)  


def multiprocess_data(data,fun,process_num):
    """使用多进程加速数据处理"""
    with Pool(processes = process_num) as pool:result = list(tqdm(pool.imap(fun, data), total=len(data)))
    return result


def ChatGPT_multiprocess(filename,save_dir,process_num=6,start_index=0):

    """并行处理ChatGPT命令,结果保存在多个文件中，以jsonl形式保存
    
    :param
        filename: prompt文件，格式为prompt列表
        save_dir: 保存生成结果的文件目录，会创建n*process_num个文件，用来并行保存
        process_num: 进程个数
        start_index: prompt列表开始数量，由于调用时会卡住，因此需要重新运行，之前的prompt不用在生成了
    """
    
    # 设置文件保存倍数，越大越不容易发生冲突
    times=2   

    # 创建文件夹，并在里面生成 process_num*times 个内容为[]的json文件，序列为0 —— process_num*times-1
    os.makedirs(save_dir, exist_ok=True)
    for i in range(process_num*times):open(save_dir+"/result_"+str(i)+".jsonl", 'w',encoding='utf-8').close()


    # 为Prompt标注保存文件，从1到process_num*2，用元组方式扩展
    data=load_json(filename)
    data=[(save_dir+"/result_"+str(i%(process_num*times))+".jsonl",data[i]) for i in range(len(data))]

    # 执行，可以选择data的开始数量
    multiprocess_data(data[start_index:],get_prompt_fun,process_num)


def sum_gpt_results(save_dirs,output_filename,file_num=12):
    """汇总GPT生成结果
    
    :param
        save_dirs: 文件夹列表，每一项对应ChatGPT_multiprocess中的save_dir参数
        output_filename: 保存的目标地址
        file_num: 每个文件夹中的文件数量，对应ChatGPT_multiprocess中的process_num*2
    
    """
    data=[]

    for save_dir in save_dirs:
        if os.path.exists(save_dir):
            for i in range(file_num):
                temp_file=save_dir+"/result_"+str(i)+".json"
                if os.path.exists(temp_file):
                    data+=load_json(temp_file)
                elif os.path.exists(temp_file+"l"):
                    data+=load_jsonl(temp_file+"l")
    save_json(data,output_filename)


def get_last_item_of_whole_file(generation_dir,prompt_file):
    """由于生成多个文件，因此不知道哪一个是最后一项，因此需要找对应Prompt文件中的最后一项，防止重新启动找不到断点
    
    :param
        generation_dir: 对应ChatGPT_multiprocess中的save_dir
        prompt_file: 对应ChatGPT中的prompt filename
    
    """
    last_items=[]
    for filename in [generation_dir+"/result_"+str(i)+".jsonl" for i in range(12)]:
        last_items.append(load_jsonl(filename)[-1]["prompt"])
    last_idx=[]
    data=load_json(prompt_file)
    for i in range(len(data)):
        if data[i] in last_items:last_idx.append(i)
    print(max(last_idx))



if __name__ == '__main__':
    ChatGPT_multiprocess("data/prompt_review_16125.json",save_dir="generation_16125_7",process_num=6,start_index=0)
    pass
