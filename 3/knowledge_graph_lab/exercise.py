# exercise.py

'''
对该知识图谱进行的一些简单操作，作为测试脚本。
'''

### TODO 1 开始 ###
# 从 utils 包的公开接口导入 load_graph。
# 从 knowledge_graph 包的公开接口导入下面用到的函数。
# 不要在这里复制这些函数的实现。


### TODO 1 结束 ###

def task_filter_mitigations(graph):
    """使用 lambda 和 filter_triples 筛出所有关系名为“缓解”的三元组。

    返回升序排列的三元组列表。
    """
    ### TODO 3.1: 按照注释要求补全代码 ###

    ### TODO 3.1 结束 ###
    pass


def task_collect_mitigated_problems(graph):
    """利用 filter_triples 与 transform_triples 提取所有 “缓解” 关系的客体。

    返回去重后按字典序排列的字符串列表。
    要求在筛选和转换阶段分别使用 lambda 表达式。
    """
    ### TODO 3.2: 补全其中的 lambda 函数 ###
    mitigations = filter_triples(graph, lambda t: )
    problems = transform_triples(mitigations, lambda t: )

    ### TODO 3.2 结束 ###
    return sorted(set(problems))


def task_query_adopted(graph, subject):
    """使用 make_query 创建固定“采用”关系的查询器，返回 subject 对应的客体列表。"""
    ### TODO 3.3: 使用 make_query 返回对 subject 的查询结果 ###

    ### TODO 3.3 结束 ###
    pass


def main():
    graph, sources = load_graph()
    print(f"已读取 {len(graph)} 条关系，附带 {len(sources)} 条来源记录。")
    print("包含‘缓解’的关系（前 5 条）：", task_filter_mitigations(graph)[:5])
    print("被缓解的问题：", task_collect_mitigated_problems(graph))
    print("ResNet 采用：", task_query_adopted(graph, "ResNet"))


if __name__ == "__main__":
    main()
