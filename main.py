from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import socket

# pyqtgraphとpyqt6を用インストール、numpyも念の為


# サーバーIPとポート番号
IPADDR = "127.0.0.1"
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IPADDR, PORT))

n_samples = 5001
i = 0
num_list = np.ones(n_samples)
app = pg.mkQApp("Plotting Example")
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('pyqtgraph example: Plotting')
pg.setConfigOptions(antialias=True)
p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='y')


def update():
    global curve, p6, i
    msg = s.recv(1024).decode()
    i = i % n_samples
    num_list[i] = msg
    pos = i + 1 if i < n_samples else 0
    curve.setData(np.r_[num_list[pos:n_samples], num_list[0:pos]])
    print(i)
    i += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)


def main():
    pg.exec()


if __name__ == "__main__":
    main()
