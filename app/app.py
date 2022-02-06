from figure_manager import *


class App:
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
