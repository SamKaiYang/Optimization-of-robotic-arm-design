#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import rospy
# import threading
# import time
import numpy as np

from dynamics.dynamics_function_teco import Dynamics_space

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
# matplotlib.use("Qt5Agg") 

from Ui_main import Ui_MainWindow
from interface_control.msg import cal_cmd, dyna_data, dyna_space_data
import sys
import importlib
importlib.reload(sys)

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

class MyFigureCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=5, xlim=(0, 2500), ylim=(-2, 2), dpi=100):
        # 创建一个Figure
        fig = plt.Figure(figsize=(width, height), dpi=dpi, tight_layout=True) # tight_layout: 用于去除画图时两边的空白

        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)

        self.axes = fig.add_subplot(111) # 添加子图
        self.axes.spines['top'].set_visible(False) # 去掉绘图时上面的横线
        self.axes.spines['right'].set_visible(False) # 去掉绘图时右面的横线
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

class MainWindow(QtWidgets.QMainWindow,Dynamics_space):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化 gv_visual_data 的显示
        self.gv_visual_data_content = MyFigureCanvas(width=self.ui.graphicsView.width() / 101,
                            height=self.ui.graphicsView.height() / 101,
                            xlim=(0, 2*np.pi),
                            ylim=(-1, 1)) # 实例化一个FigureCanvas

        self.pub_cmd = rospy.Publisher("/cal_command",cal_cmd, queue_size=10)
        self.pub_dyna_data = rospy.Publisher("/dynamics_data",dyna_data, queue_size=10)
        self.pub_dyna_space = rospy.Publisher("/dynamics_space_data",dyna_space_data, queue_size=10)
        self.cal_cmd = cal_cmd()
        self.dyna_data = dyna_data()
        self.dyna_space_data = dyna_space_data()
        
        self.payload = 0.0
        self.payload_position = [0.0,0.0,0.0]
        self.payload_space = 0.0
        self.payload_position_space = [0.0,0.0,0.0]
        self.joint_velocity = [0.0,0.0,0.0,0.0,0.0,0.0]
        self.joint_acceleration = [0.0,0.0,0.0,0.0,0.0,0.0]
        self.joint_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
        # self.pub_ipset = rospy.Publisher("/ip_comm",ipconfig,queue_size=10)
        # self.pub_closenode = rospy.Publisher("/close_node",closenode,queue_size=10)
        # self.startthreadflag = False
        # self.setStyleSheet()
        # self._creat_menubar()
        # self.ui.lineEdit_vel.setText(str(self.vel))
        # self.ui.lineEdit_acc.setText(str(self.acc))
        self.ui.btn_dynamics.clicked.connect(self.dyna_buttonClicked)
        self.ui.btn_dyn_space.clicked.connect(self.dyna_space_buttonClicked)
        self.ui.btn_dyn_set.clicked.connect(self.dyna_set_buttonClicked)
        self.ui.btn_dyn_space_set.clicked.connect(self.dyna_space_set_buttonClicked)
        self.ui.btn_arm_plot.clicked.connect(self.arm_plot_buttonClicked)
        self.ui.btn_dyn_axis_set.clicked.connect(self.axis_set_buttonClicked)
        
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


    def dyna_set_buttonClicked(self):
        self.payload = float(self.ui.lineEdit_payload.text())
        self.dyna_data.payload = self.payload

        payload_x = float(self.ui.lineEdit_payload_x.text())
        payload_y = float(self.ui.lineEdit_payload_y.text())
        payload_z = float(self.ui.lineEdit_payload_z.text())
        self.payload_position = [payload_x, payload_y, payload_z]
        self.dyna_data.payload_position = self.payload_position

        vel_0 = float(self.ui.lineEdit_vel_0.text())
        vel_1 = float(self.ui.lineEdit_vel_1.text())
        vel_2 = float(self.ui.lineEdit_vel_2.text())
        vel_3 = float(self.ui.lineEdit_vel_3.text())
        vel_4 = float(self.ui.lineEdit_vel_4.text())
        vel_5 = float(self.ui.lineEdit_vel_5.text())
        self.joint_velocity = [vel_0, vel_1, vel_2, vel_3, vel_4, vel_5]
        self.dyna_data.vel = self.joint_velocity

        acc_0 = float(self.ui.lineEdit_acc_0.text())
        acc_1 = float(self.ui.lineEdit_acc_1.text())
        acc_2 = float(self.ui.lineEdit_acc_2.text())
        acc_3 = float(self.ui.lineEdit_acc_3.text())
        acc_4 = float(self.ui.lineEdit_acc_4.text())
        acc_5 = float(self.ui.lineEdit_acc_5.text())
        self.joint_acceleration = [acc_0, acc_1, acc_2, acc_3, acc_4, acc_5]
        self.dyna_data.acc = self.joint_acceleration

        jog_0 = float(self.ui.lineEdit_jog_0.text())
        jog_1 = float(self.ui.lineEdit_jog_1.text())
        jog_2 = float(self.ui.lineEdit_jog_2.text())
        jog_3 = float(self.ui.lineEdit_jog_3.text())
        jog_4 = float(self.ui.lineEdit_jog_4.text())
        jog_5 = float(self.ui.lineEdit_jog_5.text())
        self.joint_angle = [jog_0, jog_1, jog_2, jog_3, jog_4, jog_5]
        self.dyna_data.joint_angle = self.joint_angle

        self.pub_dyna_data.publish(self.dyna_data)

    def dyna_space_set_buttonClicked(self):
        # self.dyna_space_data
        self.payload_space = float(self.ui.lineEdit_payload_space.text())
        self.dyna_space_data.payload = self.payload_space

        payload_x = float(self.ui.lineEdit_payload_x_space.text())
        payload_y = float(self.ui.lineEdit_payload_y_space.text())
        payload_z = float(self.ui.lineEdit_payload_z_space.text())
        self.payload_position_space = [payload_x, payload_y, payload_z]
        self.dyna_space_data.payload_position = self.payload_position_space

        self.pub_dyna_space.publish(self.dyna_space_data)
        
    def axis_set_buttonClicked(self):
        self.axis = int(self.ui.lineEdit_axis_set.text())
        self.dyna_space_data.analysis_axis = self.axis
        self.pub_dyna_space.publish(self.dyna_space_data)

        self.pub_cmd.publish(3)

    def dyna_space_buttonClicked(self):
        self.pub_cmd.publish(1)

    def dyna_buttonClicked(self):
        self.pub_cmd.publish(2)

    def arm_plot_buttonClicked(self):
        self.pub_cmd.publish(4)
        # self.init()
        # self.arm_plot()

        # self.graphic_scene.addWidget(self.arm_plot()) # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        # self.ui.graphicsView.setScene(self.graphic_scene) # 把QGraphicsScene放入QGraphicsView
        # self.ui.graphicsView.show() # 调用show方法呈现图形

        # x = np.arange(0, 2 * np.pi, np.pi / 100)
        # y = np.cos(x)
        # self.gv_visual_data_content.axes.plot(x, y)
        # self.gv_visual_data_content.axes.set_title('cos()')
        # # 加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        # self.graphic_scene = QGraphicsScene() # 创建一个QGraphicsScene
        # self.graphic_scene.addWidget(self.gv_visual_data_content) # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        # self.ui.graphicsView.setScene(self.graphic_scene) # 把QGraphicsScene放入QGraphicsView
        # self.ui.graphicsView.show() # 调用show方法呈现图形

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
    