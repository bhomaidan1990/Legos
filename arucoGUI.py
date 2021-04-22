#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow,
	QDesktopWidget, QLabel, QComboBox, QPushButton, QSizePolicy, QGroupBox,
	QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt5.QtCore import (Qt, QCoreApplication, QMetaObject, pyqtProperty, 
	QRect, QPropertyAnimation, pyqtProperty)
from PyQt5.QtGui import QPixmap, QPalette, QColor

#======================
# class AnimatedLabel |
#======================
class AnimatedLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

        self.colorDict = {
                "b": QColor(0, 0, 255),
                "y": QColor(255, 255, 0),
                "g": QColor(0, 130, 0),
                "bg": [QColor(0, 0, 255), QColor(0, 130, 0)],
                "yg": [QColor(255, 255, 0), QColor(0, 130, 0)],
                "bp": [QColor(0, 0, 255), QColor(255, 10, 10)],
                "yp": [QColor(255, 255, 0), QColor(255, 10, 10)]
                }
        self.color_anim = QPropertyAnimation(self, b'zcolor')

    def blink(self, mode):
        
        self.color_anim.stop()

        if len(mode)==1:
            bgColor = fgColor = self.colorDict[mode]
        elif len(mode)==2:
            bgColor = self.colorDict[mode][0]
            fgColor = self.colorDict[mode][1]
        else:
            bgColor = fgColor = QColor(0, 0, 0)

        self.color_anim.setStartValue(bgColor)
        self.color_anim.setKeyValueAt(0.2, bgColor)
        self.color_anim.setKeyValueAt(0.6, fgColor)
        self.color_anim.setKeyValueAt(0.2, bgColor)
        self.color_anim.setEndValue(bgColor)
        self.color_anim.setDuration(2000)
        self.color_anim.setLoopCount(-1)
        self.color_anim.start()

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def getBackColor(self):
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        sss = self.parseStyleSheet()
        bg_new = 'background-color: rgba(%d,%d,%d,%d);' % (color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Abackground-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    pal_ele = QPalette.Window
    zcolor = QtCore.pyqtProperty(QColor, getBackColor, setBackColor)

#======================
# class Ui_MainWindow |
#======================
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        #------------------------------------------------------
        # central widget
        #===============
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.centralwidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #------- Initialization -------------------------------
        # Messenger
        self.LB_Messenger = QLabel(self.centralwidget)
        self.LB_Messenger.setGeometry(QRect(260, 20, 841, 111))
        # self.LB_Messenger.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.LB_Messenger.setScaledContents(True)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.LB_Messenger.setFont(font)
        self.LB_Messenger.setAlignment(Qt.AlignCenter)
        self.LB_Messenger.setWordWrap(True)
        self.LB_Messenger.setObjectName("LB_Messenger")
        self.LB_Messenger.setStyleSheet("background-color: pink; border: 1px solid black;")

        # ArUco Group Box
        self.arucoGB = QGroupBox(self.centralwidget)
        self.arucoGB.setGeometry(QRect(260, 140, 841, 631))
        # self.arucoGB.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.arucoGB.setObjectName("arucoGB")
        self.arucoGB.setStyleSheet("background-color: lightgreen; border: 1px solid black;")

        # Cells Labels
        # 01
        self.LB_01 = AnimatedLabel(self.arucoGB)
        self.LB_01.setGeometry(QRect(140, 60, 131, 121))
        self.LB_01.setScaledContents(True)
        self.LB_01.setObjectName("LB_01")
        self.LB_01.setStyleSheet("background-color: green; border: 1px solid black;") # lightgreen
        # 02
        self.LB_02 = AnimatedLabel(self.arucoGB)
        self.LB_02.setGeometry(QRect(280, 60, 131, 121))
        # self.LB_02.setScaledContents(True)
        self.LB_02.setObjectName("LB_02")
        self.LB_02.setStyleSheet("background-color: green; border: 1px solid black;")
        # 03
        self.LB_03 = AnimatedLabel(self.arucoGB)
        self.LB_03.setGeometry(QRect(420, 60, 131, 121))
        # self.LB_03.setScaledContents(True)
        self.LB_03.setObjectName("LB_03")
        self.LB_03.setStyleSheet("background-color: green; border: 1px solid black;")
        # 04
        self.LB_04 = AnimatedLabel(self.arucoGB)
        self.LB_04.setGeometry(QRect(560, 60, 131, 121))
        # self.LB_04.setScaledContents(True)
        self.LB_04.setObjectName("LB_04")
        self.LB_04.setStyleSheet("background-color: green; border: 1px solid black;")
        # 05
        self.LB_05 = AnimatedLabel(self.arucoGB)
        self.LB_05.setGeometry(QRect(140, 190, 131, 121))
        # self.LB_05.setScaledContents(True)
        self.LB_05.setObjectName("LB_05")
        self.LB_05.setStyleSheet("background-color: green; border: 1px solid black;")
        # 06
        self.LB_06 = AnimatedLabel(self.arucoGB)
        self.LB_06.setGeometry(QRect(280, 190, 131, 121))
        # self.LB_06.setScaledContents(True)
        self.LB_06.setObjectName("LB_06")
        self.LB_06.setStyleSheet("background-color: green; border: 1px solid black;")
        # 07
        self.LB_07 = AnimatedLabel(self.arucoGB)
        self.LB_07.setGeometry(QRect(420, 190, 131, 121))
        # self.LB_07.setScaledContents(True)
        self.LB_07.setObjectName("LB_07")
        self.LB_07.setStyleSheet("background-color: green; border: 1px solid black;")
        # 08
        self.LB_08 = AnimatedLabel(self.arucoGB)
        self.LB_08.setGeometry(QRect(560, 190, 131, 121))
        # self.LB_08.setScaledContents(True)
        self.LB_08.setObjectName("LB_08")
        self.LB_08.setStyleSheet("background-color: green; border: 1px solid black;")
        # 09
        self.LB_09 = AnimatedLabel(self.arucoGB)
        self.LB_09.setGeometry(QRect(140, 320, 131, 121))
        # self.LB_09.setScaledContents(True)
        self.LB_09.setObjectName("LB_09")
        self.LB_09.setStyleSheet("background-color: green; border: 1px solid black;")
        # 10
        self.LB_10 = AnimatedLabel(self.arucoGB)
        self.LB_10.setGeometry(QRect(280, 320, 131, 121))
        # self.LB_10.setScaledContents(True)
        self.LB_10.setObjectName("LB_10")
        self.LB_10.setStyleSheet("background-color: green; border: 1px solid black;")
        # 11
        self.LB_11 = AnimatedLabel(self.arucoGB)
        self.LB_11.setGeometry(QRect(420, 320, 131, 121))
        # self.LB_11.setScaledContents(True)
        self.LB_11.setObjectName("LB_11")
        self.LB_11.setStyleSheet("background-color: green; border: 1px solid black;")
        # 12
        self.LB_12 = AnimatedLabel(self.arucoGB)
        self.LB_12.setGeometry(QRect(560, 320, 131, 121))
        # self.LB_12.setScaledContents(True)
        self.LB_12.setObjectName("LB_12")
        self.LB_12.setStyleSheet("background-color: green; border: 1px solid black;")
        # 13
        self.LB_13 = AnimatedLabel(self.arucoGB)
        self.LB_13.setGeometry(QRect(140, 450, 131, 121))
        # self.LB_13.setScaledContents(True)
        self.LB_13.setObjectName("LB_13")
        self.LB_13.setStyleSheet("background-color: green; border: 1px solid black;")
        # 14
        self.LB_14 = AnimatedLabel(self.arucoGB)
        self.LB_14.setGeometry(QRect(280, 450, 131, 121))
        # self.LB_14.setScaledContents(True)
        self.LB_14.setObjectName("LB_14")
        self.LB_14.setStyleSheet("background-color: green; border: 1px solid black;")
        # 15
        self.LB_15 = AnimatedLabel(self.arucoGB)
        self.LB_15.setGeometry(QRect(420, 450, 131, 121))
        # self.LB_15.setScaledContents(True)
        self.LB_15.setObjectName("LB_15")
        self.LB_15.setStyleSheet("background-color: green; border: 1px solid black;")
        # 16
        self.LB_16 = AnimatedLabel(self.arucoGB)
        self.LB_16.setGeometry(QRect(560, 450, 131, 121))
        # self.LB_16.setScaledContents(True)
        self.LB_16.setObjectName("LB_16")
        self.LB_16.setStyleSheet("background-color: green; border: 1px solid black;")

        # Swap GroupBox
        self.swapGB = QGroupBox(self.centralwidget)
        self.swapGB.setGeometry(QRect(60, 250, 181, 471))
        # self.swapGB.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.swapGB.setObjectName("swapGB")
        self.swapGB.setStyleSheet("background-color: lightgreen; border: 1px solid black;")
        # Swap Labels
        # s1
        self.LB_s1 = AnimatedLabel(self.swapGB)
        self.LB_s1.setGeometry(QRect(30, 310, 131, 121))
        # self.LB_s1.setScaledContents(True)
        self.LB_s1.setObjectName("LB_s1")
        self.LB_s1.setStyleSheet("background-color: green; border: 1px solid black;")
        # s2
        self.LB_s2 = AnimatedLabel(self.swapGB)
        self.LB_s2.setGeometry(QRect(30, 180, 131, 121))
        # self.LB_s2.setScaledContents(True)
        self.LB_s2.setObjectName("LB_s2")
        self.LB_s2.setStyleSheet("background-color: green; border: 1px solid black;")
        # s3
        self.LB_s3 = AnimatedLabel(self.swapGB)
        self.LB_s3.setGeometry(QRect(30, 40, 131, 121))
        # self.LB_s3.setScaledContents(True)
        self.LB_s3.setObjectName("LB_s3")
        self.LB_s3.setStyleSheet("background-color: green; border: 1px solid black;")
        # Logo Label
        self.LB_Logo = QLabel(self.centralwidget)
        self.LB_Logo.setGeometry(QRect(60, 20, 141, 111))
        # self.LB_Logo.setScaledContents(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        # self.LB_Logo.setFont(font)
        self.LB_Logo.setAlignment(Qt.AlignCenter)
        # self.LB_Logo.setWordWrap(True)
        self.LB_Logo.setObjectName("LB_Logo")
        logoPixmap = QPixmap('logo.png')
        self.LB_Logo.setPixmap(logoPixmap)
        self.LB_Logo.setScaledContents(False)
        # ArUco Selector Label
        self.LB_ArUco_selector = QLabel(self.centralwidget)
        self.LB_ArUco_selector.setGeometry(QRect(60, 150, 141, 51))
        # self.LB_ArUco_selector.setScaledContents(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LB_ArUco_selector.setFont(font)
        self.LB_ArUco_selector.setAlignment(Qt.AlignCenter)
        self.LB_ArUco_selector.setObjectName("LB_ArUco_selector")
        # ArUco Combo Box
        self.Aruco_selector = QComboBox(self.centralwidget)
        self.Aruco_selector.setGeometry(QRect(60, 210, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Aruco_selector.setFont(font)
        self.Aruco_selector.setObjectName("Aruco_selector")
        self.Aruco_selector.addItem('id_18')
        self.Aruco_selector.addItem('id_25')
        self.Aruco_selector.addItem('id_101')
        self.Aruco_selector.activated[str].connect(self.messenger)
        # Exit Push Butoon
        self.PB_Exit = QPushButton(self.centralwidget)
        self.PB_Exit.setGeometry(QRect(90, 730, 131, 41))
        #
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.PB_Exit.setFont(font)
        self.PB_Exit.setObjectName("PB_Exit")
        #------------------------------------------------
        # Layout
        mainLayout  = QGridLayout(self.centralwidget)
        leftLayout  = QGridLayout()
        rightLayout = QGridLayout()
        arucoLayout = QGridLayout(self.arucoGB)
        swapLayout  = QGridLayout(self.swapGB)
        #
        arucoLayout.addWidget(self.LB_01, 0, 0)
        arucoLayout.addWidget(self.LB_02, 0, 1)
        arucoLayout.addWidget(self.LB_03, 0, 2)
        arucoLayout.addWidget(self.LB_04, 0, 3)
        arucoLayout.addWidget(self.LB_05, 1, 0)
        arucoLayout.addWidget(self.LB_06, 1, 1)
        arucoLayout.addWidget(self.LB_07, 1, 2)
        arucoLayout.addWidget(self.LB_08, 1, 3)
        arucoLayout.addWidget(self.LB_09, 2, 0)
        arucoLayout.addWidget(self.LB_10, 2, 1)
        arucoLayout.addWidget(self.LB_11, 2, 2)
        arucoLayout.addWidget(self.LB_12, 2, 3)
        arucoLayout.addWidget(self.LB_13, 3, 0)
        arucoLayout.addWidget(self.LB_14, 3, 1)
        arucoLayout.addWidget(self.LB_15, 3, 2)
        arucoLayout.addWidget(self.LB_16, 3, 3)
        #
        rightLayout.addWidget(self.LB_Messenger, 0, 0, 1, 4)
        rightLayout.addWidget(self.arucoGB, 1, 0, 4, 4)
        #
        swapLayout.addWidget(self.LB_s3, 0, 0)
        swapLayout.addWidget(self.LB_s2, 1, 0)
        swapLayout.addWidget(self.LB_s1, 2, 0)
        #
        leftLayout.addWidget(self.LB_Logo, 0, 0)
        leftLayout.addWidget(self.LB_ArUco_selector, 1, 0)
        leftLayout.addWidget(self.Aruco_selector, 2, 0)
        leftLayout.addWidget(self.swapGB, 3, 0, 3, 1)
        leftLayout.addWidget(self.PB_Exit, 6, 0)
        #
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1, 1, 4)
        #------------------------------------------------
        MainWindow.setCentralWidget(self.centralwidget)
        #------------------------------------------------
        self.retranslateUi(MainWindow)
        #===================================================================
        #======================== Signals ==================================
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #
        self.PB_Exit.clicked.connect(self.close)
        # self.PB_Exit.clicked.connect(lambda: self.wrong('s3'))

        #==================================================================
        #==================================================================
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ArUco_Tasks"))
        self.LB_Messenger.setText(_translate("MainWindow", "Messenger"))
        self.LB_ArUco_selector.setText(_translate("MainWindow", "Select ArUco"))
        # ArUco GB
        self.arucoGB.setTitle(_translate("MainWindow", "Platform"))
        # Cells
        self.LB_01.setText(_translate("MainWindow", "01"))
        self.LB_02.setText(_translate("MainWindow", "02"))
        self.LB_03.setText(_translate("MainWindow", "03"))
        self.LB_04.setText(_translate("MainWindow", "04"))
        self.LB_05.setText(_translate("MainWindow", "05"))
        self.LB_06.setText(_translate("MainWindow", "06"))
        self.LB_07.setText(_translate("MainWindow", "07"))
        self.LB_08.setText(_translate("MainWindow", "08"))
        self.LB_09.setText(_translate("MainWindow", "09"))
        self.LB_10.setText(_translate("MainWindow", "10"))
        self.LB_11.setText(_translate("MainWindow", "11"))
        self.LB_12.setText(_translate("MainWindow", "12"))
        self.LB_13.setText(_translate("MainWindow", "13"))
        self.LB_14.setText(_translate("MainWindow", "14"))
        self.LB_15.setText(_translate("MainWindow", "15"))
        self.LB_16.setText(_translate("MainWindow", "16"))
        # Swap GB
        self.swapGB.setTitle(_translate("MainWindow", "Swap Zone"))
        # Swap Cells
        self.LB_s1.setText(_translate("MainWindow", "s1"))
        self.LB_s2.setText(_translate("MainWindow", "s2"))
        self.LB_s3.setText(_translate("MainWindow", "s3"))
        # Exit PB
        self.PB_Exit.setText(_translate("MainWindow", "Exit"))

    def blinker(self, ID, mode):
    	workspaceDict = {
    	1: self.LB_01,
    	2: self.LB_02,
    	3: self.LB_03,
    	4: self.LB_04,
    	5: self.LB_05,
    	6: self.LB_06,
    	7: self.LB_07,
    	8: self.LB_08,
    	9: self.LB_09,
    	10: self.LB_10,
    	11: self.LB_11,
    	12: self.LB_12,
    	13: self.LB_13,
    	14: self.LB_14,
    	15: self.LB_15,
    	16: self.LB_16,
    	's1': self.LB_s1,
    	's2': self.LB_s2,
    	's3': self.LB_s3
    	}
    	workspaceDict[ID].blink(mode)

    def wrong(self, ID):
    	workspaceDict = {
    	1: self.LB_01,
    	2: self.LB_02,
    	3: self.LB_03,
    	4: self.LB_04,
    	5: self.LB_05,
    	6: self.LB_06,
    	7: self.LB_07,
    	8: self.LB_08,
    	9: self.LB_09,
    	10: self.LB_10,
    	11: self.LB_11,
    	12: self.LB_12,
    	13: self.LB_13,
    	14: self.LB_14,
    	15: self.LB_15,
    	16: self.LB_16,
    	}
    	wrongPixmap = QPixmap('wrong.png')
    	w = workspaceDict[ID].width()
    	h = workspaceDict[ID].height()
    	workspaceDict[ID].setPixmap(wrongPixmap.scaled(w,h,Qt.KeepAspectRatio))
    	workspaceDict[ID].setScaledContents(True)

    def messenger(self, text):
    	self.LB_Messenger.setText(text)

    def close(selft):
        QCoreApplication.quit()

#=================
#  Main Function #
#=================
if __name__ == "__main__":

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # screenShape = QDesktopWidget().screenGeometry()
    # MainWindow.resize(screenShape.width(), screenShape.height())
    MainWindow.show()
    sys.exit(app.exec_())