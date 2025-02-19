from PyQt5 import QtCore, QtGui, QtWidgets

class BestClickerForm(object):
    def setupUi(self, MainWindow, font):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(308, 239)
        MainWindow.setMinimumSize(QtCore.QSize(308, 239))
        MainWindow.setMaximumSize(QtCore.QSize(308, 239))
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont("TOYZ")
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 239, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.shopbt = QtWidgets.QPushButton(self.layoutWidget)
        self.shopbt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.shopbt.setObjectName("shopbt")
        self.horizontalLayout_3.addWidget(self.shopbt)
        self.settingsbt = QtWidgets.QPushButton(self.layoutWidget)
        self.settingsbt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.settingsbt.setObjectName("settingsbt")
        self.horizontalLayout_3.addWidget(self.settingsbt)
        self.clickpng = QtWidgets.QLabel(self.centralwidget)
        self.clickpng.setEnabled(True)
        self.clickpng.setGeometry(QtCore.QRect(10, 110, 121, 121))
        self.clickpng.setText("")
        self.clickpng.setPixmap(QtGui.QPixmap("../images/coockie.png"))
        self.clickpng.setScaledContents(True)
        self.clickpng.setWordWrap(False)
        self.clickpng.setOpenExternalLinks(False)
        self.clickpng.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.clickpng.setObjectName("clickpng")
        self.clickbt = QtWidgets.QPushButton(self.centralwidget)
        self.clickbt.setGeometry(QtCore.QRect(10, 110, 120, 120))
        self.clickbt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clickbt.setStyleSheet("background-color:  rgba(255,255,255,0)\n"
"")
        self.clickbt.setText("")
        self.clickbt.setObjectName("clickbt")
        self.mousekek = QtWidgets.QLabel(self.centralwidget)
        self.mousekek.setEnabled(True)
        self.mousekek.setGeometry(QtCore.QRect(180, 110, 121, 121))
        self.mousekek.setText("")
        self.mousekek.setPixmap(QtGui.QPixmap("../images/mouse2.png"))
        self.mousekek.setScaledContents(True)
        self.mousekek.setWordWrap(False)
        self.mousekek.setOpenExternalLinks(False)
        self.mousekek.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.mousekek.setObjectName("mousekek")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 44, 241, 54))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.moneylb = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.moneylb.setFont(font)
        self.moneylb.setObjectName("moneylb")
        self.horizontalLayout.addWidget(self.moneylb)
        self.moneyint = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.moneyint.setFont(font)
        self.moneyint.setObjectName("moneyint")
        self.horizontalLayout.addWidget(self.moneyint)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.energylb = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.energylb.setFont(font)
        self.energylb.setObjectName("energylb")
        self.horizontalLayout_2.addWidget(self.energylb)
        self.energyint = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.energyint.setFont(font)
        self.energyint.setObjectName("energyint")
        self.horizontalLayout_2.addWidget(self.energyint)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Лучший кликер"))
        self.shopbt.setText(_translate("MainWindow", "Магазин"))
        self.settingsbt.setText(_translate("MainWindow", "Настройки"))
        self.moneylb.setText(_translate("MainWindow", "Деньги:"))
        self.moneyint.setText(_translate("MainWindow", "0"))
        self.energylb.setText(_translate("MainWindow", "Энергия:"))
        self.energyint.setText(_translate("MainWindow", "0"))
