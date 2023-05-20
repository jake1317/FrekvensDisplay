from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QCheckBox, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.xDim = 16
        self.yDim = 16

        self.setWindowTitle("Frekvens Visualizer")

        self.mainLayout = QVBoxLayout()

        self.initGrid()
        self.initButtons()
        self.initOutput()

        mainWidget = QWidget()
        mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(mainWidget)

    def initGrid(self):
        grid = QGridLayout()

        self.theCheckBoxes = [[QCheckBox() for y in range(self.yDim)] for x in range(self.xDim)]
        self.theCheckBoxValues = [[False for y in range(self.yDim)] for x in range(self.xDim)]
        for y in range(self.yDim):
            for x in range(self.xDim):
                grid.addWidget(self.theCheckBoxes[x][y], (self.xDim-1-x), y)
                self.theCheckBoxes[x][y].stateChanged.connect(lambda i, x=x, y=y: self.boxChanged(i, x, y))


        gridWidget = QWidget()
        gridWidget.setLayout(grid)

        self.mainLayout.addWidget(gridWidget)

    def initButtons(self):
        buttonLayout = QHBoxLayout()
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearAll)
        self.setButton = QPushButton("Set")
        self.setButton.clicked.connect(self.setAll)
        self.outputTextButton = QPushButton("Pull")
        self.outputBoxesButton = QPushButton("Push")
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addWidget(self.setButton)
        buttonLayout.addWidget(self.outputTextButton)
        buttonLayout.addWidget(self.outputBoxesButton)
        buttonWidget = QWidget()
        buttonWidget.setLayout(buttonLayout)
        self.mainLayout.addWidget(buttonWidget)

    def initOutput(self):
        self.textBox = QLineEdit()
        self.outputTextButton.clicked.connect(lambda x: self.textBox.setText(str(self.getCheckBoxState())))
        self.outputBoxesButton.clicked.connect(lambda x: self.setCheckBoxStateStr(self.textBox.text()))
        self.mainLayout.addWidget(self.textBox)

    def getCheckBoxState(self):
        output = []
        for y in range(self.yDim):
            row = 0x0
            for x in range(self.xDim):
                if self.theCheckBoxValues[y][x]:
                    row |= 1 << x
            output.append(row)
        return output

    def setCheckBoxStateStr(self, txt):
        myTxt = txt.replace(" ", "")
        print(myTxt)
        if myTxt[0] != '[' or myTxt[-1] != ']':
            raise Exception("Incorrectly formatted string!")

        myList = [int(spl) for spl in myTxt[1:-1].split(',')]
        for y in range(self.yDim):
            row = myList[y]
            for x in range(self.xDim):
                self.setCheckBox(y, x, row & 0x1)
                row = row >> 1

    def boxChanged(self, int, x, y):
        self.theCheckBoxValues[x][y] = self.theCheckBoxes[x][y].isChecked()

    def clearAll(self, int):
        for y in range(self.yDim):
            for x in range(self.xDim):
                self.setCheckBox(x,y,False)

    def setAll(self, int):
        for y in range(self.yDim):
            for x in range(self.xDim):
                self.setCheckBox(x,y,True)

    def setCheckBox(self, x, y, value):
        self.theCheckBoxes[x][y].setChecked(value)
        self.theCheckBoxValues[x][y] = value

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
