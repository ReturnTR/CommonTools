# coding=utf-8
import json
import time
import traceback
import requests
import random
from multiprocessing import Pool
from tqdm import tqdm
from CommonTools.JsonTool import *
import os
CHATGPTURL = 'xxx'

appId = 'xxx'



def get_rps_from_prompt(prompt):
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'appId': appId,
        'messages': [
            {
                'role': 'user',
                'content': prompt,
            },
        ],
    }
    count = 0
    while True:
        count += 1
        try:
            if count > 10:
                break
            response = requests.post(CHATGPTURL, headers=headers, json=json_data)
            time.sleep(5) # qps 太快会抱错
            result = response.json()
            if result is not None:
                result=result.get('data').get('result')
            else:
                continue
            return result
            break
        except:
            print('error, trace=' + traceback.format_exc())

def self_instruct_prompt(filename):
    data=load_json(filename)
    save_file="data/gpt_prompt_review_6_26_1.json"
    for prompt in tqdm(data):
        result = get_rps_from_prompt(prompt)
        sentence = json.dumps(result, ensure_ascii=False)
        data2=load_json(save_file)
        data2.append({"prompt":prompt,"generation":sentence})
        save_json(data2,save_file)
        time.sleep(5)

def get_rps_from_prompt_fun(data):
    """具体实现方法"""
    save_file,prompt=data
    res=get_rps_from_prompt(prompt)
    data2=load_json(save_file)
    data2.append({"prompt":prompt,"generation":res})
    save_json(data2,save_file)
    time.sleep(5)


def multiprocess_data(data,fun,process_num):
    """使用多进程加速数据处理"""
    with Pool(processes = process_num) as pool:result = list(tqdm(pool.imap(fun, data), total=len(data)))
    return result

def self_instruct_prompt_multiprocess_pool(filename,save_dir,process_num=6):
    
    # 设置文件保存倍数，越大越不容易发生冲突
    times=2   

    # 创建文件夹，并在里面生成 process_num*times 个内容为[]的json文件，序列为0 —— process_num*times-1
    os.makedirs(save_dir, exist_ok=True)
    for i in range(process_num*times):save_json([],save_dir+"/result_"+str(i)+".json")  


    # 为Prompt标注保存文件，从1到process_num*2，用元组方式扩展
    data=load_json(filename)
    data=[(save_dir+"/result_"+str(i%process_num*times)+".json",data[i]) for i in range(len(data))]

    # 执行
    multiprocess_data(data,get_rps_from_prompt_fun,process_num)

if __name__ == '__main__':
    # with open('self_instruct.txt', '')
    # print(return_random_prompt()
    self_instruct_prompt_multiprocess_pool("data/prompt_review_16125.json",save_dir="generation_16125")

