from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
import subprocess
import signal

class Home(QWidget):

    createGraphSignal = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.process = None
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.scanbtn = QPushButton("Start Scan")
        self.scanbtn.clicked.connect(self.startScan)
        self.mainLayout.addWidget(self.scanbtn)

        self.scanLabel = QLabel("No Active Scan")
        self.mainLayout.addWidget(self.scanLabel)

        self.stopbtn = QPushButton("Stop Scan")
        self.stopbtn.clicked.connect(self.stopScan)
        self.mainLayout.addWidget(self.stopbtn)

        self.gotoGraphbtn = QPushButton("Create Graph")
        self.gotoGraphbtn.clicked.connect(self.emitGraph)
        self.mainLayout.addWidget(self.gotoGraphbtn)

    def startScan(self):
        try:
            self.process = subprocess.Popen(["python", "../C++/serialLogger.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            self.scanLabel.setText("Scanning...")
        except:
            raise RuntimeError
        
    def stopScan(self):
        if self.process is None:
            return

        try:
            self.process.send_signal(signal.CTRL_BREAK_EVENT)
            self.process.wait(timeout=5)
        except Exception:
            self.process.kill()
        finally:
            self.process = None
            self.scanLabel.setText("Scan Completed")

    def emitGraph(self):
        self.createGraphSignal.emit()