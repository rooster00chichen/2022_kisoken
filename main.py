from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial

# pyqtgraphとpyqt6を用インストール、numpyも念の為

ser = serial.Serial("COM3", 9600, 8, timeout=50*10**-3)
toSer=True
n_samples = 5001
i = 0
num_list = np.zeros(n_samples)
app = pg.mkQApp("Plotting Example")
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('show_wave_form')
pg.setConfigOptions(antialias=True)
p6 = win.addPlot(title="Voltage plot")
curve = p6.plot(pen='y')
p6.setLimits(yMin=0.7,yMax=1.2,xMin=0,xMax=5000)
p6.setYRange(0.7,1.2)
p6.setMouseEnabled(x=True, y=False)


def update():
    global curve, p6, i,toSer,ser
    if not toSer:
        try:
            # シリアル
            ser = serial.Serial("COM3", 9600, 8, timeout=50*10**-3)
            toSer=True
        except:
            pass
    try:
        msg = ser.readline().decode()
    except:
        msg = "0"
        toSer=False

    if msg!='':
        i = i % n_samples
        num_list[i] = msg
        pos = i + 1 if i < n_samples else 0
        curve.setData(np.r_[num_list[pos:n_samples], num_list[0:pos]])
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


if __name__ == "__main__":
    main()
