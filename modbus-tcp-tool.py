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

    def __init__(self):
        super().__init__()
        
        self.initUI()


    def initUI(self):      
        self.is_connected = False
        self.is_connect_pressed = False
        self.grid = QGridLayout()
        self.setLayout(self.grid)    
        btn1 = QPushButton("open", self)
        #btn1.move(30, 50)

        btn2 = QPushButton("close", self)
        #btn2.move(30, 100)

        btn3 = QPushButton("query", self)
        #btn3.move(30, 150)

        btn1.clicked.connect(self.buttonClicked)            
        btn2.clicked.connect(self.buttonClicked)
        btn3.clicked.connect(self.buttonClicked)
    
        self.text = "DI状态为:"
        self.label = QLabel(self.text, self)
        self.label_address = QLabel("IP地址：", self)
        #self.label.move(30,300)

        self.tcp_address = QLineEdit("192.168.192.111",self)
        #self.tcp_address.move(30, 200)
        btn4 = QPushButton("connect", self)
        #btn4.move(30, 250)
        btn5 = QPushButton("disconnect", self)
        #btn5.move(200, 250)
        btn4.clicked.connect(self.buttonClicked)
        btn5.clicked.connect(self.buttonClicked)

        self.grid.addWidget(self.label_address, 1, 0)
        self.grid.addWidget(self.tcp_address, 1, 1)
        self.grid.addWidget(btn4, 2, 0)
        self.grid.addWidget(btn5, 2, 1)
        self.grid.addWidget(self.label, 3, 0)
        self.grid.addWidget(btn1, 4, 0)
        self.grid.addWidget(btn2, 4, 1)
        self.grid.addWidget(btn3, 5, 0)

        # self.statusBar()
        # self.resize(550,400)
        #self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('MODBUS_TCP_TOOLKIT')
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
                # self.statusBar().showMessage("打开操作")
        elif "close" == sender.text():
            if self.is_connected == True:
                self.modbus_master.writeSingleCoilRegister()
                # self.statusBar().showMessage("关闭操作")
        elif "query" == sender.text():
            if self.is_connected == True:
                status = self.modbus_master.readDiscreteRegister(1,32,8)
                str1 = "DI状态为:" + str(status[0])
                self.label.setText(str1)
                # self.statusBar().showMessage("查询操作")
        elif "connect" == sender.text():
            if self.is_connect_pressed == False:
                self.modbus_master = modbus_tcp_toolkit(self.tcp_address.text())
                status = self.modbus_master.readDiscreteRegister(1,32,8)
                self.is_connect_pressed = True
                if status == False:
                    self.is_connected = False
                    # self.statusBar().showMessage("连接失败...")
                else:
                    self.is_connected = True
                    self.thread = work()
                    self.thread.signal.connect(self.updateText)
                    self.thread.start()
                    # self.statusBar().showMessage("连接成功...")
        elif "disconnect" == sender.text():
            self.is_connect_pressed = False
            self.is_connected = False
            #self.grid.removeWidget(self.label)
            #隐藏控件
            #self.label.close()
            


    def updateText(self):
        if self.is_connected == True:
            status = self.modbus_master.readDiscreteRegister(1,32,8)
            print(status)
            str1 = "DI状态为:" + str(status[0])
            self.label.setText(str1)
            # self.statusBar().showMessage("查询操作")
        
        

class work(QThread):
    signal = pyqtSignal()    # 括号里填写信号传递的参数
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
