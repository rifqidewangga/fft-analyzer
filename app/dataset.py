"""
Provide a container for dataset and fft operation on dataset.
UI module can ask for a pair of x and y value for plotting.
"""
from enum import Enum, auto
from fft_tools import *


class Axis(Enum):
    """Plot axis enum"""
    X = auto()
    Y = auto()
    Z = auto()


class FftData(Enum):
    """FFT data enum for accessing dictionary from calculate_fft"""
    FREQ = auto()
    MAG = auto()


class Dataset:
    """
    Class for storing measurement data in 3 axes and perform FFT operation on it
    """
    def __init__(self, data_sampling_period: float = 0.001, file_name: str = None) -> None:
        if file_name is not None:
            pass

        self.data_sampling_period = data_sampling_period
        self.time_data = np.arange(0.0, 5.0, self.data_sampling_period)
        self.measurement_raw_data_dict = self.generate_sample_data(self.time_data)

    @staticmethod
    def generate_sample_data(time_data: np.ndarray) -> dict:
        """
        Populate dataset with sample data for default view of apps
        :param time_data: time series data
        :return: dictionary of 3 axis sample data
        """
        sample_data_dict = {
            Axis.X: np.sin(100 * np.pi * time_data) + 0.5 * np.random.randn(len(time_data)),
            Axis.Y: np.sin(350 * np.pi * time_data) + 0.5 * np.random.randn(len(time_data)),
            Axis.Z: np.sin(134 * np.pi * time_data) + 0.5 * np.random.randn(len(time_data))
        }
        return sample_data_dict

    def get_time_data(self) -> np.ndarray:
        """
        Get time series data from raw measurement data.
        This time series is created based on measurement sampling period
        :return: numpy array
        """
        return self.time_data

    def get_measurement_raw_data(self, axis: Axis) -> np.ndarray:
        """
        Get single axis of measurement raw data
        :param axis: data axis (e.g x, y, or z)
        :return: numpy array
        """
        return self.measurement_raw_data_dict[axis]

    def get_fft_data(self, axis: Axis, index_min: int = 0, index_max: int = -1) -> dict:
        """
        Calculate fft from dataset and returning it as dictionary of fft data.
        :param axis: axis of dataset (e.g. x, y, z)
        :param index_min: start of dataset for fft calculation
        :param index_max: end of dataset for fft calculation
        :return: dictionary of fft result magnitude and frequency
        """
        selected_data = self.get_measurement_raw_data(axis)[index_min:index_max]
        result = calculate_fft(selected_data, self.data_sampling_period)

        return {key: data for key, data in zip(FftData, result)}

    def update_data(self, filename: str, data_sampling_period: float) -> None:
        """
        update internal dataset from a csv file
        :param filename: fullpath to csv file
        :param data_sampling_period: in seconds
        :return: None
        """
        raw_data = get_3axis_raw_data(filename, remove_dc=True)

        raw_data_dict = {key: data for key, data in zip(Axis, raw_data)}

        self.data_sampling_period = data_sampling_period
        self.measurement_raw_data_dict.update(raw_data_dict)
        self.time_data = generate_time_array(self.get_measurement_raw_data(Axis.X),
                                             self.data_sampling_period)
