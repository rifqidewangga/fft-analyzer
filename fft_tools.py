import numpy as np
from scipy.fftpack import fft, fftfreq


def get_3axis_raw_data(filename: str, remove_dc: bool = False) -> list:
    """
    Read 3 axis measurement data from CSV file and return it as tuple of (x, y, z).

    :param remove_dc:
    :param filename: name with csv extension (eg: sample.csv)
    :return:
    """
    x, y, z = np.loadtxt(filename, delimiter=",", unpack=True)

    if remove_dc:
        return [remove_dc_offset(x), remove_dc_offset(y), remove_dc_offset(z)]

    return [x, y, z]


def remove_dc_offset(data: np.ndarray):
    dc_offset = np.average(data)
    return data - dc_offset


def generate_time_array(data: np.ndarray, measurement_period: float = 0.001):
    n_data = len(data)
    end_time = n_data * measurement_period

    return np.arange(start=0, stop=end_time, step=measurement_period)


def calculate_fft(data: np.ndarray, measurement_period: float = 0.001):
    n_data = len(data)

    data_fft = fft(data)
    data_freq = fftfreq(n_data, measurement_period)[:n_data//2]
    data_fft_trimmed = 2.0/n_data * np.abs(data_fft[0:n_data//2])

    return np.array(data_freq), np.array(data_fft_trimmed)


def calculate_rms(data: np.ndarray) -> float:
    return np.sqrt(np.mean(data**2))


def calculate_resultant(x, y, z):
    resultant = []
    for (i, j, k) in zip(x, y, z):
        resultant.append(np.linalg.norm([i, j, k]))

    return np.array(resultant)
