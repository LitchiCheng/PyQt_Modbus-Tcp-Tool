# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
import sys
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QWidget

 #modbus_tcp_io板模拟操作
import modbus_tk
import modbus_tk.defines as modbus_define
import modbus_tk.modbus_tcp as modbus_tcp
class modbus_tcp_toolkit():
    _is_connected = False
    def __init__(self, slave_ip_str, slave_id_int = 1):
        try:
            self.master = modbus_tcp.TcpMaster(host=slave_ip_str)
            self.master.set_timeout(5.0)
        except:
            print("modbus_tcp connect fail...")
    def readHoldRegister(self, slave_id_int = 1, first_register_id_int = 0, register_num_int = 0):
        try:
            return self.master.execute(slave_id_int, modbus_define.READ_HOLDING_REGISTERS, first_register_id_int, register_num_int)
        except:
            print("readHoldRegister fail...")
    def readInputRegister(self, slave_id_int = 1, first_register_id_int = 0, register_num_int = 0):
        try:
            return self.master.execute(slave_id_int, modbus_define.READ_INPUT_REGISTERS, first_register_id_int, register_num_int)
        except:
            print("readInputRegister fail...")
    def readCoilsRegister(self, slave_id_int = 1, first_register_id_int = 0, register_num_int = 0):
        try:
            self._is_connected = True
            return self.master.execute(slave_id_int, modbus_define.READ_COILS, first_register_id_int, register_num_int)
        except:
            self._is_connected = False
            print("readCoilsRegister fail...")
            return False
    def readDiscreteRegister(self, slave_id_int = 1, first_register_id_int = 0, register_num_int = 0):
        try:
            self._is_connected = True
            return self.master.execute(slave_id_int, modbus_define.READ_DISCRETE_INPUTS, first_register_id_int, register_num_int)
        except:
            self._is_connected = False
            print("readDiscreteRegister fail...")
            return False
    def writeSingleHoldRegister(self, slave_id_int = 1, first_register_id_int = 0, register_value_int = 0):
        try:
            self.master.execute(slave_id_int, modbus_define.WRITE_SINGLE_REGISTER, first_register_id_int, output_value = regiter_value_int)
        except:
            print("writeSingleHoldRegister fail...")
    def writeSingleCoilRegister(self, slave_id_int = 1, first_register_id_int = 0, register_value_int = 0):
        try:
            self.master.execute(slave_id_int, modbus_define.WRITE_SINGLE_COIL, first_register_id_int, output_value = register_value_int)
        except:
            print("writeSingleCoilRegister fail...")
    def writeMultipleHoldRegister(self, slave_id_int = 1, first_register_id_int = 0, register_value_int_arrary = [0,0,0,0,0,0,0,0]):
        try:
            self.master.execute(slave_id_int, modbus_define.WRITE_MULTIPLE_REGISTERS, first_register_id_int, output_value = register_value_int_arrary)
        except:
            print("writeMultipleHoldRegister fail...")
    def writeMultipleCoilRegister(self, slave_id_int = 1, first_register_id_int = 0, register_value_int_arrary = [0,0,0,0,0,0,0,0]):
        try:
            self.master.execute(slave_id_int, modbus_define.WRITE_MULTIPLE_COILS, first_register_id_int, output_value = register_value_int_arrary)
        except:
            print("writeMultipleCoilRegister fail...")

class Example(QWidget):

    di_status_label={}
    di_order_label={}
    button={}

    def __init__(self):
        super().__init__()
        
        self.initUI()


    def initUI(self):      
        self.is_connected = False
        self.is_connect_pressed = False
        self.grid = QGridLayout()
        self.setLayout(self.grid) 
    
        self.connect_status_text = "连接状态为:"
        self.connect_status_label = QLabel(self.connect_status_text, self)

        self.ip_address_label = QLabel("IP地址：", self)
        self.ip_address_edit = QLineEdit("192.168.192.111",self)
        #self.ip_address_edit.setFixedSize(100,25)

        self.do_address_label = QLabel("DO地址：", self)
        self.do_address_edit = QLineEdit("1",self)

        self.do_num_label = QLabel("DO数量：", self)
        self.do_num_edit = QLineEdit("8",self)

        self.di_address_label = QLabel("DI地址：", self)
        self.di_address_edit = QLineEdit("32",self)

        self.di_num_label = QLabel("DI数量：", self)
        self.di_num_edit = QLineEdit("8",self)

        connect_button = QPushButton("connect", self)
        disconnect_button = QPushButton("disconnect", self)
        #connect_button.setFixedSize(75,25)
        #disconnect_button.setFixedSize(75,25)
        connect_button.clicked.connect(self.buttonClicked)
        disconnect_button.clicked.connect(self.buttonClicked)
     
        # open_button = QPushButton("open", self)
        # close_button = QPushButton("ResetDO", self)
        #close_button.setFixedSize(75,25)
        #open_button.setFixedSize(75,25)
        # open_button.clicked.connect(self.buttonClicked)            
        # close_button.clicked.connect(self.buttonClicked)

        self.grid.addWidget(self.ip_address_label, 1, 0)
        self.grid.addWidget(self.ip_address_edit, 1, 1)
        self.grid.addWidget(self.do_address_label, 2, 0)
        self.grid.addWidget(self.do_address_edit, 2, 1)
        self.grid.addWidget(self.do_num_label, 3, 0)
        self.grid.addWidget(self.do_num_edit, 3, 1)
        self.grid.addWidget(self.di_address_label, 4, 0)
        self.grid.addWidget(self.di_address_edit, 4, 1)
        self.grid.addWidget(self.di_num_label, 5, 0)
        self.grid.addWidget(self.di_num_edit, 5, 1)
        self.grid.addWidget(connect_button, 6, 0)
        self.grid.addWidget(disconnect_button, 6, 1)

        self.grid.addWidget(self.connect_status_label, 7, 0)
        # self.grid.addWidget(open_button, 8, 0)
        # self.grid.addWidget(close_button, 8, 1)
        self.grid.setSpacing(45)
        # self.statusBar()
        # self.resize(550,400)
        #self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('MODBUS_TCP_TOOLKIT')
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        #self.setWindowFlag(Qt.FramelessWindowHint) # 隐藏边框
        self.show()


    def buttonClicked_open(self):
        self.modbus_master.writeSingleCoilRegister(1,0,1)

    def buttonClicked_close(self):
        self.modbus_master.writeSingleCoilRegister()

    def buttonClicked(self):
        sender = self.sender()
       
        if "open" == sender.text() :
            if self.is_connected == True:
                self.modbus_master.writeSingleCoilRegister(1,0,1)
        elif "ResetDO" == sender.text():
            if self.is_connected == True:
                try:
                    self.status = self.modbus_master.writeSingleCoilRegister()
                except:
                    print(self.status)
        elif "connect" == sender.text():
            self.ip_address_edit.setEnabled(False)
            self.di_num_edit.setEnabled(False)
            self.do_num_edit.setEnabled(False)
            self.di_address_edit.setEnabled(False)
            self.do_address_edit.setEnabled(False)
            if self.is_connect_pressed == False:
                self.modbus_master = modbus_tcp_toolkit(self.ip_address_edit.text())
                status = self.modbus_master.readDiscreteRegister(1,32,8)
                self.is_connect_pressed = True
                if status == False:
                    self.is_connected = False
                    self.connect_status_label.setText("连接状态为："+"失败")
                else:
                    self.is_connected = True
                    self.connect_status_label.setText("连接状态为："+"成功")
                    self.modbus_master.writeMultipleCoilRegister()
                    for i in range(1, (int(self.do_num_edit.text())+1)): 
                        self.button[i]=QPushButton(str(i))
                        self.button[i].setFixedSize(50,50)
                        self.grid.addWidget(self.button[i],9,(i-1))
                        self.button[i].clicked.connect(self.doClicked)  
                    for i in range(1, (int(self.di_num_edit.text())+1)):
                        self.di_order_label[i]=QLabel("DI-"+str(i))
                        self.di_order_label[i].setFixedSize(50,50)
                        self.grid.addWidget(self.di_order_label[i],10,(i-1))
                    for i in range(1, (int(self.di_num_edit.text())+1)): 
                        self.di_status_label[i-1]=QLabel(" ")
                        self.di_status_label[i-1].setFixedSize(50,50)
                        self.grid.addWidget(self.di_status_label[i-1],11,(i-1))
                    # self.di_status_label[1].setText("sdfa")
                    self.thread = work()
                    self.thread.signal.connect(self.updateText)
                    self.thread.start()         
        elif "disconnect" == sender.text():
            self.is_connect_pressed = False
            self.is_connected = False
            self.ip_address_edit.setEnabled(True)
            self.di_num_edit.setEnabled(True)
            self.do_num_edit.setEnabled(True)
            self.di_address_edit.setEnabled(True)
            self.do_address_edit.setEnabled(True)
            self.connect_status_label.setText("连接状态为："+"断开")
            #self.grid.removeWidget(self.label)
            #隐藏控件
            #self.label.close()

    def updateText(self):
        if self.is_connected == True:
            status = self.modbus_master.readDiscreteRegister(1,32,int(self.di_num_edit.text()))
            # print(status)
            # print(self.di_status_label[3])
            # str1 = "DI状态为:" + str(status[0])
            for i in range(1, int(self.di_num_edit.text())+1):
                try:
                    self.di_status_label[i-1].setText(str(status[i-1]))
                except:
                    print("updataText failed...")
            #self.di_status_label.setText(str1)
            # self.statusBar().showMessage("查询操作")
    
    def doClicked(self):
        sender = self.sender()
        do_status = self.modbus_master.readCoilsRegister(1, 0 ,int(self.do_num_edit.text()))
        # print(do_status)
        if self.is_connected == True:
            print("DO-"+sender.text())
            if (do_status[(int(sender.text())-1)] == 0):
                self.modbus_master.writeSingleCoilRegister(1,(int(sender.text())-1),1)
            else:
                self.modbus_master.writeSingleCoilRegister(1,(int(sender.text())-1),0)

        
class work(QThread):
    signal = pyqtSignal()    # 括号里填写信号传递的参数类型
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
    # 进行任务操作
        while(1):
            self.signal.emit()    # 发射信号
            time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
