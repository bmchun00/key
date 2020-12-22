from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        N = 5
        value = (20, 35, 30, 35, 27)
        ind = np.arange(N)
        width = 0.35
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        ax.bar(ind, value, width)
        ax.set_xticks(ind + width / 20)
        ax.set_xticklabels(['G1', 'G2', 'G3', 'G4', 'G5'])
        canvas = FigureCanvas(fig)
        canvas.draw()
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(canvas)
        canvas.show()