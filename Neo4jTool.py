# coding=utf-8
# Time : 2022/10/11 16:03
# Description : 图数据库Neo4j的操作

from py2neo import Graph
import re

class Neo4jDB():

    def __init__(self, url, username, password):
        # 连接neo4j数据库，输入地址、用户名、密码
        self.graph = Graph(url, auth=(username, password))  # 用户名和密码
        self.count=0

    def execute_CQL(self, CQL):
        # 执行CQL命令
        return self.graph.run(CQL)

    @staticmethod
    def dict2str(d):
        res = ""
        for key, value in d.items():
            if isinstance(value,list):
                value="**".join(value)
            value=value.replace('"','”')
            res += '{}:"{}",'.format(key, value)
        res = "{" + res[:-1] + "}"
        res=res.replace("\\","\\\\").replace("\\\\n","\\n")
        return res

    def add_item(self, item):
        """
        将item项变成一个节点添加到图数据库中
        :param item: 字典，页面中抽出来的项，必须有"name"属性
        :return: 命令执行结果

        先识别name作为节点的名字
        再将剩余的属性全部作为该节点的属性
        """
        CQL = "CREATE (p:unknown{})".format(self.dict2str(item))
        res = self.execute_CQL(CQL)
        self.count+=1
        return res

    def add_attribute_value(self,name,data):
        CQL="MATCH (p:unknown) \nWHERE p.name = '{}'\n".format(name)
        for key,value in data.items():
            value=value.replace("'","").replace('"',"")
            key=key.replace("-","_").replace(" ","_").replace("(","_").replace(")","_")
            CQL+="SET p.{}='{}'\n".format(key,value)
        CQL += "RETURN p"
        self.execute_CQL(CQL)

    def add_label(self,name,label):
        CQL = "MATCH (p:unknown) \nWHERE p.name = '{}'\nSET p:{}".format(name,label)
        self.execute_CQL(CQL)

    def add_relation(self,head,tail,relation):
        """
        建立已有实体节点的关系
        :param name1: 头实体
        :param name2: 尾实体
        :param relation_name: 关系名称
        :return:
        """
        head=head.replace("-","_").replace(" ","_").replace("(","_").replace(")","_").replace("'","").replace('"',"")
        tail=tail.replace("-","_").replace(" ","_").replace("(","_").replace(")","_").replace("'","").replace('"',"")
        CQL='''
        MATCH (head:unknown)
        WHERE head.name = '{}'aaa
        MATCH (tail:unknown)
        WHERE tail.name = '{}'
        CREATE (head)-[r:{}]->(tail) 
        '''.format(head,tail,relation)
        self.execute_CQL(CQL)


        pass
if __name__ == "__main__":
    db = Neo4jDB(url='http://localhost:7474', username="neo4j", password="zyliu")

    item = {'category': ['[[Category:博茨瓦纳行政区划]]'], 'name': '博茨瓦纳行政区划', 'para': '==参见==\n*[[ISO 3166-2:BW]]\n', 'summary': ' \n博茨瓦纳行政区划\n[[波札那]]分为10个行政区（districts）区下再设28个分区（subdistricts）： \n*1.[中部区]（Central District）\n*2.[[杭济区]]（Ghanzi District\n*3.[[卡拉哈迪区]]（Kgalagadi District）\n*4.[[卡特伦区]]（Kgatleng District）\n*5.[[奎嫩区]]（Kweneng District）\n*6.[东北区]（North-East District）\n*7.[西北区]（North-West District）\n*8.[东南区]（South-East District）\n*9.[南部区]（Southern District）\n*10.[[乔贝区]]（Chobe District）\n'}
    print(db.add_item(item))

    """
    装填流程：
    添加全部节点

    将有人物的节点改变

    为人物节点建立链接

    """
