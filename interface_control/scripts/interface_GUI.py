#!/usr/bin/env python
# -*-coding:utf-8 -*-
import rospy
# import threading
# import time
import numpy as np
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from Ui_main import Ui_MainWindow
from interface_control.msg import cal_cmd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

class MyThread(QThread):
    callback = Signal(int, int)#自定義訊號, Qt的文件中有說明, 必需為類別變數
    def __init__(self, label, delay, parent=None):
        super(MyThread, self).__init__(parent)
        self.runFlag = True
        self.label=label
        self.delay=delay
        
    def __del__(self):
        self.runFlag = False
        self.wait()

    def run(self):
        index=0
        while self.runFlag:
            self.callback.emit(index, self.label)
            # print(threading.currentThread().getName())
            index+=1
            self.msleep(self.delay)


    def setData(self, index, value, role):
        if role == Qt.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            self._data[index.row(), index.column()] = value
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.pub_cmd = rospy.Publisher("/cal_command",cal_cmd, queue_size=10)
        self.cal_cmd = cal_cmd()
        # self.pub_ipset = rospy.Publisher("/ip_comm",ipconfig,queue_size=10)
        # self.pub_closenode = rospy.Publisher("/close_node",closenode,queue_size=10)
        # self.startthreadflag = False
        # self.setStyleSheet()
        # self._creat_menubar()
        # self.ui.lineEdit_vel.setText(str(self.vel))
        # self.ui.lineEdit_acc.setText(str(self.acc))
        self.ui.btn_dynamics.clicked.connect(self.dyna_buttonClicked)
        self.ui.btn_dyn_space.clicked.connect(self.dyna_space_buttonClicked)

        # # Vel. HorizontalSlider
        # self.ui.horizontalSlider_vel.valueChanged.connect(self.VelSliderValue)
        # # Acc. HorizontalSlider
        # self.ui.horizontalSlider_acc.valueChanged.connect(self.AccSliderValue)

        # # ComboBox
        # # choices = ['None','Show 1', 'Show 2', 'Init', 'Home','Stop','Show All Select','jogging']
        # choices = ['None','Show 1', 'Show 2', 'Init', 'Home','Stop','Show All Select']
        # self.ui.comboBox.addItems(choices)
        # self.ui.comboBox.currentIndexChanged.connect(self.display)
        # self.display()
        
        
    #     self.initUi()


    # def initUi(self):
    #     self.status = self.statusBar()
    #     self.status.showMessage('Update State', 0) #状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
    #     self.status.setStyleSheet("font-size: 18px;background-color: #F5E8FF")
    #     self.safetyNum = QtWidgets.QLabel("Safety:")
    #     self.taskNum = QtWidgets.QLabel("Task:")
    #     self.reloadNum = QtWidgets.QLabel("Reload:")

    #     self.safetyNum.setFixedWidth(200)
    #     self.safetyNum.setStyleSheet("font-size: 18px;border-radius: 25px;border: 1px solid black;")
    #     self.taskNum.setFixedWidth(200)
    #     self.taskNum.setStyleSheet("font-size: 18px;border-radius: 25px;border: 1px solid black;")
    #     self.reloadNum.setFixedWidth(200)
    #     self.reloadNum.setStyleSheet("font-size: 18px;border-radius: 25px;border: 1px solid black;")

    #     self.status.addPermanentWidget(self.safetyNum, stretch=0)
    #     self.status.addPermanentWidget(self.taskNum, stretch=0)
    #     self.status.addPermanentWidget(self.reloadNum, stretch=0)
        
    # def setStyleSheet(self):
    #     self.ui.btn_reset.setStyleSheet("QPushButton" + "{" + "background-color:#da7700;\n" + "color:white;\n" + "border-color: black;" 
    #         + "}" + "QPushButton::pressed" + "{" + "background-color :#5151A2;\n" + "color:white;" +"}")
    #     self.ui.btn_enable.setStyleSheet("QPushButton" + "{" + "background-color:#00d21a;\n" + "color:white;\n" + "border-color: black;" 
    #         + "}" + "QPushButton::pressed" + "{" + "background-color :#5151A2;\n" + "color:white;" +"}")


    

    def dyna_space_buttonClicked(self):
        self.pub_cmd.publish(1)

    def dyna_buttonClicked(self):
        self.pub_cmd.publish(2)

    # def display(self):
        
    #     if self.ui.comboBox.currentText() == "None":
    #         # self.ui.label_mission_case_show.setText('Choose：%s' % self.ui.comboBox.currentText())
    #         task_value = 0
    #         # self.ui_reload_program()
    #     elif self.ui.comboBox.currentText() == "Show 1":
    #         self.ui.label_mission_case_show.setText('Choose：%s' % self.ui.comboBox.currentText())
    #         task_value = 1
    #         self.ui_reload_program()
    #         self.ui.comboBox.setCurrentIndex(0)
    #     self.mission_number = task_value
        

    # def topic_callback_init(self):
    #     self.pub_armstatus = rospy.Subscriber("/reply_external_comm",peripheralCmd,self.topic_reply_callback)
    #     self.sub_taskcmd = rospy.Subscriber("/write_external_comm",peripheralCmd,self.topic_write_callback)
    #     self.peripheralCmd = peripheralCmd()

    # def topic_write_callback(self,data):
    #     self.task_cmd = data.actionTypeID
    #     self.statusID = data.statusID

    # def topic_reply_callback(self,data):
    #     self.task_cmd_reply = data.actionTypeID
    #     self.statusID_reply = data.statusID

if __name__=="__main__":
    rospy.init_node("interface_ui")
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    