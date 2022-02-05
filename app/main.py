import tkinter
from tkinter import filedialog as fd, simpledialog, messagebox

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
    root = tkinter.Tk()
    root.withdraw()

    filetypes = (
        ('csv files', '*.csv'),
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='.',
        filetypes=filetypes
    )

    return filename


def import_csv():
    user_input = simpledialog.askfloat("Input", "What is your measurement sample period in second?")

    if user_input is None:
        return
    if user_input <= 0.0:
        messagebox.showerror("Error", "Please input positive value")
        return

    filename = select_file()
    if len(filename) == 0:
        return

    try:
        x, y, z = get_3axis_raw_data(filename, remove_dc=True)
        new_raw_data = [x, y, z]

        updated_raw_data_dict = {}
        for axis_key, data in zip(AXIS_KEYS, new_raw_data):
            updated_raw_data_dict[axis_key] = np.array(data)

        global MEASUREMENT_PERIOD
        MEASUREMENT_PERIOD = user_input

        global TIME_DATA
        TIME_DATA = generate_time_array(np.array(x), measurement_period=MEASUREMENT_PERIOD)

        global RAW_DATA_DICT
        RAW_DATA_DICT.update(updated_raw_data_dict)

        update_raw_plot()
        update_fft_plot(0, -1)

    except ValueError:
        messagebox.showerror("Error", "Please check your input, discrepancy in data count between axes")


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

    SUBPLOT_RAW.relim()
    SUBPLOT_RAW.autoscale_view(True, True, True)

    FIG.canvas.draw_idle()


def update_fft_plot(ind_min: int = 0, ind_max: int = -1):
    for line_key, data_key in zip(FFT_LINES_DICT, RAW_DATA_DICT):
        line = FFT_LINES_DICT[line_key]
        data = RAW_DATA_DICT[data_key]

        selected_data = np.array(data[ind_min:ind_max])
        freq_trimmed, fft_trimmed = calculate_fft(selected_data, MEASUREMENT_PERIOD)
        line.set_data(freq_trimmed, fft_trimmed)

    SUBPLOT_FFT.relim()
    SUBPLOT_FFT.autoscale_view(True, True, True)

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
    root = tkinter.Tk()
    root.withdraw()

    create_raw_lines()
    apply_raw_lines_style()

    create_fft_lines()
    apply_fft_lines_style()

    FIG.tight_layout()

    span = SpanSelector(SUBPLOT_RAW, on_select, 'horizontal', useblit=True,
                        props=dict(alpha=0.5, facecolor='red'))

    c = ToolbarController(FIG)

    c.set_callback(OpenFile.callback_key, import_csv)
    c.set_callback(ToggleXVisibility.callback_key, create_callback('x'))
    c.set_callback(ToggleYVisibility.callback_key, create_callback('y'))
    c.set_callback(ToggleZVisibility.callback_key, create_callback('z'))

    plt.show()

    root.destroy()


if __name__ == '__main__':
    main()
