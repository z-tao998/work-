"""Launch the interactive Matplotlib physics-graph experiment.

Run on a machine with a graphical desktop:
    python main.py
    python main.py --dt 0.25 --steps 200 --interval 100
"""

import argparse

from dynamics import GraphDynamics, IndependentDynamics
from graph import StateGraph
from visualization import LiveSimulation


INITIAL_STATE = {"load": 0.18, "temperature": 0.08, "vibration": 0.025}
BASE_RATES = {"load": 0.014, "temperature": 0.003, "vibration": 0.001}
DAMPING = {"load": 0.023, "temperature": 0.090, "vibration": 0.140}


def build_models(dt=0.5):
    """Create two comparable models from exactly the same initial state."""
    graph = StateGraph(INITIAL_STATE)
    graph.add_edge("load", "temperature", 0.075)
    graph.add_edge("temperature", "vibration", 0.120)
    graph.add_edge("load", "vibration", 0.014)

    independent = IndependentDynamics(INITIAL_STATE, BASE_RATES, DAMPING, dt)
    coupled = GraphDynamics(INITIAL_STATE, BASE_RATES, DAMPING, graph, dt)
    return graph, independent, coupled


def main():
    parser = argparse.ArgumentParser(description="Live graph dynamics lab (Matplotlib)")
    parser.add_argument("--steps", type=int, default=120, help="maximum simulation steps")
    parser.add_argument("--dt", type=float, default=0.5, help="Euler simulation step")
    parser.add_argument("--interval", type=int, default=100, help="milliseconds between animation frames")
    args = parser.parse_args()
    if args.steps < 1 or args.interval < 1:
        parser.error("steps and interval must be positive")

    # Rebuilding the models allows the Reset button to restore the initial state.
    def create_models():
        return build_models(dt=args.dt)
    viewer = LiveSimulation(create_models, max_steps=args.steps, interval_ms=args.interval)
    viewer.show()


if __name__ == "__main__":
    main()
