from PyQt5 import QtCore, QtGui, QtWidgets


class EnterForm(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(217, 157)
        MainWindow.setMinimumSize(QtCore.QSize(217, 157))
        MainWindow.setMaximumSize(QtCore.QSize(217, 157))
        font = QtGui.QFont()
        font.setFamily("TOYZ")
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.enter = QtWidgets.QPushButton(self.centralwidget)
        self.enter.setGeometry(QtCore.QRect(10, 110, 101, 23))
        self.enter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enter.setObjectName("enter")
        self.registerbt = QtWidgets.QPushButton(self.centralwidget)
        self.registerbt.setGeometry(QtCore.QRect(10, 82, 201, 23))
        self.registerbt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.registerbt.setObjectName("registerbt")
        self.enterlb = QtWidgets.QLabel(self.centralwidget)
        self.enterlb.setGeometry(QtCore.QRect(10, 10, 181, 16))
        self.enterlb.setObjectName("enterlb")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 201, 52))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.loginlb = QtWidgets.QLabel(self.layoutWidget)
        self.loginlb.setObjectName("loginlb")
        self.gridLayout.addWidget(self.loginlb, 0, 0, 1, 1)
        self.loginle = QtWidgets.QLineEdit(self.layoutWidget)
        self.loginle.setObjectName("loginle")
        self.gridLayout.addWidget(self.loginle, 0, 1, 1, 1)
        self.passwordlb = QtWidgets.QLabel(self.layoutWidget)
        self.passwordlb.setObjectName("passwordlb")
        self.gridLayout.addWidget(self.passwordlb, 1, 0, 1, 1)
        self.passwordle = QtWidgets.QLineEdit(self.layoutWidget)
        self.passwordle.setObjectName("passwordle")
        self.gridLayout.addWidget(self.passwordle, 1, 1, 1, 1)
        self.help = QtWidgets.QPushButton(self.centralwidget)
        self.help.setGeometry(QtCore.QRect(110, 110, 101, 23))
        self.help.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.help.setObjectName("help")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.statusbar.setFont(font)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Best Clicker"))
        self.enter.setText(_translate("MainWindow", "Войти"))
        self.registerbt.setText(_translate("MainWindow", "Зарегистрироваться"))
        self.enterlb.setText(_translate("MainWindow", "Войдите в аккаунт"))
        self.loginlb.setText(_translate("MainWindow", "Логин:"))
        self.passwordlb.setText(_translate("MainWindow", "Пароль:"))
        self.help.setText(_translate("MainWindow", "Помощь"))
