# coding=utf-8
# Time : 2022/10/12 22:52
# Description : csv 的一些操作
import csv

def save_csv(data,filename):
    """data是二维列表"""
    f = open(filename, 'w', encoding='utf-8', newline='')
    for i in data:
        for j in range(len(i)-1):
            f.write(str(i[j])+",")
        f.write(str(i[-1])+"\n")
    f.close()


def load_csv(filename):
    """读取文件数据到二维列表上"""
    with open(filename, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        data=[i for i in spamreader]
    return data
if __name__ == "__main__":

    print("hello")
