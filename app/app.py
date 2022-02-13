"""
Main fft processor app
"""
from figure_manager import FigureManager
from dataset import Dataset


class App:
    """
    App class for instantiating FigureManager and Dataset
    """
    def __init__(self, name: str = "My App"):
        self.dataset = Dataset()
        self.figure_manager = FigureManager(name, self.dataset)

    def run(self):
        self.figure_manager.show()


def main():
    app = App("FFT Analyzer")
    app.run()


if __name__ == '__main__':
    main()
