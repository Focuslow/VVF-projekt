from PyQt5 import QtGui, QtWidgets, QtCore
from mnc import mnc
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 850, 563))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(4, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QtCore.QSize(300, 100))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)

        self.line_2 = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(10)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.verticalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.radioButton_3 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout_2.addWidget(self.radioButton_3)

        self.radioButton_2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)

        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn.setText("Run")
        self.verticalLayout.addWidget(self.btn)

        self.namiestoTohtoTrebaGraf = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.namiestoTohtoTrebaGraf.setAlignment(QtCore.Qt.AlignCenter)
        self.namiestoTohtoTrebaGraf.setWordWrap(False)
        self.namiestoTohtoTrebaGraf.setObjectName("namiestoTohtoTrebaGraf")
        self.horizontalLayout.addWidget(self.namiestoTohtoTrebaGraf)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.conn_btns()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Zadaj systém"))
        self.label_2.setText(_translate("MainWindow", "Vyber vstupný signál"))
        self.radioButton_3.setText(_translate("MainWindow", "Niečo"))
        self.radioButton_2.setText(_translate("MainWindow", "Step"))
        self.radioButton.setText(_translate("MainWindow", "Sin"))
        self.namiestoTohtoTrebaGraf.setText(_translate("MainWindow", "fdsfdsfsdssssssssssssssssssssssssssssssssssssssssssssssssssss"))

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            if event.key() == QtCore.Qt.Key_Escape:
                sys.exit(0)

    def conn_btns(self):
        self.btn.clicked.connect(self.start)

    def start(self):
        num = self.lineEdit.text()
        den = self.lineEdit_2.text()

        sys=[list(num.split(",")),list(den.split(","))]

        mnc(sys)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())