"""
Module for calculating fft based on raw data and sampling period
This module also contains some helper function to remove DC offset and generate time series data
"""
import numpy as np
from scipy.fftpack import fft, fftfreq


def get_3axis_raw_data(filename: str, remove_dc: bool = False) -> list:
    """
    Read 3 axis measurement data from CSV file and return it as tuple of (x, y, z).
    :param filename: name with csv extension (eg: sample.csv)
    :param remove_dc: enable auto remove dc offset
    :return: list of raw data measurement with or without dc offset
    """
    x, y, z = np.loadtxt(filename, delimiter=",", unpack=True)

    if remove_dc:
        return [remove_dc_offset(x), remove_dc_offset(y), remove_dc_offset(z)]

    return [x, y, z]


def remove_dc_offset(data: np.ndarray) -> np.ndarray:
    """
    Removing dc offset from single axis dataset
    :param data: single axis numpy array
    :return: data with dc offset removed
    """
    dc_offset = np.average(data)
    return data - dc_offset


def generate_time_array(data: np.ndarray, data_sampling_period: float = 0.001) -> np.ndarray:
    """
    Generate time series data based on length of raw measurement data and sampling period
    :param data: single axis raw measurement data
    :param data_sampling_period: in seconds
    :return: numpy array of time series
    """
    n_data = len(data)
    end_time = (n_data - 1) * data_sampling_period

    return np.linspace(start=0, stop=end_time, num=n_data)


def calculate_fft(data: np.ndarray, data_sampling_period: float = 0.001) -> tuple:
    """
    Calculate fft from single axis numpy array
    :param data: single axis raw measurement data
    :param data_sampling_period: in seconds
    :return: tuple of frequency and magnitude
    """
    n_data = len(data)

    data_fft = fft(data)
    data_freq = fftfreq(n_data, data_sampling_period)[:n_data // 2]
    data_fft_trimmed = 2.0/n_data * np.abs(data_fft[0:n_data//2])

    return np.array(data_freq), np.array(data_fft_trimmed)


def calculate_rms(data: np.ndarray) -> float:
    """
    Calculate root mean squares of single axis dataset
    :param data: numpy array of single axis measurement
    :return: root-mean-square
    """
    return np.sqrt(np.mean(data**2))


def calculate_resultant(x, y, z):
    """
    Calculate resultant of 3 dimensions vector
    :param x: vector x
    :param y: vector y
    :param z: vector z
    :return: resultant
    """
    resultant = []
    for (i, j, k) in zip(x, y, z):
        resultant.append(np.linalg.norm([i, j, k]))

    return np.array(resultant)
