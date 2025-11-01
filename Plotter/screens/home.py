from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
import subprocess
import os, time

class Home(QWidget):

    createAnalyzedGraphSignal = pyqtSignal()
    createDataGraphSignal = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.process = None
        self.failed = False
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.scanLabel = QLabel("No Active Scan")
        self.scanLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.scanLabel)

        self.scanbtn = QPushButton("Start Scan")
        self.scanbtn.clicked.connect(self.startScan)
        self.mainLayout.addWidget(self.scanbtn)

        self.stopbtn = QPushButton("Stop Scan")
        self.stopbtn.clicked.connect(self.stopScan)
        self.stopbtn.setEnabled(False)
        self.mainLayout.addWidget(self.stopbtn)

        self.gotoAnalyzebtn = QPushButton("Create Analyzed Graph")
        self.gotoAnalyzebtn.clicked.connect(self.emitAnalyzedGraph)
        self.mainLayout.addWidget(self.gotoAnalyzebtn)

        self.gotoDatabtn = QPushButton("Create Data Graph")
        self.gotoDatabtn.clicked.connect(self.emitAnalyzedGraph)
        self.mainLayout.addWidget(self.gotoDatabtn)

        self.quitbtn = QPushButton("Quit")
        self.quitbtn.clicked.connect(QApplication.quit)
        self.mainLayout.addWidget(self.quitbtn)

    def startScan(self):
        self.failed = False
        self.scanLabel.setText("Starting...")
        currentDir = os.path.dirname(os.path.realpath(__file__))

        parentDir = os.path.abspath(os.path.join(currentDir, "..", ".."))

        self.stopFile = os.path.join(parentDir, "C++", "stop.flag")
        os.makedirs(os.path.dirname(self.stopFile), exist_ok=True)

        if os.path.exists(self.stopFile):
            os.remove(self.stopFile)

        self.process = subprocess.Popen(["python","-u","../C++/serialLogger.py"], 
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, 
                                        bufsize=1,
                                        universal_newlines=True)

        self.stopbtn.setEnabled(False)
        self.scanbtn.setEnabled(False)
        self.gotoAnalyzebtn.setEnabled(False)
        self.gotoDatabtn.setEnabled(False)
        self.quitbtn.setEnabled(False)

        while True:
            line = self.process.stdout.readline()
            if not line:
                time.sleep(0.01)
                continue
            line = line.strip()
            if "INIT_OK" in line:
                self.scanLabel.setText("Scanning...")
                self.stopbtn.setEnabled(True)
                break
            elif "SERIAL_FAIL" in line:
                self.scanLabel.setText("Serial Fail")
                self.failed = True
                self.process.kill()
                self.process = None
                self.scanbtn.setEnabled(True)
                self.quitbtn.setEnabled(True)
                self.gotoAnalyzebtn.setEnabled(True)
                self.gotoDatabtn.setEnabled(True)
                return
            
    def check_process(self):
        if self.process.poll() is not None: 
            self.scanLabel.setText("Scan Completed")
            self.scanbtn.setEnabled(True)
            self.gotoAnalyzebtn.setEnabled(True)
            self.gotoDatabtn.setEnabled(True)
            self.quitbtn.setEnabled(True)
            self.process = None
            self.timer.stop()

    def stopScan(self):
        if not self.process:
            return
        with open(self.stopFile, "w") as f:
            f.write("stop")

        self.scanLabel.setText("Stopping...")
        self.stopbtn.setEnabled(False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_process)
        self.timer.start(100)

    def emitAnalyzedGraph(self):
        self.createAnalyzedGraphSignal.emit()