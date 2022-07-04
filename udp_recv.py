from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import socket

# pyqtgraphとpyqt6を用インストール、numpyも念の為


# サーバーIPとポート番号
IPADDR = "127.0.0.1"
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(10*10**-3)
s.bind((IPADDR, PORT))

n_samples = 5001
i = 0
num_list = np.zeros(n_samples)
app = pg.mkQApp("Plotting Example")
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('pyqtgraph example: Plotting')
pg.setConfigOptions(antialias=True)

p1 = win.addPlot(title="Voltage plot")
curve_1 = p1.plot(pen='y')
p1.setLimits(yMin=0.7, yMax=1.2, xMin=0, xMax=5000)
p1.setMouseEnabled(x=True, y=False)

p2 = win.addPlot(title="frequency plot")
curve_2 = p2.plot(pen='r')
p2.setMouseEnabled(x=True, y=False)


def update():
    global curve_1, i, toSer, ser, curve_2

    try:
        msg = s.recv(1024).decode()
    except socket.timeout:
        msg = '0'

    if msg != '':
        i = i % n_samples
        num_list[i] = msg
        pos = i + 1 if i < n_samples else 0
        wave_date1 = np.r_[num_list[pos:n_samples], num_list[0:pos]]
        frequency, wave_amp = do_fft(wave_date1)
        curve_1.setData(wave_date1)
        curve_2.setData(frequency, wave_amp)
        i += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)


def main():
    pg.exec()


def do_fft(wave_date):
    sampling_cycle = 10*10**-3
    N = len(wave_date)
    fft_wave = np.fft.fft(wave_date)
    abs_fft_wave = np.abs(fft_wave)
    abs_fft_wave = abs_fft_wave / N * 2   # 交流成分
    abs_fft_wave[0] = abs_fft_wave[0] / 2       # 直流成分
    frequency = np.linspace(0, 1.0/sampling_cycle, N)

    return frequency, abs_fft_wave


if __name__ == "__main__":
    main()
