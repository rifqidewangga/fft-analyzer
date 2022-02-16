"""
This module contains user defined toolbar class for plot visibility toggling and csv import
"""
import os
from matplotlib.backend_tools import ToolBase
import matplotlib.pyplot as plt
from enum import Enum, auto
import warnings

warnings.filterwarnings("ignore", ".*Treat the new Tool classes introduced in v1.5 as experimental.*", )

plt.rcParams["toolbar"] = "toolmanager"
BASE_PATH = os.path.dirname(__file__)


class Tools(Enum):
    OPEN_FILE = auto()
    TOGGLE_X_VIS = auto()
    TOGGLE_Y_VIS = auto()
    TOGGLE_Z_VIS = auto()


class CallBackNotSet(Exception):
    pass


class OpenFile(ToolBase):
    image = f'{BASE_PATH}/icons/open-file.png'
    callback = None
    description = "Import CSV file"

    def trigger(self, sender, event, data=None):
        if self.callback is None:
            raise CallBackNotSet
        OpenFile.callback()


class ToggleXVisibility(ToolBase):
    image = f'{BASE_PATH}/icons/x.png'
    callback = None
    description = "Toggle X Axis"

    def trigger(self, sender, event, data=None):
        if self.callback is None:
            raise CallBackNotSet
        ToggleXVisibility.callback()


class ToggleYVisibility(ToolBase):
    image = f'{BASE_PATH}/icons/y.png'
    callback = None
    description = "Toggle Y Axis"

    def trigger(self, sender, event, data=None):
        if self.callback is None:
            raise CallBackNotSet
        ToggleYVisibility.callback()


class ToggleZVisibility(ToolBase):
    image = f'{BASE_PATH}/icons/z.png'
    callback = None
    description = "Toggle Z Axis"

    def trigger(self, sender, event, data=None):
        if self.callback is None:
            raise CallBackNotSet
        ToggleZVisibility.callback()


class ToolbarController:
    def __init__(self, figure: plt.Figure):
        self._figure = figure

        self.file_interaction_tools_dict = {"Tools.OPEN_FILE": OpenFile}
        self.visibility_tools_dict = {"Tools.TOGGLE_X_VIS": ToggleXVisibility,
                                      "Tools.TOGGLE_Y_VIS": ToggleYVisibility,
                                      "Tools.TOGGLE_Z_VIS": ToggleZVisibility}

        self.remove_unnecessary_tools()
        self.create_visibility_toolbar()
        self.create_file_interaction_toolbar()

    def create_visibility_toolbar(self):
        tm = self._figure.canvas.manager.toolmanager

        group_name = "axis_visibility"

        for tool_name in self.visibility_tools_dict:
            tm.add_tool(tool_name, self.visibility_tools_dict[tool_name])
            self._figure.canvas.manager.toolbar.add_tool(tm.get_tool(tool_name), group_name)

    def create_file_interaction_toolbar(self):
        tm = self._figure.canvas.manager.toolmanager

        group_name = "file_interaction"

        for tool_name in self.file_interaction_tools_dict:
            tm.add_tool(tool_name, self.file_interaction_tools_dict[tool_name])
            self._figure.canvas.manager.toolbar.add_tool(tm.get_tool(tool_name), group_name)

    def remove_unnecessary_tools(self):
        self._figure.canvas.manager.toolmanager.remove_tool("subplots")
        self._figure.canvas.manager.toolmanager.remove_tool("help")

    @staticmethod
    def set_toolbar_callback():
        OpenFile.callback = None
        ToggleXVisibility.callback = None
        ToggleYVisibility.callback = None
        ToggleZVisibility.callback = None
