"""A small directed weighted graph used by the dynamics experiment."""


class StateGraph:
    """Represent dependencies among named physical state variables.

    Every edge is (source, target, weight).  The edge source -> target
    means that the source contributes weight * source_state to the
    target's rate of change.
    """

    def __init__(self, nodes):
        self.nodes = list(nodes)
        if len(set(self.nodes)) != len(self.nodes):
            raise ValueError("Node names must be unique")
        self.edges = []

    def add_edge(self, source, target, weight):
        """Add one directed edge, allowing positive or negative influence."""
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("Both ends of an edge must be in the graph")

        ### TODO 2.1: 为自身 edge 列表添加边 (source, target, weight)
        self.edges.append((source, target, weight))
        ### TODO 2.1 结束

    def incoming(self, target):
        """Return (source, weight) pairs for all edges ending at target."""
        if target not in self.nodes:
            raise ValueError(f"Unknown node: {target}")
        return [
            ### TODO 2.2: 返回以 target 节点为末尾的所有边对 (source, weight)
            (source, weight)
            for source, dest, weight in self.edges
            if dest == target
            ### TODO 2.2 结束
        ]
