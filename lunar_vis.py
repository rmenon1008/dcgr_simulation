import json
from mesa.visualization.ModularVisualization import VisualizationElement


class LunarVis(VisualizationElement):
    local_includes = [
        "visualization/lunar_vis.js",
        "visualization/styles.css",
        "controls/json_formatter.min.js",
        "controls/controls.js",
        "controls/styles.css",
    ]

    def __init__(self, simWidth, simHeight):
        self.width = simWidth
        self.height = simHeight
        new_element = "new LunarVis({}, {})".format(self.width, self.height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        nodes = []
        for agent in model.schedule.agents:
            nodes.append(agent.get_state())
        return {
            # @Isaac, @Andrew, @Lyla: A good spot for any other model-level
            # state to go like physical objects and radio data. This gets
            # sent to the front-end to be visualized.
            "nodes": nodes,
        }
