from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial

# pyqtgraphとpyqt6を用インストール、numpyも念の為

ser = serial.Serial("COM3", 9600, 8, timeout=50*10**-3)
toSer = True
n_samples = 5001
i = 0
num_list = np.zeros(n_samples)
app = pg.mkQApp("Plotting Example")
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('show_wave_form')
pg.setConfigOptions(antialias=True)

p1 = win.addPlot(title="Voltage plot")
curve_1 = p1.plot(pen='y')
p1.setLimits(yMin=0.7, yMax=1.2, xMin=0, xMax=5000)
p1.setMouseEnabled(x=True, y=False)

p2 = win.addPlot(title="frequency plot")
curve_2 = p2.plot(pen='xy')
#p6.setLimits(yMin=0.7, yMax=1.2, xMin=0, xMax=5000)
p2.setMouseEnabled(x=False, y=False)


def update():
    global curve_1, i, toSer, ser, curve_2
    if not toSer:
        try:
            # シリアル
            ser = serial.Serial("COM3", 9600, 8, timeout=50*10**-3)
            toSer = True
        except:
            pass
    try:
        msg = ser.readline().decode()
    except:
        msg = "0"
        toSer = False

    if msg != '':
        i = i % n_samples
        num_list[i] = msg
        pos = i + 1 if i < n_samples else 0
        wave_date1 = np.r_[num_list[pos:n_samples], num_list[0:pos]]
        frequency, wave_amp = do_fft(wave_date1)
        curve_1.setData(wave_date1)
        curve_2.setData(x=frequency, y=wave_amp)
        i += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)


def main():
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
    if toSer:
        ser.close()


def do_fft(wave_date):
    sampling_cycle = 10*10**-3
    N = len(wave_date)
    fft_wave = np.fft.fft(wave_date)
    abs_fft_wave = np.abs(fft_wave)
    abs_fft_amp = abs_fft_amp / N * 2   # 交流成分
    abs_fft_amp[0] = abs_fft_amp[0] / 2       # 直流成分
    frequency = np.linspace(0, 1.0/sampling_cycle, N)

    return frequency, fft_wave


if __name__ == "__main__":
    main()
