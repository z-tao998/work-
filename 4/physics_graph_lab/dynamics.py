"""Discrete-time simulations of independent and graph-coupled dynamics."""




class DynamicsModel:
    """Base class that owns time integration and records state histories."""

    def __init__(self, initial_state, dt=1.0):
        self.state = dict(initial_state)
        self.dt = float(dt)
        if self.dt <= 0:
            raise ValueError("dt must be positive")
        self.time = 0.0
        self.history = [self.snapshot()]

    def snapshot(self):
        """Return an independent record of the current model state."""

        ### TODO 1.1: 补全 snapshot 函数，其返回一个字典，记录 time 和 state
        
        ### TODO 1.1 结束

    def derivatives(self, state):
        """Subclasses supply dx/dt for every state variable."""

        # 求导函数，父类只提供函数签名，具体实现由子类重写。
        raise NotImplementedError("Subclasses must implement derivatives()")

    def step(self):
        """Advance all variables *simultaneously* using forward Euler."""
        old_state = self.state.copy()
        rates = self.derivatives(old_state)

        ### TODO 1.2: 补全对 state 和 time 的更新

        ### TODO 1.2 结束

        record = self.snapshot()
        self.history.append(record)
        return record

    def simulate(self, steps):
        """Run additional steps and return the entire recorded trajectory."""
        if steps < 0:
            raise ValueError("steps must not be negative")

        ### TODO 1.3: 执行 steps 步动力学演化

        ### TODO 1.3 结束

        return self.history


### TODO 1.4: 补全类之间的继承关系: 
### DynamicsModel -> IndependentDynamics -> GraphDynamics;

class IndependentDynamics():
    """dx_i/dt = base_rate_i - damping_i * x_i."""

    def __init__(self, initial_state, base_rates, damping, dt=1.0):

        ### TODO 1.5: 补全类继承的初始化 super().__init__

        ### TODO 1.5 结束

        self.base_rates = dict(base_rates)
        self.damping = dict(damping)
        if set(self.base_rates) != set(self.state) or set(self.damping) != set(self.state):
            raise ValueError("Every state must have a base rate and damping coefficient")

    def derivatives(self, state):
        ### TODO 1.6: 根据手册中的公式补全动力学演化方程

        ### TODO 1.6 结束


class GraphDynamics():
    """Include messages from incoming edges in each state's derivative."""

    def __init__(self, initial_state, base_rates, damping, graph, dt=1.0):

        ### TODO 1.7: 补全类继承的初始化 super().__init__
        
        ### TODO 1.7 结束

        if set(graph.nodes) != set(self.state):
            raise ValueError("Graph nodes must match the model's state variables")
        self.graph = graph

    def message(self, source, target, weight, state):
        """Message from node source to node target (target is for clarity)."""
        
        ### TODO 1.8: 根据手册中的公式补全 GNN 的消息传递

        ### TODO 1.8 结束

    def aggregate(self, node, state):
        """Sum incoming messages addressed to one node."""
        
        ### TODO 1.9: 补全 GNN 的消息聚合，这里只做简单求和 (sum)

        ### TODO 1.9 结束

    def derivatives(self, state):
        rates = super().derivatives(state)

        ### TODO 1.10: 用聚合到的信息对 GNN 每个节点的 rates 作更新

        ### TODO 1.10 结束

        return rates

### TODO 1.4 结束