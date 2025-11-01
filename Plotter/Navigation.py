from PyQt5.QtWidgets import QStackedWidget
from screens.home import Home
from screens.analyzedGraph import AnalyzedGraph
from screens.dataGraph import DataGraph

class NavigationController:
    def __init__(self):
        self.stack = QStackedWidget()
        self.screens = {}

        self.home = Home(self)
        self.home.createAnalyzedGraphSignal.connect(self.goToAnalyzedGraph)
        self.home.createDataGraphSignal.connect(self.goToDataGraph)

        self.addScreen("home", self.home)
        self.setCurrent("home") 
    
    def show(self):
        self.stack.setWindowTitle("Data Analyzer")
        self.stack.setGeometry(250,250,600,500)
        self.stack.show()

    def addScreen(self, name, widget):
        self.screens[name] = widget
        self.stack.addWidget(widget)

    def setCurrent(self, name):
        if name in self.screens:
            self.stack.setCurrentWidget(self.screens[name])
        else:
            raise ValueError(f"Screen {name} not found")
        
    def goToAnalyzedGraph(self):
        if "analyze" not in self.screens:
            self.analyze = AnalyzedGraph(self)
            self.analyze.goBackSignal.connect(self.goBackHome)
        self.addScreen("analyze", self.analyze)
        self.setCurrent("analyze")

    def goToDataGraph(self):
        if "data" not in self.screens:
            self.data = DataGraph(self)
            self.data.goBackSignal.connect(self.goBackHome)
        self.addScreen("data",self.data)
        self.setCurrent("data")

    def goBackHome(self):
        self.setCurrent("home")