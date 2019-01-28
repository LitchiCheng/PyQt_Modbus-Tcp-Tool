# #!/usr/bin/python3
# # -*- coding: utf-8 -*-

import sys
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QLabel

 #modbus_tcp_io板模拟操作
import modbus_tk
import modbus_tk.defines as modbus_define
import modbus_tk.modbus_tcp as modbus_tcp
class modbus_tcp_toolkit():
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
            return self.master.execute(slave_id_int, modbus_define.READ_COILS, first_register_id_int, register_num_int)
        except:
            print("readCoilsRegister fail...")
    def readDiscreteRegister(self, slave_id_int = 1, first_register_id_int = 0, register_num_int = 0):
        try:
            return self.master.execute(slave_id_int, modbus_define.READ_DISCRETE_INPUTS, first_register_id_int, register_num_int)
        except:
            print("readDiscreteRegister fail...")
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

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.modbus_master = modbus_tcp_toolkit('192.168.192.111')
        self.initUI()


    def initUI(self):      

        btn1 = QPushButton("open", self)
        btn1.move(30, 50)

        btn2 = QPushButton("close", self)
        btn2.move(30, 100)

        btn3 = QPushButton("query", self)
        btn3.move(30, 150)

        btn1.clicked.connect(self.buttonClicked)            
        btn2.clicked.connect(self.buttonClicked)
        btn3.clicked.connect(self.buttonClicked)
        
        self.thread = work()
        self.thread.signal.connect(self.updateText)
        self.thread.start()
    
        self.text = "DI状态为:"
        self.label = QLabel(self.text, self)
        self.label.move(30,250)
    
        self.statusBar()

        self.setGeometry(300, 300, 100, 400)
        self.setWindowTitle('MODBUS_TCP_TOOLKIT')
        self.show()


    def buttonClicked_open(self):
        self.modbus_master.writeSingleCoilRegister(1,0,1)

    def buttonClicked_close(self):
        self.modbus_master.writeSingleCoilRegister()

    def buttonClicked(self):
        sender = self.sender()
        if "open" == sender.text() :
            self.modbus_master.writeSingleCoilRegister(1,0,1)
            self.statusBar().showMessage("打开操作")
        elif "close" == sender.text():
            self.modbus_master.writeSingleCoilRegister()
            self.statusBar().showMessage("关闭操作")
        elif "query" == sender.text():
            status = self.modbus_master.readDiscreteRegister(1,32,8)
            print(status)
            str1 = "DI状态为:" + str(status[0])
            self.label.setText(str1)
            self.statusBar().showMessage("查询操作")

    def updateText(self):
            status = self.modbus_master.readDiscreteRegister(1,32,8)
            print(status)
            str1 = "DI状态为:" + str(status[0])
            self.label.setText(str1)
            self.statusBar().showMessage("查询操作")
        
        

class work(QThread):
    signal = pyqtSignal()    # 括号里填写信号传递的参数
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
    # 进行任务操作
        while(1):
            for i in range(10):
                self.signal.emit()    # 发射信号
                time.sleep(1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
