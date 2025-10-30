from PyQt5.QtWidgets import QStackedWidget
from screens.home import Home
from screens.graph import Graph

class NavigationController:
    def __init__(self):
        self.stack = QStackedWidget()
        self.screens = {}

        self.home = Home(self)
        self.home.createGraphSignal.connect(self.goToGraph)

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
        
    def goToGraph(self):
        if "graph" not in self.screens:
            self.graph = Graph(self)
            self.graph.goBackSignal.connect(self.goBackHome)
        self.addScreen("graph", self.graph)
        self.setCurrent("graph")

    def goBackHome(self):
        self.setCurrent("home")