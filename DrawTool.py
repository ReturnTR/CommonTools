# coding=utf-8
# Time : 2022/11/9 22:55
# Description : 提供画图的功能

import matplotlib.pyplot as plt
import matplotlib
class Draw():


    def __init__(self,use_color=True,save_dir="",is_show=True):

        # 初始化操作
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
        self.color = ["red", "yellow", "green", "black", "orange", "brown"]  # 彩色原料

        # 配置
        self.use_color=use_color  # 是否使用彩色
        self.save_dir=save_dir    # 图片保存地址，默认不保存
        self.is_show=is_show   # 是否显示出来


    def configure(self,**kwargs):
        """设置全局属性"""
        if "use_color" in kwargs:self.use_color=kwargs["use_color"]
        if "save_dir" in kwargs: self.save_dir = kwargs["save_dir"]
        if "is_show" in kwargs: self.is_show = kwargs["is_show"]

    def process_list_two_data(self,data):
        """处理n×2类型的数据"""
        if isinstance(data,dict):
            return [key for key in data],[value for value in data.values()]
        elif isinstance(data,list):
            return [i[0]for i in data],[i[1]for i in data]
        else:
            print("process_list_two_data：类型非法！")

    def do(self):
        """图像设置好之后的操作"""
        if self.save_dir!="":plt.savefig(self.save_dir)
        if self.is_show:plt.show()

    def histogram(self,data,is_vertical=True): #重复性
        """
        柱状图
        :param data: 1.元组列表，2.二维列表，第二维长度必须是2，3.字典，值必须为数字
            例: [("label_1",1),("lable_2",2),...]
        :param is_vertical:是否采用垂直的柱状图，否则采用横着的柱状图
        """

        name_list,num_list=self.process_list_two_data(data)

        if is_vertical is True:
            if self.use_color:
                plt.bar(range(len(num_list)), num_list, color=self.color, tick_label=name_list)
            else:
                plt.bar(range(len(num_list)), num_list, tick_label=name_list)

        else:
            # 图像绘制
            fig, ax = plt.subplots()
            if self.use_color:
                b = ax.barh(range(len(name_list)), num_list, color=self.color)
            else:
                b = ax.barh(range(len(name_list)), num_list)
            # 添加数据标签
            for rect in b:
                w = rect.get_width()
                ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' % int(w), ha='left', va='center')
            # 设置Y轴刻度线标签
            ax.set_yticks(range(len(name_list)))
            ax.set_yticklabels(name_list)

        self.do()



if __name__ == "__main__":
    draw=Draw()
    draw.configure()
    draw.histogram([("label_1",1),("lable_2",2),("label_1",1),("lable_2",2)])




