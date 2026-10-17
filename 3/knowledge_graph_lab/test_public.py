# test_public.py

'''
该脚本用于测试知识图谱自身功能是否已经被完备实现。

当前不需要了解该测试代码是如何构建的，只需要会调用它并确保测试结果正确。
代码已经完整，不需要其它补全。
'''

import unittest


class TestPackagesAndData(unittest.TestCase):
    def test_package_import_and_dataset(self):
        from utils import load_graph
        from knowledge_graph import query

        graph, sources = load_graph()
        self.assertEqual(len(graph), 304)
        self.assertEqual(len(sources), 304)
        self.assertEqual(
            query(graph, subject="He初始化", relation="适用于"),
            [("He初始化", "适用于", "ReLU")],
        )
        self.assertEqual(
            sources[("He初始化", "适用于", "ReLU")],
            ("3.3", 46),
        )


class TestBasicFunctions(unittest.TestCase):
    def test_add_and_remove(self):
        from knowledge_graph import add_triple, remove_triple

        graph = set()
        self.assertTrue(add_triple(graph, "A", "属于", "B"))
        self.assertFalse(add_triple(graph, "A", "属于", "B"))
        self.assertEqual(len(graph), 1)
        self.assertTrue(remove_triple(graph, "A", "属于", "B"))
        self.assertFalse(remove_triple(graph, "A", "属于", "B"))
        self.assertEqual(graph, set())

    def test_query_optional_conditions(self):
        from knowledge_graph import query

        graph = {
            ("A", "采用", "B"),
            ("A", "属于", "C"),
            ("D", "采用", "B"),
        }
        self.assertEqual(query(graph, subject="A"), [
            ("A", "属于", "C"), ("A", "采用", "B")
        ])
        self.assertEqual(query(graph, relation="采用", object="B"), [
            ("A", "采用", "B"), ("D", "采用", "B")
        ])
        self.assertEqual(query(graph, subject="不存在"), [])
        self.assertEqual(len(graph), 3)


class TestFunctionalAndClosure(unittest.TestCase):
    def test_filter_and_map(self):
        from knowledge_graph import filter_triples, transform_triples

        graph = {
            ("B", "缓解", "X"),
            ("A", "缓解", "Y"),
            ("A", "属于", "Z"),
        }
        matched = filter_triples(graph, lambda t: t[1] == "缓解")
        self.assertEqual(matched, [("A", "缓解", "Y"), ("B", "缓解", "X")])
        self.assertEqual(
            transform_triples(matched, lambda t: t[2]), ["Y", "X"]
        )
        self.assertEqual(len(graph), 3)

    def test_closure_remembers_relation_and_live_graph(self):
        from knowledge_graph import add_triple, make_query

        graph = {("A", "采用", "B"), ("A", "缓解", "C")}
        uses = make_query(graph, "采用")
        mitigates = make_query(graph, "缓解")
        self.assertEqual(uses("A"), ["B"])
        self.assertEqual(mitigates("A"), ["C"])
        add_triple(graph, "A", "采用", "D")
        self.assertEqual(uses("A"), ["B", "D"])
        self.assertEqual(mitigates("A"), ["C"])


class TestExercises(unittest.TestCase):
    def test_lambda_and_functional_tasks(self):
        from utils import load_graph
        from exercise import (
            task_filter_mitigations,
            # task_sort_mitigations,
            task_collect_mitigated_problems,
        )

        graph, _ = load_graph()
        mitigations = task_filter_mitigations(graph)
        self.assertIn(("残差连接", "缓解", "梯度消失"), mitigations)
        self.assertTrue(all(t[1] == "缓解" for t in mitigations))
        self.assertEqual(mitigations, sorted(mitigations))
        # self.assertEqual(
        #     task_sort_mitigations(graph),
        #     sorted(mitigations, key=lambda t: (t[2], t[0], t[1])),
        # )
        self.assertEqual(
            task_collect_mitigated_problems(graph),
            sorted({t[2] for t in mitigations}),
        )

    def test_closure_task(self):
        from utils import load_graph
        from exercise import task_query_adopted

        graph, _ = load_graph()
        self.assertIn("残差连接", task_query_adopted(graph, "ResNet"))
        self.assertEqual(task_query_adopted(graph, "不存在的概念"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
