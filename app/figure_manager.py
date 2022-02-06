from dataset import *
from toolbar_controller import *
from matplotlib.widgets import SpanSelector
from tkinter_manager import TkinterManager


class FigureManager:
    def __init__(self, figure_name: str, dataset: Dataset):
        self.dataset = dataset
        self.figure_name = figure_name

        self.figure = plt.figure(figure_name)

        self.toolbar_controller = ToolbarController(self.figure)
        self.set_toolbar_callback()

        self.subplot_raw = self.figure.add_subplot(211)
        self.subplot_fft = self.figure.add_subplot(212)

        self.raw_lines_dict = {key: self.create_line_raw_data(key)
                               for key in Axis}
        self.fft_lines_dict = {key: self.create_line_fft_data(key)
                               for key in Axis}

        self.apply_raw_lines_style()
        self.apply_fft_lines_style()
        self.figure.tight_layout()

        self.span = SpanSelector(self.subplot_raw, self.on_select, 'horizontal', useblit=True,
                                 props=dict(alpha=0.5, facecolor='red'))

    def set_toolbar_callback(self):
        OpenFile.callback = self.import_csv
        ToggleXVisibility.callback = self.create_callback(Axis.X)
        ToggleYVisibility.callback = self.create_callback(Axis.Y)
        ToggleZVisibility.callback = self.create_callback(Axis.Z)

    def create_line_raw_data(self, axis: Axis):
        time_data = self.dataset.get_time_data()
        data = self.dataset.get_measurement_raw_data(axis)

        sp = self.subplot_raw
        line, = sp.plot(time_data, data, linewidth=0.3, label=axis)

        return line

    def create_line_fft_data(self, axis: Axis):
        result = self.dataset.get_fft_data(axis)
        freq = result[FftData.FREQ]
        mag = result[FftData.MAG]

        sp = self.subplot_fft
        line, = sp.plot(freq, mag, linewidth=0.3, label=axis)

        return line

    def update_figure(self):
        self.update_raw_plot()
        self.update_fft_plot()

    def apply_raw_lines_style(self):
        self.subplot_raw.legend(loc='lower right')
        self.subplot_raw.set_title(r'$Measurement Raw Data$')
        self.subplot_raw.set_xlabel(r'$time\ (s)$')
        self.subplot_raw.set_ylabel(r'$magnitude\ (m/s^{2})$')

    def apply_fft_lines_style(self):
        self.subplot_fft.legend(loc='lower right')
        self.subplot_fft.set_title(r'$FFT$')
        self.subplot_fft.set_xlabel(r'$frequency\ (Hz)$')
        self.subplot_fft.set_ylabel(r'$magnitude\ (m/s^{2})$')

    def toggle_line_visibility(self, axis: Axis):
        print(axis)
        raw_line = self.raw_lines_dict[axis]
        fft_line = self.fft_lines_dict[axis]

        raw_line.set_visible(not raw_line.get_visible())
        fft_line.set_visible(not fft_line.get_visible())

        self.figure.canvas.draw_idle()

    def create_callback(self, axis: Axis):
        def func():
            self.toggle_line_visibility(axis)

        return func

    def on_select(self, x_min, x_max):
        time_data = self.dataset.get_time_data()
        ind_min, ind_max = np.searchsorted(time_data, (x_min, x_max))
        ind_max = min(len(time_data) - 1, ind_max)

        if ind_max == ind_min:
            return

        self.update_fft_plot(ind_min, ind_max)

    def update_raw_plot(self):
        for axis in Axis:
            time_data = self.dataset.get_time_data()
            data = self.dataset.get_measurement_raw_data(axis)
            line = self.raw_lines_dict[axis]
            line.set_data(time_data, data)

        self.subplot_raw.relim()
        self.subplot_raw.autoscale_view(True, True, True)
        self.figure.canvas.draw_idle()

    def update_fft_plot(self, i_min: int = 0, i_max: int = -1):
        for axis in Axis:
            result = self.dataset.get_fft_data(axis, i_min, i_max)
            freq = result[FftData.FREQ]
            mag = result[FftData.MAG]

            line = self.fft_lines_dict[axis]
            line.set_data(freq, mag)

        self.subplot_fft.relim()
        self.subplot_fft.autoscale_view(True, True, True)
        self.figure.canvas.draw_idle()

    def import_csv(self):
        data_sampling_period = TkinterManager.get_data_sampling_period()
        filename = TkinterManager.select_file()
        if len(filename) == 0:
            return

        self.dataset.update_data(filename, data_sampling_period)
        self.update_figure()

    @staticmethod
    def show():
        plt.show()
