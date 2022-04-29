#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, 
| LIG lab/ Marvin Team, 
| France, 2021.
| ArUco GUI.
'''

import sys
import re
from time import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLabel, QComboBox,
QPushButton, QSizePolicy, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout)
# , QApplication, QMainWindow
from PyQt5.QtCore import (Qt, QCoreApplication, QMetaObject, pyqtProperty, 
    QRect, QPropertyAnimation, pyqtProperty, QTimer)
from PyQt5.QtGui import QPixmap, QPalette, QColor, QPainter

# from yuVision import visionHandler
from problemHandler import problemHandler
#======================
# class AnimatedLabel |
#======================
class AnimatedLabel(QLabel):
    def __init__(self, parent=None):
        """
        Class AnimatedLabel: turns QLabel into animated one with 
          Foreground/Background blinking colors.
        ---
        Parameters:
        @param: path, string, the path to the problem.
        @param: filename, string, the problem filename.
        """
        QLabel.__init__(self, parent)
        # color mapping
        self.colorDict = {
                "b": QColor(0, 0, 255),
                "y": QColor(255, 255, 0),
                "g": QColor(0, 130, 0),
                # "bg": [QColor(0, 0, 255), QColor(0, 130, 0)],
                # "yg": [QColor(255, 255, 0), QColor(0, 130, 0)],
                "gp": [QColor(0, 130, 0), QColor(255, 10, 10)],
                "bp": [QColor(0, 0, 255), QColor(255, 10, 10)],
                "yp": [QColor(255, 255, 0), QColor(255, 10, 10)]
                }
        self.color_anim = QPropertyAnimation(self, b'zcolor')

    def blink(self, mode):
        """
        Function: blink, define the foreground backgound color for blinking.
        ---
        Parameters:
        @param: mode, string, any of the set: ['b', 'y', 'g', 'bp', 'yp', 'gp']
        ---
        @return: None
        """
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
        """
        Function: parseStyleSheet, lists the styleSheet parameters.
        ---
        Parameters:
        @param: None
        ---
        @return: sts, list, list of the styleSheet Parameters.
        """
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def getBackColor(self):
        """
        Function: getBackColor, returns the styleSheet backgound color.
        ---
        Parameters:
        @param: None
        ---
        @return: color, QColor, color of the styleSheet background.
        """
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        """
        Function: setBackColor, sets the styleSheet backgound color.
        ---
        Parameters:
        @param: color, QColor, the color to be assigned to the background.
        ---
        @return: None
        """
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
    def __init__(self, MainWindow, path):
        """
        Class Ui_MainWindow:to create the GUI Main Window.
        ---
        Parameters:
        @param: MainWindow, QMainWindow object.
        @param: path, string, the path to the problem.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(3840, 2160)
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ArUco"))

        boldFfont = QtGui.QFont()
        boldFfont.setPointSize(12)
        boldFfont.setBold(True)
        boldFfont.setWeight(60)
        self.path = path
        self.problemChanged = False
        self.exit  = False
        self.startFlag = False
        # self.vh = visionHandler('', taskID='', connection=False)
        self.ph = problemHandler(path=path, filename='problem_main.pddl', ui=self)
        self.actionState = True
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.solved = False
        self.GB_aruco = QGroupBox(self.centralwidget)
        self.GB_aruco.setGeometry(QRect(600, 150, 1850, 1600))
        self.GB_aruco.setObjectName("GB_aruco")
        self.GB_aruco.setStyleSheet("background-color: lightgreen; border: 1px solid black;")
        # 
        self.LB_RC_00 = QLabel(self.GB_aruco)
        self.LB_RC_00.setGeometry(QRect(480, 50, 200, 300))
        self.LB_RC_00.setObjectName("LB_RC_00")
        self.LB_RC_00.setStyleSheet("background-color: red; border: 1px solid black;")

        self.LB_RC_x0 = QLabel(self.GB_aruco)
        self.LB_RC_x0.setGeometry(QRect(480, 1300, 200, 300))
        self.LB_RC_x0.setObjectName("LB_RC_x0")
        self.LB_RC_x0.setStyleSheet("background-color: red; border: 1px solid black;")

        self.LB_RC_0y = QLabel(self.GB_aruco)
        self.LB_RC_0y.setGeometry(QRect(1630, 50, 200, 300))
        self.LB_RC_0y.setObjectName("LB_RC_0y")
        self.LB_RC_0y.setStyleSheet("background-color: red; border: 1px solid black;")

        self.LB_RC_xy = QLabel(self.GB_aruco)
        self.LB_RC_xy.setGeometry(QRect(1630, 1300, 200, 300))
        self.LB_RC_xy.setObjectName("LB_RC_xy")
        self.LB_RC_xy.setStyleSheet("background-color: red; border: 1px solid black;")
        #
        self.LB_p_10_04 = AnimatedLabel(self.GB_aruco)
        self.LB_p_10_04.setGeometry(QRect(710, 380, 200, 200))
        self.LB_p_10_04.setObjectName("LB_p_10_04")
        self.LB_p_10_04.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_10_05 = AnimatedLabel(self.GB_aruco)
        self.LB_p_10_05.setGeometry(QRect(710, 610, 200, 200))
        self.LB_p_10_05.setObjectName("LB_p_10_05")
        self.LB_p_10_05.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_10_06 = AnimatedLabel(self.GB_aruco)
        self.LB_p_10_06.setGeometry(QRect(710, 840, 200, 200))
        self.LB_p_10_06.setObjectName("LB_p_10_06")
        self.LB_p_10_06.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_10_07 = AnimatedLabel(self.GB_aruco)
        self.LB_p_10_07.setGeometry(QRect(710, 1070, 200, 200))
        self.LB_p_10_07.setObjectName("LB_p_10_07")
        self.LB_p_10_07.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_11_04 = AnimatedLabel(self.GB_aruco)
        self.LB_p_11_04.setGeometry(QRect(940, 380, 200, 200))
        self.LB_p_11_04.setObjectName("LB_p_11_04")
        self.LB_p_11_04.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_11_05 = AnimatedLabel(self.GB_aruco)
        self.LB_p_11_05.setGeometry(QRect(940, 610, 200, 200))
        self.LB_p_11_05.setObjectName("LB_p_11_05")
        self.LB_p_11_05.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_11_06 = AnimatedLabel(self.GB_aruco)
        self.LB_p_11_06.setGeometry(QRect(940, 840, 200, 200))
        self.LB_p_11_06.setObjectName("LB_p_11_06")
        self.LB_p_11_06.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_11_07 = AnimatedLabel(self.GB_aruco)
        self.LB_p_11_07.setGeometry(QRect(940, 1070, 200, 200))
        self.LB_p_11_07.setObjectName("LB_p_11_07")
        self.LB_p_11_07.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_12_04 = AnimatedLabel(self.GB_aruco)
        self.LB_p_12_04.setGeometry(QRect(1170, 380, 200, 200))
        self.LB_p_12_04.setObjectName("LB_p_12_04")
        self.LB_p_12_04.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_12_05 = AnimatedLabel(self.GB_aruco)
        self.LB_p_12_05.setGeometry(QRect(1170, 610, 200, 200))
        self.LB_p_12_05.setObjectName("LB_p_12_05")
        self.LB_p_12_05.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_12_06 = AnimatedLabel(self.GB_aruco)
        self.LB_p_12_06.setGeometry(QRect(1170, 840, 200, 200))
        self.LB_p_12_06.setObjectName("LB_p_12_06")
        self.LB_p_12_06.setStyleSheet("background-color: green; border: 1px solid black;")                                                                        

        self.LB_p_12_07 = AnimatedLabel(self.GB_aruco)
        self.LB_p_12_07.setGeometry(QRect(1170, 1070, 200, 200))
        self.LB_p_12_07.setObjectName("LB_p_12_07")
        self.LB_p_12_07.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_13_04 = AnimatedLabel(self.GB_aruco)
        self.LB_p_13_04.setGeometry(QRect(1400, 380, 200, 200))
        self.LB_p_13_04.setObjectName("LB_p_13_04")
        self.LB_p_13_04.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_13_05 = AnimatedLabel(self.GB_aruco)
        self.LB_p_13_05.setGeometry(QRect(1400, 610, 200, 200))
        self.LB_p_13_05.setObjectName("LB_p_13_05")
        self.LB_p_13_05.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_p_13_06 = AnimatedLabel(self.GB_aruco)
        self.LB_p_13_06.setGeometry(QRect(1400, 840, 200, 200))
        self.LB_p_13_06.setObjectName("LB_p_13_06")
        self.LB_p_13_06.setStyleSheet("background-color: green; border: 1px solid black;")
                    
        self.LB_p_13_07 = AnimatedLabel(self.GB_aruco)
        self.LB_p_13_07.setGeometry(QRect(1400, 1070, 200, 200))
        self.LB_p_13_07.setObjectName("LB_p_13_07")
        self.LB_p_13_07.setStyleSheet("background-color: green; border: 1px solid black;")
        #
        color = QColor(25, 200, 25)

        self.LB_swap_top = QLabel(self.GB_aruco)
        self.LB_swap_top.setGeometry(QRect(10, 550, 200, 200))
        self.LB_swap_top.setObjectName("LB_swap_top")
        self.LB_swap_top.setStyleSheet("background-color: rgba(%d,%d,%d,%d); border: 1px solid black;" % (color.red(), color.green(), color.blue(), color.alpha()))

        self.LB_s1 = AnimatedLabel(self.GB_aruco)
        self.LB_s1.setGeometry(QRect(10, 840, 200, 200))
        self.LB_s1.setObjectName("LB_s2")
        self.LB_s1.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_s2 = AnimatedLabel(self.GB_aruco)
        self.LB_s2.setGeometry(QRect(10, 1070, 200, 200))
        self.LB_s2.setObjectName("LB_s1")
        self.LB_s2.setStyleSheet("background-color: green; border: 1px solid black;")

        self.LB_swap_bottom = QLabel(self.GB_aruco)
        self.LB_swap_bottom.setGeometry(QRect(10, 1360, 200, 200))
        self.LB_swap_bottom.setObjectName("LB_swap_bottom")
        self.LB_swap_bottom.setStyleSheet("background-color: rgba(%d,%d,%d,%d); border: 1px solid black;" % (color.red(), color.green(), color.blue(), color.alpha()))

        self.LB_Messenger_title = QLabel(self.centralwidget)
        self.LB_Messenger_title.setGeometry(QRect(2500, 150, 1200, 400))
        self.LB_Messenger_title.setObjectName("LB_Messenger_title")
        self.LB_Messenger_title.setStyleSheet("background-color: pink; border: 5px solid black;")
        self.LB_Messenger_title.setAlignment(Qt.AlignCenter)
        self.LB_Messenger_title.setFont(boldFfont)
        self.LB_Messenger_title.setText('YuMi Messenger')

        self.LB_Messenger = QLabel(self.centralwidget)
        self.LB_Messenger.setGeometry(QRect(2500, 600, 1200, 1150))
        self.LB_Messenger.setObjectName("LB_Messenger")
        self.LB_Messenger.setStyleSheet("background-color: pink; border: 5px solid black;")
        self.LB_Messenger.setFont(boldFfont)
        self.LB_Messenger.setAlignment(Qt.AlignCenter)
        self.LB_Messenger.setWordWrap(True)
        self.LB_Messenger.setText('----------------\n\n----------------')

        self.LB_Logo = QLabel(self.centralwidget)
        self.LB_Logo.setGeometry(QRect(100, 50, 450, 600))
        self.LB_Logo.setObjectName("LB_Logo")
        logoPixmap = QPixmap('logo.png')
        self.LB_Logo.setPixmap(logoPixmap)
        self.LB_Logo.setScaledContents(True)

        # ArUco Combo Box
        self.Aruco_selector = QComboBox(self.centralwidget)
        self.Aruco_selector.setGeometry(QRect(50, 800, 500, 100))
        self.Aruco_selector.setFont(boldFfont)
        self.Aruco_selector.setObjectName("Aruco_selector")
        self.Aruco_selector.addItem('id_18')
        self.Aruco_selector.addItem('id_21')
        self.Aruco_selector.addItem('id_25')
        self.Aruco_selector.addItem('id_101')

        self.GB_PB = QGroupBox(self.centralwidget)
        self.GB_PB.setGeometry(QRect(50, 1150, 500, 650))
        self.GB_PB.setObjectName("GB_PB")
        self.GB_PB.setStyleSheet("border: 1px solid black;")

        self.PB_Start = QPushButton(self.GB_PB)
        self.PB_Start.setGeometry(QRect(50, 50, 400, 150))
        self.PB_Start.setFont(boldFfont)
        self.PB_Start.setObjectName("PB_Start")
        self.PB_Start.setText("Start")

        self.PB_Stop = QPushButton(self.GB_PB)
        self.PB_Stop.setGeometry(QRect(50, 250, 400, 150))
        self.PB_Stop.setFont(boldFfont)
        self.PB_Stop.setObjectName("PB_Stop")
        self.PB_Stop.setText("Stop")

        self.PB_Exit = QPushButton(self.GB_PB)
        self.PB_Exit.setGeometry(QRect(50, 450, 400, 150))
        self.PB_Exit.setFont(boldFfont)
        self.PB_Exit.setObjectName("PB_Exit")
        self.PB_Exit.setText("Exit")

        MainWindow.setCentralWidget(self.centralwidget)
 
        QMetaObject.connectSlotsByName(MainWindow)
        #===================================================================
        #======================== Signals ==================================
        self.PB_Start.clicked.connect(self.start)
        self.PB_Stop.clicked.connect(self.stop)
        self.PB_Exit.clicked.connect(self.close)
        self.Aruco_selector.currentTextChanged.connect(self.arucoChanged)

        #==================================================================
        #==================================================================
    def blinker(self, ID, mode, reset=False):
        """
        Function: blinker, to make the labels blink/not blink with specific colors.
        ---
        Parameters:
        @param: ID, string, the id of the Label to change its colors.
        @param: mode, string, any of the set: ['b', 'y', 'g', 'bp', 'yp', 'gp']
        ---
        @return: None
        """
        workspaceDict = {
        'p_10_04': self.LB_p_10_04,
        'p_11_04': self.LB_p_11_04,
        'p_12_04': self.LB_p_12_04,
        'p_13_04': self.LB_p_13_04,
        'p_10_05': self.LB_p_10_05,
        'p_11_05': self.LB_p_11_05,
        'p_12_05': self.LB_p_12_05,
        'p_13_05': self.LB_p_13_05,
        'p_10_06': self.LB_p_10_06,
        'p_11_06': self.LB_p_11_06,
        'p_12_06': self.LB_p_12_06,
        'p_13_06': self.LB_p_13_06,
        'p_10_07': self.LB_p_10_07,
        'p_11_07': self.LB_p_11_07,
        'p_12_07': self.LB_p_12_07,
        'p_13_07': self.LB_p_13_07,
        'p_07_06': self.LB_s1,
        'p_07_07': self.LB_s2
        }

        if reset:
            workspaceDict[ID].clear()
            w = workspaceDict[ID].width()
            h = workspaceDict[ID].height()
            pm2 = QPixmap(w, h)
            pm2.fill(Qt.transparent)
            workspaceDict[ID].setPixmap(pm2.scaled(w,h,Qt.KeepAspectRatio))
            workspaceDict[ID].setScaledContents(True)

        workspaceDict[ID].blink(mode)



    def wrong(self, ID):
        """
        Function: wrong, to show wrong signal on the label.
        ---
        Parameters:
        @param: ID, string, the id of the Label to change its colors.
        ---
        @return: None
        """
        workspaceDict = {
        'p_10_04': self.LB_p_10_04,
        'p_11_04': self.LB_p_11_04,
        'p_12_04': self.LB_p_12_04,
        'p_13_04': self.LB_p_13_04,
        'p_10_05': self.LB_p_10_05,
        'p_11_05': self.LB_p_11_05,
        'p_12_05': self.LB_p_12_05,
        'p_13_05': self.LB_p_13_05,
        'p_10_06': self.LB_p_10_06,
        'p_11_06': self.LB_p_11_06,
        'p_12_06': self.LB_p_12_06,
        'p_13_06': self.LB_p_13_06,
        'p_10_07': self.LB_p_10_07,
        'p_11_07': self.LB_p_11_07,
        'p_12_07': self.LB_p_12_07,
        'p_13_07': self.LB_p_13_07
        }
        wrongPixmap = QPixmap('wrong.png')
        w = workspaceDict[ID].width()
        h = workspaceDict[ID].height()
        workspaceDict[ID].setPixmap(wrongPixmap.scaled(w,h,Qt.KeepAspectRatio))
        workspaceDict[ID].setScaledContents(True)

    def messenger(self, text, idx=0):
        """
        Function: messenger, to make the labels blink/not blink with specific colors.
        ---
        Parameters:
        @param: text, string, the text to be shown on the Messenger Label.
        @param: idx, integer, index of the mesage, 0: Warning, 1: Error.
        ---
        @return: None
        """
        tex = self.LB_Messenger.text()
        message = tex.split("\n\n")

        message[idx] = text
        message = "\n\n".join(message)
        self.LB_Messenger.setText(message)

    def getArUcoID(self):
        """
        Function: getArUcoID, to get ArUco ID.
        ---
        Parameters:
        @param: None
        ---
        @return: text, string, ArUco ID.
        """
        text = str(self.Aruco_selector.currentText())
        return text

    def arucoChanged(self):
        """
        Function: arucoChanged, to detect problem change.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        if self.startFlag:
            self.problemChanged = True

    def start(self):
        """
        Function: start, to start.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        self.startFlag = True
        # self.vh.taskID = self.getArUcoID()
        # self.messenger("YuMi is Thinking!,")
        # self.messenger("---------------------", idx=1)
        self.ph.NoSolution = False
        self.ph.solved = False
        self.ph.reset_problem()
        self.startLooper()


    def startLooper(self):

        if self.ph.vh.solved:
            # self.messenger("Thank You")
            # self.messenger("Task Has been solved", idx=1)
            print("gui, Solved")
            self.messenger("je vous remercie beaucoup")
            self.messenger("La tâche a été résolue", idx=1)
            
            return

        print('Procedure is Running!')
        if (not self.ph.NoSolution) and self.startFlag and (not self.ph.vh.solved):
            # print("Waiting for YuMi Server ...")
            # self.messenger("YuMi is Thinking!.")
            if self.actionState:
                # self.messenger("YuMi is Thinking!..")
                print("Running...")
                tic = time()

                self.ph.stateReader()

                toc = time()
                
                print("time for perception is: ", round(toc-tic, 3))
                tic = toc
                # self.messenger("Please see the used positions before to move!")
                self.ph.run()
            
            if (not self.ph.NoSolution):
                # self.messenger("Please Feel Free to work on the Free Zone!..")
                self.ph.checkAction()

            QTimer.singleShot(5000, self.startLooper)


        if self.ph.NoSolution:

            # self.messenger("Please wait The Robot to Take a photo!,")
            # self.messenger("Please Do the Rest, our Robot cannot do more!,,")
            self.messenger("Je ne peux plus vous aider. Je vous laisse terminer.")
            self.ph.stateReader()

            QTimer.singleShot(5000, self.startLooper)


    def stop(self):
        """
        Function: stop, to stop.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        self.startFlag = False
        legos = self.ph.vh.taskWorld[self.getArUcoID()]
        for point in legos:
        	self.blinker(point, 'g', reset=True)
        self.messenger("---------------------,")
        self.messenger("---------------------,", idx=1)
        self.ph = problemHandler(path=self.path, filename='problem_main.pddl', ui=self)
        print("Stopped !")

    def close(self):
        """
        Function: close, to close the GUI.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        self.exit = True
        QCoreApplication.quit()

#=================
#  Main Function #
#=================

if __name__ == "__main__":

	mypath = 'G:/Grenoble/Semester_4/Project_Codes/Problem_Domain/New_Domain_Problem/'

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()

	ui = Ui_MainWindow(MainWindow, mypath)
	MainWindow.show()
	sys.exit(app.exec_())
