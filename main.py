from tkinter import filedialog as fd

from matplotlib.widgets import SpanSelector

from fft_tools import calculate_fft, np
from toolbar_controller import *

TIME_DATA_SAMPLE = np.arange(0.0, 5.0, 0.001)
X_DATA_SAMPLE = np.sin(100 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))
Y_DATA_SAMPLE = np.sin(350 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))
Z_DATA_SAMPLE = np.sin(134 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))

AXIS_LABELS = ('x', 'y', 'z')

time_data = TIME_DATA_SAMPLE
raw_data = [X_DATA_SAMPLE, Y_DATA_SAMPLE, Z_DATA_SAMPLE]

fig = plt.figure('FFT Analyzer')

axes_raw = fig.add_subplot(211)
axes_fft = fig.add_subplot(212)

raw_lines_dict = {}
fft_lines_dict = {}


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


def on_select(x_min, x_max):
    ind_min, ind_max = np.searchsorted(time_data, (x_min, x_max))
    ind_max = min(len(time_data) - 1, ind_max)

    if ind_max == ind_min:
        return

    update_fft_plot(ind_min, ind_max)


def update_fft_plot(ind_min, ind_max):
    for key, data in zip(fft_lines_dict, raw_data):
        selected_data = np.array(data[ind_min:ind_max])
        freq_trimmed, fft_trimmed = calculate_fft(selected_data)
        line = fft_lines_dict[key]
        line.set_data(freq_trimmed, fft_trimmed)

    fig.canvas.draw_idle()


def apply_raw_lines_style():
    axes_raw.legend(loc='lower right')


def apply_fft_lines_style():
    axes_fft.legend(loc='lower right')


def create_fft_lines():
    for key, data, label in zip(AXIS_LABELS, raw_data, AXIS_LABELS):
        res_freq, res_fft = calculate_fft(data)
        line, = axes_fft.plot(res_freq, res_fft, linewidth=0.3, label=label)
        fft_lines_dict[key] = line


def create_raw_lines():
    for key, data, label in zip(AXIS_LABELS, raw_data, AXIS_LABELS):
        line, = axes_raw.plot(time_data, data, linewidth=0.3, label=label, )
        raw_lines_dict[key] = line


def toggle_line_visibility(key):
    raw_line = raw_lines_dict[key]
    fft_line = fft_lines_dict[key]

    raw_line.set_visible(not raw_line.get_visible())
    fft_line.set_visible(not fft_line.get_visible())

    fig.canvas.draw_idle()


def create_callback(key):
    def callback():
        toggle_line_visibility(key)

    return callback


def main():
    create_raw_lines()
    apply_raw_lines_style()

    create_fft_lines()
    apply_fft_lines_style()

    span = SpanSelector(axes_raw, on_select, 'horizontal', useblit=True,
                        props=dict(alpha=0.5, facecolor='red'))

    c = ToolbarController(fig)

    c.set_callback(OpenFile.callback_key, select_file)
    c.set_callback(ToggleXVisibility.callback_key, create_callback('x'))
    c.set_callback(ToggleYVisibility.callback_key, create_callback('y'))
    c.set_callback(ToggleZVisibility.callback_key, create_callback('z'))

    plt.show()


if __name__ == '__main__':
    main()
