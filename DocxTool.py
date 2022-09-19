from docx import Document
from lxml import etree

# 不同文件的命名空间不同，需要查阅word里面的xml文件内容进行修改
w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def get_xml(filename):
    """
    返回docx中的xml格式，类型为element
    """
    return Document(filename)._body._element.xml

def get_text(element):
    """
    获取该节点下的所有文字
    :return:
    """
    test_list = element.xpath(".//w:t", namespaces={"w": w})
    return "".join([i.text for i in test_list])

def extract_xml(xml):
    """
    获取文段信息和表格信息的粗数据
    :param filename:
    :return: 列表类型，表格为二维列表
    """
    xml = etree.fromstring(xml)
    # 获取所有段落节点和表格节点
    p_and_tbl=xml.xpath("/w:body/w:p |/w:body/w:tbl",namespaces={"w":w})

    res=[]
    for item in p_and_tbl:
        # 线性找段落和表格
        if item.tag[-1]=="p": # 标签
            # print(etree.tounicode(item))
            text=get_text(item)
            if text!="":
                text=text.replace(":","：")
                res.append(text)
        else: #表
            # print(etree.tounicode(item))
            # 获取一行的制表
            trs=item.xpath("./w:tr",namespaces={"w": w})
            table_list=[]
            for tr in trs:
                tcs=tr.xpath("./w:tc",namespaces={"w": w})
                table_list_i=[]
                for i in tcs:
                    p=i.findall("w:p",namespaces={"w": w})
                    t=[get_text(i) for i in p]
                    # if len(t)==1:t=t[0]
                    # else:
                    #     for k in ["当前","目前","计划","无"]:
                    #         if k in t:t.remove(k)
                    table_list_i.append("\n".join(t))
                table_list.append(table_list_i)
            res.append(table_list)

    return res

def get_info(filename):
    return extract_xml(get_xml(filename))


def flags_of_p(p):
    """
    处理每一个P标签
    需要用到的信息有：
        是否在中央
        是否加粗
    """

    def get_text(element):
        """
        获取该节点下的所有文字
        :return:
        """
        test_list = element.xpath(".//w:t", namespaces={"w": w})
        return "".join([i.text for i in test_list])

    # 存放所有标志
    flags = {
        "center": False,  # 是否居中
        "B": False,  # 整段是否加粗
        "加粗文字": []

    }
    # 判断该段是否居中
    jc = p.find("w:pPr", namespaces={"w": w}).find("w:jc", namespaces={"w": w})
    if jc is not None:
        if jc.attrib["{" + w + "}val"] == "center":
            flags["center"] = True
    # 判断该段是否加粗标志
    style = p.find("w:pPr", namespaces={"w": w}).find("w:pStyle", namespaces={"w": w})

    if style is not None:
        if style.attrib.values()[0] in "2345":  # 通过判断Style类型来判断是否整段居中
            flags["B"] = True
    else:
        r = p.findall("w:r", namespaces={"w": w})
        for i in r:
            b = i.find("w:rPr", namespaces={"w": w}).find("w:b", namespaces={"w": w})
            if b is not None:
                attrib = b.attrib
                if attrib == {}:
                    flags["加粗文字"].append(get_text(i))
                elif attrib.values()[0] == "0":
                    pass
                else:
                    print("遇到无法识别加粗的文字")
    return flags