# coding=utf-8
# Time : 2022/10/11 16:03
# Description : 图数据库Neo4j的操作

from py2neo import Graph


class Neo4jDB():

    def __init__(self, url, username, password):
        # 连接neo4j数据库，输入地址、用户名、密码
        self.graph = Graph(url, auth=(username, password))  # 用户名和密码

    def execute_CQL(self, CQL):
        # 执行CQL命令
        return self.graph.run(CQL)

    @staticmethod
    def dict2str(d):
        res = ""
        for key, value in d.items():
            res += "{}:'{}',".format(key, value)
        res = "{" + res[:-1] + "}"
        return res

    def add_node(self, item):
        """
        将item项变成一个节点添加到图数据库中
        :param item: 字典，页面中抽出来的项，必须有"name"属性
        :return: 命令执行结果

        先识别name作为节点的名字
        再将剩余的属性全部作为该节点的属性
        """
        name = item["name"]
        CQL = "CREATE ({}:unknown{})".format(name, self.dict2str(item))
        print(CQL)
        res = self.execute_CQL(CQL)
        return res


if __name__ == "__main__":
    db = Neo4jDB(url='http://localhost:7474', username="neo4j", password="zyliu")

    item = {
        "name": "中国",
        "infobox": "inininnfobox",
        "para": "abcdefghigklmn"
    }
    print(db.add_node(item))

    """
    装填流程：
    添加全部节点

    将有人物的节点改变

    为人物节点建立链接

    """
