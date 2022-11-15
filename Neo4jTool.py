# coding=utf-8
# Time : 2022/10/11 16:03
# Description : 图数据库Neo4j的操作

from py2neo import *
import py2neo
import re

class Neo4jDB():
    """
    包含所有的cypher语句
    如何让其方便是一个需要考虑的问题
    字符串处理应该在这之前，或者新建一个字符串模块，neo4j的字符串与java相同，变量名也相同

    """
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

    def add_attribute_value(self,label,name,infobox,new_label="person"):
        """设置属性值，设置标签"""

        CQL="MATCH (p:{}) \nWHERE p.name = '{}'\n".format(label,name)
        for key,value in infobox.items():
            key=re.sub("[^\u4e00-\u9fa5a-z0-9_]","_",key)
            if key =="" or key is None: continue
            if not isinstance(value,list):
                value=value.replace("'","").replace('"',"").replace("\\","")
                CQL += "SET p.{}='{}'\n".format(key, value)
            else:
                value=str(value)
                CQL+="SET p.{}={}\n".format(key,value)
        CQL+="SET p:{}\n".format(new_label)
        CQL += "RETURN p.name"

        try:
            self.execute_CQL(CQL)
        except py2neo.errors.ClientError:
            print(CQL)

    def add_label(self,node,label):
        node.add_label(label)
        return node

    def add_label_CQL(self,or_label,name,new_label):
        CQL='match (p:{})\nwhere p.name="{}"\nset p:{}\nreturn p.name'.format(or_label,name,new_label)
        self.execute_CQL(CQL)

    def copy_node(self,node):
        new_node=Node()
        new_node.update(dict(node))
        for label in node.labels:
            new_node.add_label(label)
        return new_node

    def create_node(self,labels,pairs):
        """
        创建节点
        :param labels: 标签列表
        :param pairs: 属性值字典
        :return: 节点
        """
        node=Node()
        for label in labels:
            node.add_label(label)
        node.update(pairs)
        return node


    def search_node_by_name(self,label,name):
        """寻找特定标签和特定name属性的节点"""
        return NodeMatcher(self.graph).match(label, name=name).first()

    def update_node(self,node,label,name="name"):
        self.graph.merge(node, label, name)

    def add_node(self,node):
        tx = self.graph.begin()  # 开始一个Transaction
        tx.create(node)
        tx.commit()  # push到服务器

    def exist(self,sb):
        return self.graph.exists(sb)


    def add_relation(self,relation):
        self.graph.create(relation)

    def search_attribute(self,attribute,label="unknown",limit=200):
        """查询指定属性名称的属性值"""
        CQL="match (p:{})\nwhere p.{} is not null\nreturn p.{} limit {}".format(label,attribute,attribute,limit)
        res=self.execute_CQL(CQL)
        records=[i[0] for i in res]
        return records


if __name__ == "__main__":

    # 测试
    db = Neo4jDB(url='http://localhost:7474', username="neo4j", password="zyliu")
    if db:print("连接成功！")
    # item = {'category': ['[[Category:博茨瓦纳行政区划]]'], 'name': '博茨瓦纳行政区划', 'para': '==参见==\n*[[ISO 3166-2:BW]]\n', 'summary': ' \n博茨瓦纳行政区划\n[[波札那]]分为10个行政区（districts）区下再设28个分区（subdistricts）： \n*1.[中部区]（Central District）\n*2.[[杭济区]]（Ghanzi District\n*3.[[卡拉哈迪区]]（Kgalagadi District）\n*4.[[卡特伦区]]（Kgatleng District）\n*5.[[奎嫩区]]（Kweneng District）\n*6.[东北区]（North-East District）\n*7.[西北区]（North-West District）\n*8.[东南区]（South-East District）\n*9.[南部区]（Southern District）\n*10.[[乔贝区]]（Chobe District）\n'}
    # print(db.add_item(item))
    #
    # node = db.search_node_by_name("person","习近")
    # print(node)
    #
    # b = Node("Person", name="Bob")
    # print(b["name"])
    # print(b)

    res=db.search_attribute("children")
    print(res)