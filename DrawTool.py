# coding=utf-8
# Time : 2022/11/9 22:55
# Description : 提供画图的功能

import matplotlib.pyplot as plt
import matplotlib
class Draw():


    def __init__(self):
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    def process_list_two_data(self,data):
        """处理n×2类型的数据"""
        if isinstance(data,dict):
            return [key for key in data],[value for value in data.values()]
        elif isinstance(data,list):
            return [i[0]for i in data],[i[1]for i in data]
        else:
            print("process_list_two_data：类型非法！")

    def draw_histogram(self,data,use_color=False,is_vertical=True,save_dir="",is_show=True): #重复性
        """
        柱状图
        :param data: 1.元组列表，2.二维列表，第二维长度必须是2，3.字典，值必须为数字
            例: [("label_1",1),("lable_2",2),...]
        :param use_color:是否使用彩色标识
        :param is_vertical:是否采用垂直的柱状图，否则采用横着的柱状图
        :return: 图
        """
        color=["red","yellow","green","black","orange","brown"]
        name_list,num_list=self.process_list_two_data(data)

        if is_vertical is True:
            if use_color:
                plt.bar(range(len(num_list)), num_list, color=color, tick_label=name_list)
            else:
                plt.bar(range(len(num_list)), num_list, tick_label=name_list)

        else:
            # 图像绘制
            fig, ax = plt.subplots()
            b = ax.barh(range(len(name_list)), num_list, color=color)

            # 添加数据标签
            for rect in b:
                w = rect.get_width()
                ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' % int(w), ha='left', va='center')

            # 设置Y轴刻度线标签
            ax.set_yticks(range(len(name_list)))
            # 设置字体
            # font=FontProperties(fname=r'/Library/Fonts/Songti.ttc')
            ax.set_yticklabels(name_list)

        if save_dir!="":plt.savefig(save_dir)
        if is_show:plt.show()



if __name__ == "__main__":
    draw_histogram([("label_1",1),("lable_2",2),("label_1",1),("lable_2",2)],use_color=True,is_vertical=False)




