import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QMessageBox, QComboBox, QLabel, QGridLayout

class UpdateGui (QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.setStyleSheet("""
            QComboBox[Test=true] {
                border: 2px solid #000000;
                background-color: #bbe6ff;
                color: #790000;
            }
        """)

        self.initUi()

    def initUi(self):

        dht_label = QLabel('DHT Interval:')
        self.dht_value = QLabel('1')
        probe_label = QLabel('Temp Probe Interval: ')
        self.probe_value = QLabel('1')
        curr_label = QLabel('Current Interval: ')
        self.curr_value = QLabel('1')

        # DHT Dropdown
        combo = QComboBox(self)
        combo.addItem("1")
        combo.addItem("2")
        combo.addItem("3")
        combo.addItem("4")
        combo.setProperty('Test', True)

        # On selected item change
        combo.activated[str].connect(self.onDHTLabelChange)

        # Temp Probe Dropdown
        combo2 = QComboBox(self)
        combo2.addItem("1")
        combo2.addItem("2")
        combo2.addItem("3")
        combo2.addItem("4")

        combo2.activated[str].connect(self.onProbeLabelChange)

        # Current Dropdown
        combo3 = QComboBox(self)
        combo3.addItem("1")
        combo3.addItem("2")
        combo3.addItem("3")
        combo3.addItem("4")

        combo3.activated[str].connect(self.onCurrLabelChange)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(dht_label, 1, 1)
        grid.addWidget(self.dht_value, 1, 2)
        grid.addWidget(combo, 1, 3)

        grid.addWidget(probe_label, 2, 1)
        grid.addWidget(self.probe_value, 2, 2)
        grid.addWidget(combo2, 2, 3)

        grid.addWidget(curr_label, 3, 1)
        grid.addWidget(self.curr_value, 3, 2)
        grid.addWidget(combo3, 3, 3)

        self.setLayout(grid)

        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle('UpdateGui')
        self.show()

    def onDHTLabelChange(self, text):
        self.dht_value.setText(text)
        self.dht_value.adjustSize()

    def onProbeLabelChange(self, text):
        self.probe_value.setText(text)
        self.probe_value.adjustSize()

    def onCurrLabelChange(self, text):
        self.curr_value.setText(text)
        self.curr_value.adjustSize()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you wish to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
    sys.exit(app.exec_())