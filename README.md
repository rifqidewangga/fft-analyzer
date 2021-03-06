# FFT Analyzer
Simple desktop application that will take csv data from 3 axis vibration measurement and plot fft. User can select area of interest within data for fft calculation. This app used matplotlib, tkinter and scipy.

## How To Run Application on Linux
1. Download fft-analyzer-x.y.z from release page and copy it to any directory you want
2. Enter following command on your terminal to add execution permission to the file (make sure you are in the same directory as the executable)
```bash
chmod +x fft-analyzer-x.y.z
./fft-analyzer-x.y.z
```
3. You should get a new window with default view and dataset as follows
 
![lt text](docs/images/fft-analyzer-default-window.png)


## How To Run Application on Any Machine
1. Make sure you have python 3.8 or later installed
2. Install all dependencies using pip by entering following command
```bash
pip3 install -r requirements.txt
```
3. Run app.py
```bash
python3 app.py
```

## Features
### Toggling plot Visibility
![lt text](docs/images/fft-analyzer-toggle-visibility.gif)
### Calculate FFT From Area of Interest
![lt text](docs/images/fft-analyzer-calculate-fft.gif)<br /> 
By default fft plot is calculated based on all data from dataset. You can calculate fft based on certain area on raw data measurement by selecting it on raw data plot area. This can be useful if you have continuous raw data from different operation, and you need to analyze each section independently.
### Importing CSV Data 
![lt text](docs/images/fft-analyzer-import-csv.gif)<br />
CSV data should have 3 column, and the columns should be sorted from X to Z axis. Measurement period should match data acquisition sampling period.
