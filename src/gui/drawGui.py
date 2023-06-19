from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QCheckBox, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QSpacerItem
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self, xDim, yDim):
        super().__init__()
        self.xDim = xDim
        self.yDim = yDim
        self.paintMode = False
        self.eraseMode = False
        self.dragging = False

        self.mainLayout = QVBoxLayout()

        self.initGrid()
        self.initButtons()
        self.initOutput()

        mainWidget = QWidget()
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)
        self.setWindowTitle("Frekvens Visualizer")

    def initGrid(self):
        hbox = QHBoxLayout()
        grid = QGridLayout()

        self.theCheckBoxes = [[QCheckBox() for x in range(self.xDim)] for y in range(self.yDim)]
        self.theCheckBoxValues = [[False for x in range(self.xDim)] for y in range(self.yDim)]
        for y in range(self.yDim):
            for x in range(self.xDim):
                grid.addWidget(self.theCheckBoxes[y][x], (self.yDim-1-y), x)
                self.theCheckBoxes[y][x].stateChanged.connect(lambda i, x=x, y=y: self.boxChanged(i, x, y))
                self.theCheckBoxes[y][x].enterEvent = lambda i, x=x, y=y: self.onEnter(i, x, y)
                self.theCheckBoxes[y][x].mousePressEvent = lambda i, x=x, y=y: self.onPressed(i, x, y)

        gridWidget = QWidget()
        gridWidget.setLayout(grid)
        spacing = max((17 - self.xDim) * 10, 0)
        hbox.addSpacing(spacing)
        hbox.addWidget(gridWidget)
        hbox.addSpacing(spacing)
        hboxWidget = QWidget()
        hboxWidget.setLayout(hbox)

        self.mainLayout.addWidget(hboxWidget)

    def onEnter(self, int, x, y):
        if self.dragging:
            if self.paintMode:
                self.setCheckBox(x, y, True)
            elif self.eraseMode:
                self.setCheckBox(x, y, False)

    def onPressed(self, int, x, y):
        newState = not self.theCheckBoxes[y][x].isChecked()
        if self.dragging:
            if self.paintMode:
                newState = True
            elif self.eraseMode:
                newState = False
        self.dragging = not self.dragging
        self.setCheckBox(x, y, newState)

    def initButtons(self):
        buttonLayout1 = QHBoxLayout()
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearAll)
        self.setButton = QPushButton("Set")
        self.setButton.clicked.connect(self.setAll)
        self.outputTextButton = QPushButton("Pull")
        self.outputBoxesButton = QPushButton("Push")
        buttonLayout1.addWidget(self.clearButton)
        buttonLayout1.addWidget(self.setButton)
        buttonLayout1.addWidget(self.outputTextButton)
        buttonLayout1.addWidget(self.outputBoxesButton)
        buttonWidget1 = QWidget()
        buttonWidget1.setLayout(buttonLayout1)
        self.mainLayout.addWidget(buttonWidget1)
        buttonLayout2 = QHBoxLayout()
        self.paintModeButton = QPushButton("paintMode")
        self.eraseModeButton = QPushButton("eraseMode")
        self.paintModeButton.clicked.connect(self.paintModeClick)
        self.paintModeButton.setCheckable(True)
        self.eraseModeButton.clicked.connect(self.eraseModeClick)
        self.eraseModeButton.setCheckable(True)
        buttonLayout2.addWidget(self.paintModeButton)
        buttonLayout2.addWidget(self.eraseModeButton)
        buttonWidget2 = QWidget()
        buttonWidget2.setLayout(buttonLayout2)
        self.mainLayout.addWidget(buttonWidget2)

    def paintModeClick(self):
        self.paintMode = not self.paintMode
        self.dragging = False
        if self.eraseMode:
            self.eraseMode = False
            self.eraseModeButton.setChecked(False)

    def eraseModeClick(self):
        self.eraseMode = not self.eraseMode
        self.dragging = False
        if self.paintMode:
            self.paintMode = False
            self.paintModeButton.setChecked(False)

    def initOutput(self):
        self.textBox = QLineEdit()
        self.outputTextButton.clicked.connect(lambda x: self.textBox.setText(self.getCheckBoxStr()))
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

    def getCheckBoxStr(self):
        return '[{}]'.format(', '.join(str(x) for x in self.getCheckBoxState()))

    def setCheckBoxStateStr(self, txt):
        myTxt = txt.replace(" ", "")
        if myTxt[0] != '[' or myTxt[-1] != ']':
            raise Exception("Incorrectly formatted string!")

        myList = [int(spl, 0) for spl in myTxt[1:-1].split(',')]
        for y in range(self.yDim):
            row = myList[y]
            for x in range(self.xDim):
                self.setCheckBox(x, y, row & 0x1)
                row = row >> 1

    def boxChanged(self, int, x, y):
        if self.dragging:
            if self.paintMode:
                self.setCheckBox(x, y, True)
            elif self.eraseMode:
                self.setCheckBox(x, y, False)
        self.theCheckBoxValues[y][x] = self.theCheckBoxes[y][x].isChecked()

    def clearAll(self, int):
        for y in range(self.yDim):
            for x in range(self.xDim):
                self.setCheckBox(x,y,False)

    def setAll(self, int):
        for y in range(self.yDim):
            for x in range(self.xDim):
                self.setCheckBox(x,y,True)

    def setCheckBox(self, x, y, value):
        self.theCheckBoxes[y][x].setChecked(value)
        self.theCheckBoxValues[y][x] = value

xDim = 16
yDim = 16
if (len(sys.argv) >= 3):
    xDim = int(sys.argv[1])
    yDim = int(sys.argv[2])
app = QApplication([])
window = MainWindow(xDim, yDim)
window.show()
app.exec()
