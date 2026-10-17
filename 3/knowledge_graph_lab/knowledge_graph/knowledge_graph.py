# knowledge_graph.py

"""
知识图谱的操作函数模块。

图谱 graph 使用 set 存储，每个元素为 (subject, relation, object) 组成的三元组。
"""


def add_triple(graph, subject, relation, object):
    """向 graph 添加三元组；新增返回 True，已存在返回 False。"""
    ### TODO 2.1: 按照函数签名补全代码 ###

    ### TODO 2.1 结束 ###
    pass


def remove_triple(graph, subject, relation, object):
    """从 graph 删除三元组；删除成功返回 True，不存在返回 False。"""
    ### TODO 2.2: 按照函数签名补全代码 ###

    ### TODO 2.2 结束 ###
    pass


def query(graph, subject=None, relation=None, object=None):
    """按条件查询，返回按 (subject, relation, object) 升序排列的列表。

    任一条件为 None 时表示不限制对应字段；多个条件同时给出时取交集。
    查询不可修改 graph；无匹配结果时返回 []。
    """
    return sorted(
        ### TODO 2.3: 按照函数签名补全返回结果 ###

        ### TODO 2.3 结束 ###
    )


def filter_triples(graph, predicate):
    """返回符合 predicate(triple) 的三元组列表。

    要求使用内置 filter()；先按三元组升序排列，再进行筛选。
    """
    ### TODO 2.4: 按照函数签名补全代码 ###
    
    ### TODO 2.4 结束 ###
    pass


def transform_triples(triples, func):
    """将 func 应用于 triples 的每个元素，返回转换后的列表。

    要求使用内置 map()；保持输入 iterable 的遍历顺序，不去重。
    """
    ### TODO 2.5: 按照函数签名补全代码 ###

    ### TODO 2.5 结束 ###
    pass


def make_query(graph, relation):
    """返回一个只接受 subject 参数的关系查询函数。

    调用示例：
        get_uses = make_query(graph, "采用")
        get_uses("ResNet")  # 返回 ResNet 通过“采用”连接的客体列表

    要求使用嵌套函数与闭包；返回按字典序排列的客体列表。
    返回的函数需要保留对原 graph 的引用，能看到创建后的图谱变更。
    """
    
    def find(subject):
        ### TODO 2.6：依照上述注释补全该闭包 ###
        # 补全 triples 和 transform 中的 lambda 函数

        triples = 
        return transform_triples(triples, lambda triple: )
    
        ### TODO 2.6 结束 ###


    return find
