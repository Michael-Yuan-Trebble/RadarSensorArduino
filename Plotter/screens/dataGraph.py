from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas
import os

class DataGraph(QWidget):

    goBackSignal = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.dataFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../C++/data"))
        self.dataFile = None
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.mainLayout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("No Plot Selected")

        self.stylePlot()

        self.canvas.draw()

        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.onItemClicked)
        self.mainLayout.addWidget(self.listWidget)

        self.goBackbtn = QPushButton("Go Back")
        self.goBackbtn.clicked.connect(self.goBackSignal.emit)
        self.mainLayout.addWidget(self.goBackbtn)
        self.loadFiles()

    def stylePlot(self):
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Distance (cm)")
        self.ax.set_ylim(0,100)
        self.figure.set_facecolor("#1e1e1e")
        self.ax.set_facecolor("#1e1e1e")
        self.ax.xaxis.label.set_color("white")
        self.ax.yaxis.label.set_color("white")
        self.ax.title.set_color("white")
        self.ax.tick_params(axis='both', colors='white')
        for spine in self.ax.spines.values():
            spine.set_color("white")
        self.ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.4)

    def loadFiles(self):
        self.listWidget.clear()
        for fileName in os.listdir(self.dataFolder):
            if fileName.lower().endswith(".csv"):
                self.listWidget.addItem(fileName)

    def onItemClicked(self,item):
        self.ax.cla()
        self.stylePlot()
        self.dataFile = os.path.join(self.dataFolder,item.text())
        self.ax.set_title(item.text())
        df = pandas.read_csv(self.dataFile)
        
        for _, row in df.iterrows():
            time = row['time(s)']
            distance = row['distance(cm)']
            self.ax.scatter(time,distance,color='red',s=50)

        df = pandas.read_csv(self.dataFile)
        self.canvas.draw()
