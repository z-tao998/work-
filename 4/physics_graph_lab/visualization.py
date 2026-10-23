"""Matplotlib GUI for a live graph-coupled dynamical simulation.

Only this file knows about Matplotlib.  Each animation tick calls the
real step() methods implemented in dynamics.py; no frames are precomputed.
"""

import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.widgets import Button, Slider


BACKGROUND = "#F5F7FB"
INK = "#25304A"
MUTED = "#68758A"
GRID = "#E7EBF3"
COLORS = ("#4978D0", "#EC9560", "#2CA893", "#9C76C5", "#C39B39")


class LiveSimulation:
    """Drive two Python models and show their state changes in a local window."""

    def __init__(self, create_models, max_steps=120, interval_ms=100):
        self.create_models = create_models
        self.graph, self.independent, self.coupled = create_models()
        self.names = list(self.coupled.state)
        self.colors = {name: COLORS[i % len(COLORS)] for i, name in enumerate(self.names)}
        self.max_steps = max_steps
        self.interval_ms = interval_ms
        self.playing = True

        self.fig = plt.figure(figsize=(14.6, 8.6), facecolor=BACKGROUND)
        self.fig.canvas.manager.set_window_title("Physics Graph Lab") if hasattr(self.fig.canvas.manager, "set_window_title") else None
        grid = self.fig.add_gridspec(
            2, 2, left=0.080, right=0.96, bottom=0.27, top=0.83,
            width_ratios=[1.05, 1.8], height_ratios=[1.1, 0.62],
            wspace=0.18, hspace=0.32,
        )
        self.ax_graph = self.fig.add_subplot(grid[0, 0])
        self.ax_rates = self.fig.add_subplot(grid[1, 0])
        self.ax_history = self.fig.add_subplot(grid[:, 1])

        self.fig.text(0.080, 0.946, "PHYSICS GRAPH LAB", color=INK, fontsize=20, weight="bold")
        self.fig.text(
            0.080, 0.913,
            "A live Python simulation  ·  Coupled vs. independent dynamics",
            color=MUTED, fontsize=10,
        )
        self.status = self.fig.text(0.96, 0.946, "", color=INK, fontsize=11, ha="right", va="center")
        self.fig.text(
            0.080, 0.037,
            "Every frame executes GraphDynamics.step() and IndependentDynamics.step() directly.",
            color=MUTED, fontsize=9,
        )

        self._init_graph()
        self._init_rates()
        self._init_history()
        self._init_controls()
        self._render()

        # Keep this reference: Matplotlib stops the timer if FuncAnimation is collected.
        self.animation = FuncAnimation(
            self.fig, self._animate, interval=interval_ms,
            cache_frame_data=False, blit=False,
        )

    @staticmethod
    def _style_axis(ax, title):
        ax.set_facecolor("white")
        for spine in ax.spines.values():
            spine.set_color(GRID)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.set_title(title, loc="left", color=INK, fontsize=12, weight="bold", pad=15)

    def _positions(self):
        if self.names == ["load", "temperature", "vibration"]:
            return {"load": (0.24, 0.74), "temperature": (1.29, 0.74), "vibration": (0.765, 0.22)}
        count = len(self.names)
        return {
            name: (0.765 + 0.53 * math.cos(2 * math.pi * i / count - math.pi / 2),
                   0.5 + 0.34 * math.sin(2 * math.pi * i / count - math.pi / 2))
            for i, name in enumerate(self.names)
        }

    def _init_graph(self):
        ax = self.ax_graph
        self._style_axis(ax, "01   State dependency graph")
        ax.set(xlim=(0, 1.53), ylim=(0, 1), aspect="equal")
        ax.set_anchor("W")
        ax.set_xticks([])
        ax.set_yticks([])
        self.positions = self._positions()
        self.edge_artists = []

        for source, target, weight in self.graph.edges:
            x1, y1 = self.positions[source]
            x2, y2 = self.positions[target]
            arrow = FancyArrowPatch(
                (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=17,
                shrinkA=37, shrinkB=37, linewidth=1.7, color="#99A6B7",
                zorder=2,
            )
            ax.add_patch(arrow)
            dx, dy = x2 - x1, y2 - y1
            length = max(math.hypot(dx, dy), 1e-6)
            mid_x = (x1 + x2) / 2 - dy / length * 0.07
            mid_y = (y1 + y2) / 2 + dx / length * 0.07
            annotation = ax.text(
                mid_x, mid_y, "", fontsize=8.5, ha="center", va="center",
                color=MUTED, bbox=dict(facecolor="white", edgecolor="none", pad=2),
                zorder=3,
            )
            self.edge_artists.append((arrow, annotation, source, target, weight))

        self.node_artists = {}
        for name in self.names:
            x, y = self.positions[name]
            color = self.colors[name]
            node = Circle((x, y), 0.105, linewidth=2.4, edgecolor=color, facecolor="white", zorder=4)
            ax.add_patch(node)
            short_name = {"temperature": "TEMP", "vibration": "VIB"}.get(name, name.upper())
            title = ax.text(x, y + 0.027, short_name, ha="center", va="center",
                            fontsize=8.2, weight="bold", color=INK, zorder=5)
            value = ax.text(x, y - 0.035, "", ha="center", va="center",
                            fontsize=12, weight="bold", color=color, zorder=5)
            self.node_artists[name] = (node, title, value)
        ax.text(0.5, 0.04, "Edge labels show: weight  ·  current message",
                ha="center", fontsize=8.5, color=MUTED)

    def _init_history(self):
        ax = self.ax_history
        self._style_axis(ax, "02   State trajectories")
        ax.set_xlabel("Simulation time", color=MUTED, fontsize=10)
        ax.set_ylabel("Normalized state", color=MUTED, fontsize=10)
        ax.grid(True, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        self.lines = {}
        for name in self.names:
            color = self.colors[name]
            (line,) = ax.plot([], [], lw=2.5, color=color, label=name.capitalize())
            (baseline,) = ax.plot([], [], lw=1.5, color=color, alpha=0.35, linestyle="--")
            self.lines[name] = line, baseline
        ax.legend(frameon=False, loc="upper left", ncol=min(3, len(self.names)), fontsize=9)
        ax.text(0.99, 0.98, "Solid: graph-coupled    Dashed: independent",
                transform=ax.transAxes, ha="right", va="top", fontsize=8.5, color=MUTED)

    def _init_rates(self):
        ax = self.ax_rates
        self._style_axis(ax, "03   Instantaneous rate of change")
        ax.axvline(0, color=GRID, linewidth=1.2)
        ax.set_yticks(range(len(self.names)), [name.capitalize() for name in self.names])
        ax.invert_yaxis()
        ax.set_xlabel("dx/dt", fontsize=9, color=MUTED)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ys = list(range(len(self.names)))
        self.rate_bars_graph = ax.barh([y - 0.15 for y in ys], [0] * len(ys),
                                       0.27, color=[self.colors[n] for n in self.names])
        self.rate_bars_independent = ax.barh([y + 0.15 for y in ys], [0] * len(ys),
                                             0.27, color="#D4DAE5")
        ax.set_xlim(-0.02, 0.04)
        ax.text(0.02, 0.06, "Color: coupled    Gray: independent",
                fontsize=8.4, color=MUTED, transform=ax.transAxes)

    def _init_controls(self):
        def control_axes(left, width):
            return self.fig.add_axes((left, 0.105, width, 0.072), facecolor="white")

        self.play_button = Button(control_axes(0.055, 0.135), "Pause", color="white", hovercolor="#E9EFFA")
        self.step_button = Button(control_axes(0.202, 0.118), "Step +1", color="white", hovercolor="#E9EFFA")
        self.reset_button = Button(control_axes(0.332, 0.118), "Reset", color="white", hovercolor="#E9EFFA")
        for button in (self.play_button, self.step_button, self.reset_button):
            button.label.set_color(INK)
            button.label.set_fontsize(11)
        self.play_button.on_clicked(self._toggle_play)
        self.step_button.on_clicked(self._single_step)
        self.reset_button.on_clicked(self._reset)
        slider_ax = self.fig.add_axes((0.65, 0.12, 0.27, 0.032), facecolor=BACKGROUND)
        self.speed_slider = Slider(slider_ax, "Frame interval (ms)", 30, 500,
                                   valinit=self.interval_ms, valstep=10, color="#4978D0")
        self.speed_slider.label.set_color(MUTED)
        self.speed_slider.valtext.set_color(INK)
        self.speed_slider.on_changed(self._change_speed)

    def _change_speed(self, value):
        self.animation.event_source.interval = int(value)

    def _pause(self):
        self.playing = False
        self.play_button.label.set_text("Play")
        self.animation.event_source.stop()

    def _toggle_play(self, _event):
        if self.playing:
            self._pause()
        elif len(self.coupled.history) - 1 < self.max_steps:
            self.playing = True
            self.play_button.label.set_text("Pause")
            self.animation.event_source.start()
        self.fig.canvas.draw_idle()

    def _advance_one(self):
        """The only place where the two physical models advance in time."""
        if len(self.coupled.history) - 1 >= self.max_steps:
            return
        self.independent.step()
        self.coupled.step()

    def _single_step(self, _event):
        self._pause()
        self._advance_one()
        self._render()
        self.fig.canvas.draw_idle()

    def _reset(self, _event):
        self._pause()
        self.graph, self.independent, self.coupled = self.create_models()
        self._render()
        self.fig.canvas.draw_idle()

    def _animate(self, _frame):
        if self.playing:
            self._advance_one()
            if len(self.coupled.history) - 1 >= self.max_steps:
                self._pause()
            self._render()
        return []

    def _render(self):
        state = self.coupled.state
        for name, (_, _, label) in self.node_artists.items():
            label.set_text(f"{state[name]:.3f}")

        for arrow, label, source, target, weight in self.edge_artists:
            # Recompute labels directly from current model state, not static samples.
            message = self.coupled.message(
                source, target, weight, state
            )
            arrow.set_linewidth(1.4 + min(3.5, 60 * abs(message)))
            arrow.set_color("#C57B70" if message < 0 else "#7599BF")
            label.set_text(f"w={weight:+.3f}\nm={message:+.3f}")

        times = [record["time"] for record in self.coupled.history]
        for name, (line, baseline) in self.lines.items():
            line.set_data(times, [row["state"][name] for row in self.coupled.history])
            baseline.set_data(times, [row["state"][name] for row in self.independent.history])
        ax = self.ax_history
        ax.set_xlim(0, max(8.0, self.coupled.time * 1.12))
        values = [abs(row["state"][name]) for row in self.coupled.history for name in self.names]
        values += [abs(row["state"][name]) for row in self.independent.history for name in self.names]
        ax.set_ylim(-0.04, max(0.25, max(values, default=0) * 1.15))

        rates_coupled = self.coupled.derivatives(self.coupled.state)
        rates_independent = self.independent.derivatives(self.independent.state)
        for name, b_graph, b_independent in zip(self.names, self.rate_bars_graph, self.rate_bars_independent):
            b_graph.set_width(rates_coupled[name])
            b_independent.set_width(rates_independent[name])
        peak = max([abs(v) for v in rates_coupled.values()] +
                   [abs(v) for v in rates_independent.values()] + [0.012])
        self.ax_rates.set_xlim(-1.35 * peak, 1.35 * peak)
        self.status.set_text(f"t = {self.coupled.time:.1f}    |    step {len(times) - 1} / {self.max_steps}")

    def show(self):
        plt.show()
