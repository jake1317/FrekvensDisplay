from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QCheckBox, QGridLayout
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Frekvens Visualizer")

        layout = QGridLayout()

        for y in range(16):
            for x in range(16):
                layout.addWidget(QCheckBox(), (15-x), y)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
