from fft_tools import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import SpanSelector
import matplotlib

from tkinter import filedialog as fd
import tkinter as tk

matplotlib.use('TkAgg')

TIME_DATA_SAMPLE = np.arange(0.0, 5.0, 0.001)
X_DATA_SAMPLE = np.sin(100 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))
Y_DATA_SAMPLE = np.sin(350 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))
Z_DATA_SAMPLE = np.sin(134 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))


def select_file():
    filetypes = (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='.',
        filetypes=filetypes
    )

    return filename


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('FFT Analyzer')

        self.setup_menu_bar()

        self._time_data = TIME_DATA_SAMPLE
        self._raw_data = [X_DATA_SAMPLE, Y_DATA_SAMPLE, Z_DATA_SAMPLE]

        self._selected_time_data = self._time_data.copy()
        self._selected_data = self._raw_data.copy()

        self._figure = Figure(figsize=(6, 4), dpi=100)
        self._figure_canvas = FigureCanvasTkAgg(self._figure, self)
        NavigationToolbar2Tk(self._figure_canvas, self)

        self._axes_raw = self._figure.add_subplot(211)
        self._add_raw_axis_info()

        self._raw_lines = []
        for data in self._raw_data:
            line, = self._axes_raw.plot(self._time_data, data, linewidth=0.3)
            self._raw_lines.append(line)

        self._axes_fft = self._figure.add_subplot(212)
        self._add_fft_axis_info()

        self._fft_lines = []
        for data in self._selected_data:
            res_freq, res_fft = calculate_fft(data)
            line, = self._axes_fft.plot(res_freq, res_fft, linewidth=0.3)
            self._fft_lines.append(line)

        self._figure.tight_layout(pad=0.5)

        self._span = SpanSelector(self._axes_raw, self._on_select, 'horizontal', useblit=True,
                                  props=dict(alpha=0.5, facecolor='red'))

        self._figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def setup_menu_bar(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self._update_data_from_csv)
        file_menu.add_command(label="Exit", command=self.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def _update_data_from_csv(self):
        filename = select_file()

        if len(filename) == 0:
            return

        self._raw_data = get_3axis_raw_data(filename, remove_dc=True)
        self._selected_data = self._raw_data.copy()

        self._time_data = generate_time_array(self._raw_data[0])
        self._selected_time_data = self._time_data.copy()

        y_min = 0.0
        y_max = 0.0
        x_min = 0.0
        x_max = max(self._time_data)

        for data, line in zip(self._raw_data, self._raw_lines):
            line.set_data(self._time_data, data)

            if min(data) < y_min:
                y_min = min(data)

            if max(data) > y_max:
                y_max = max(data)

        self._axes_raw.set_xlim([x_min, x_max])
        self._axes_raw.set_ylim([y_min, y_max])

        self._update_fft()

    def _on_select(self, x_min, x_max):
        ind_min, ind_max = np.searchsorted(self._time_data, (x_min, x_max))
        ind_max = min(len(self._time_data) - 1, ind_max)

        self._selected_time_data = self._time_data[ind_min:ind_max]

        new_selected_data = []
        for data in self._raw_data:
            new_selected_data.append(data[ind_min:ind_max])

        self._selected_data = new_selected_data

        self._update_fft()

    def _update_fft(self):
        if len(self._selected_time_data) == 0:
            return

        max_magnitude = 0.0
        max_freq = 0.0
        for data, line in zip(self._selected_data, self._fft_lines):
            freq_trimmed, fft_trimmed = calculate_fft(data)
            line.set_data(freq_trimmed, fft_trimmed)

            if max(fft_trimmed) > max_magnitude:
                max_magnitude = max(fft_trimmed)

            if max(freq_trimmed) > max_freq:
                max_freq = max(freq_trimmed)

        self._axes_fft.set_xlim([0, max_freq])
        self._axes_fft.set_ylim([0, max_magnitude])

        self._figure.canvas.draw_idle()

    def _add_raw_axis_info(self):
        self._axes_raw.set_title("Select area of interest for FFT calculation")
        self._axes_raw.set_xlabel('time (s)')
        self._axes_raw.set_ylabel('magnitude (m/s^2)')

    def _add_fft_axis_info(self):
        self._axes_fft.set_xlabel('frequency (Hz)')
        self._axes_fft.set_ylabel('magnitude (m/s^2)')


if __name__ == '__main__':
    app = App()
    app.mainloop()
