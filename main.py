from tkinter import filedialog as fd, simpledialog

from matplotlib.widgets import SpanSelector

from fft_tools import calculate_fft, np, get_3axis_raw_data, generate_time_array
from toolbar_controller import *

TIME_DATA_SAMPLE = np.arange(0.0, 5.0, 0.001)
X_DATA_SAMPLE = np.sin(100 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))
Y_DATA_SAMPLE = np.sin(350 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))
Z_DATA_SAMPLE = np.sin(134 * np.pi * TIME_DATA_SAMPLE) + 0.5 * np.random.randn(len(TIME_DATA_SAMPLE))

AXIS_KEYS = ('x', 'y', 'z')

MEASUREMENT_PERIOD = 0.001
TIME_DATA = TIME_DATA_SAMPLE
RAW_DATA_DICT = {AXIS_KEYS[0]: X_DATA_SAMPLE,
                 AXIS_KEYS[1]: Y_DATA_SAMPLE,
                 AXIS_KEYS[2]: Z_DATA_SAMPLE}

FIG = plt.figure('FFT Analyzer')

SUBPLOT_RAW = FIG.add_subplot(211)
SUBPLOT_FFT = FIG.add_subplot(212)

RAW_LINES_DICT = {}
FFT_LINES_DICT = {}


def select_file():
    filetypes = (
        ('csv files', '*.csv'),
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='.',
        filetypes=filetypes
    )

    x, y, z = get_3axis_raw_data(filename, remove_dc=True)
    new_raw_data = [x, y, z]
    # prompt measurement period
    global MEASUREMENT_PERIOD
    MEASUREMENT_PERIOD = simpledialog.askfloat("Input", "What is your measurement sample period?")

    global TIME_DATA
    TIME_DATA = generate_time_array(np.array(x), measurement_period=MEASUREMENT_PERIOD)

    updated_raw_data_dict = {}
    for axis_key, data in zip(AXIS_KEYS, new_raw_data):
        updated_raw_data_dict[axis_key] = np.array(data)

    global RAW_DATA_DICT
    RAW_DATA_DICT.update(updated_raw_data_dict)

    update_raw_plot()
    update_fft_plot(0, -1)


def on_select(x_min, x_max):
    ind_min, ind_max = np.searchsorted(TIME_DATA, (x_min, x_max))
    ind_max = min(len(TIME_DATA) - 1, ind_max)

    if ind_max == ind_min:
        return

    update_fft_plot(ind_min, ind_max)


def update_raw_plot():
    for line_key, data_key in zip(RAW_LINES_DICT, RAW_DATA_DICT):
        line = RAW_LINES_DICT[line_key]
        data = RAW_DATA_DICT[data_key]

        line.set_data(TIME_DATA, data)

    FIG.canvas.draw_idle()


def update_fft_plot(ind_min, ind_max):
    for line_key, data_key in zip(FFT_LINES_DICT, RAW_DATA_DICT):
        line = FFT_LINES_DICT[line_key]
        data = RAW_DATA_DICT[data_key]

        selected_data = np.array(data[ind_min:ind_max])
        freq_trimmed, fft_trimmed = calculate_fft(selected_data, MEASUREMENT_PERIOD)
        line.set_data(freq_trimmed, fft_trimmed)

    FIG.canvas.draw_idle()


def apply_raw_lines_style():
    SUBPLOT_RAW.legend(loc='lower right')
    SUBPLOT_RAW.set_title(r'$Measurement Raw Data$')
    SUBPLOT_RAW.set_xlabel(r'$time\ (s)$')
    SUBPLOT_RAW.set_ylabel(r'$magnitude\ (m/s^{2})$')


def apply_fft_lines_style():
    SUBPLOT_FFT.legend(loc='lower right')
    SUBPLOT_FFT.set_title(r'$FFT$')
    SUBPLOT_FFT.set_xlabel(r'$frequency\ (Hz)$')
    SUBPLOT_FFT.set_ylabel(r'$magnitude\ (m/s^{2})$')


def create_fft_lines():
    for axis_key, data_key in zip(AXIS_KEYS, RAW_DATA_DICT):
        data = RAW_DATA_DICT[data_key]
        res_freq, res_fft = calculate_fft(data, MEASUREMENT_PERIOD)
        line, = SUBPLOT_FFT.plot(res_freq, res_fft, linewidth=0.3, label=axis_key)
        FFT_LINES_DICT[axis_key] = line


def create_raw_lines():
    for axis_key, data_key in zip(AXIS_KEYS, RAW_DATA_DICT):
        data = RAW_DATA_DICT[data_key]
        line, = SUBPLOT_RAW.plot(TIME_DATA, data, linewidth=0.3, label=axis_key)
        RAW_LINES_DICT[axis_key] = line


def toggle_line_visibility(key):
    raw_line = RAW_LINES_DICT[key]
    fft_line = FFT_LINES_DICT[key]

    raw_line.set_visible(not raw_line.get_visible())
    fft_line.set_visible(not fft_line.get_visible())

    FIG.canvas.draw_idle()


def create_callback(key):
    def callback():
        toggle_line_visibility(key)

    return callback


def main():
    create_raw_lines()
    apply_raw_lines_style()

    create_fft_lines()
    apply_fft_lines_style()

    FIG.tight_layout()

    span = SpanSelector(SUBPLOT_RAW, on_select, 'horizontal', useblit=True,
                        props=dict(alpha=0.5, facecolor='red'))

    c = ToolbarController(FIG)

    c.set_callback(OpenFile.callback_key, select_file)
    c.set_callback(ToggleXVisibility.callback_key, create_callback('x'))
    c.set_callback(ToggleYVisibility.callback_key, create_callback('y'))
    c.set_callback(ToggleZVisibility.callback_key, create_callback('z'))

    plt.show()


if __name__ == '__main__':
    main()
