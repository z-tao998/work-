# load_data.py

'''
该脚本用于从 chapter_triples.csv 中提取数据并生成结构化知识图谱。

可以通过该脚本观察该知识图谱是如何构建的。
脚本已经完成，不需要其它补全。
'''

import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "chapter_triples.csv"


def load_graph(path=DATA_FILE):
    """读取课程数据，返回 (graph, sources)。

    graph: set，元素为 (主体, 关系, 客体) 三元组。
    sources: dict，键为三元组，值为 (章节代号, PDF 页码)。
    """
    graph = set()
    sources = {}

    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            triple = (row["subject"], row["relation"], row["object"])
            graph.add(triple)
            sources[triple] = (row["source"], int(row["page"]))

    return graph, sources
