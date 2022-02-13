"""
Basic wrapper for tkinter file dialog, simple dialog and messagebox
"""
import tkinter
from tkinter import filedialog as fd, simpledialog, messagebox


class UserCancelInput(Exception):
    pass


class InvalidDataSamplingPeriod(Exception):
    pass


class TkinterManager:
    def __init__(self):
        root = tkinter.Tk()
        root.withdraw()

    @staticmethod
    def select_file() -> str:
        filetypes = (
            ('csv files', '*.csv'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='.',
            filetypes=filetypes
        )

        if len(filename) == 0:
            raise UserCancelInput

        return filename

    @staticmethod
    def get_data_sampling_period() -> float:
        data_sampling_period = simpledialog.askfloat("Input", "What is your measurement sample period in second?")

        if data_sampling_period is None:
            raise UserCancelInput
        if data_sampling_period <= 0.0:
            messagebox.showerror("Error", "Please input positive value")
            raise InvalidDataSamplingPeriod

        return data_sampling_period
