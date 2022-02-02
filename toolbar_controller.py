from matplotlib.backend_tools import ToolBase
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["toolbar"] = "toolmanager"

CALLBACK_DICT = {}


class CallBackNotSet(Exception):
    pass


def invoke_callback(key):
    try:
        CALLBACK_DICT[key]()
    except KeyError:
        raise CallBackNotSet(key)


class OpenFile(ToolBase):
    image = 'icons/open-file.png'
    callback_key = 'OpenFile'

    def trigger(self, sender, event, data=None):
        invoke_callback(self.callback_key)


class ToggleXVisibility(ToolBase):
    image = "icons/x.png"
    callback_key = 'ToggleXVisibility'

    def trigger(self, sender, event, data=None):
        invoke_callback(self.callback_key)


class ToggleYVisibility(ToolBase):
    image = "icons/y.png"
    callback_key = 'ToggleYVisibility'

    def trigger(self, sender, event, data=None):
        invoke_callback(self.callback_key)


class ToggleZVisibility(ToolBase):
    image = "icons/z.png"
    callback_key = 'ToggleZVisibility'

    def trigger(self, sender, event, data=None):
        invoke_callback(self.callback_key)


visibility_tools_dict = {ToggleXVisibility.callback_key: ToggleXVisibility,
                         ToggleYVisibility.callback_key: ToggleYVisibility,
                         ToggleZVisibility.callback_key: ToggleZVisibility}

file_interaction_tools_dict = {OpenFile.callback_key: OpenFile}


class ToolbarController:
    def __init__(self, figure: plt.Figure):
        self._figure = figure

        self.remove_unnecessary_tools()
        self.create_visibility_toolbar()
        self.create_file_interaction_toolbar()

    def create_visibility_toolbar(self):
        tm = self._figure.canvas.manager.toolmanager

        group_name = "axis_visibility"

        for tool_name in visibility_tools_dict:
            tm.add_tool(tool_name, visibility_tools_dict[tool_name])
            self._figure.canvas.manager.toolbar.add_tool(tm.get_tool(tool_name), group_name)

    def create_file_interaction_toolbar(self):
        tm = self._figure.canvas.manager.toolmanager

        group_name = "file_interaction"

        for tool_name in file_interaction_tools_dict:
            tm.add_tool(tool_name, file_interaction_tools_dict[tool_name])
            self._figure.canvas.manager.toolbar.add_tool(tm.get_tool(tool_name), group_name)

    def remove_unnecessary_tools(self):
        self._figure.canvas.manager.toolmanager.remove_tool("subplots")
        self._figure.canvas.manager.toolmanager.remove_tool("help")

    @staticmethod
    def set_callback(key, func):
        if key in visibility_tools_dict or key in file_interaction_tools_dict:
            CALLBACK_DICT[key] = func


def test_func():
    print("Hi!")


def test_implementation():
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3], label="legend")
    ax.legend()

    c = ToolbarController(fig)
    c.set_callback(OpenFile.callback_key, test_func)

    plt.show()


if __name__ == '__main__':
    test_implementation()
