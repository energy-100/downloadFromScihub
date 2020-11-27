
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMessageBox
import pickle
from itertools import chain
import os
import datetime
from PyQt5.QtGui import QImage, QFont
import pymysql
from PyQt5 import QtCore
import os
from PyQt5 import QtGui, QtWidgets
from os import startfile
import sys
from PyQt5.QtWidgets import *
import uuid
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
class activationwindow(QWidget):
    succeedSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(activationwindow, self).__init__(parent)
        # todo:软件配置
        self.setFont(QFont("Microsoft YaHei", 12))
        # self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('产品激活,请联系微信')
        self.resize(500,150)
        self.grid=QGridLayout()

        self.maclabel=QLabel("激活明文")
        self.grid.addWidget(self.maclabel,0,0,1,4)

        self.maceditline=QLineEdit()
        self.maceditline.setReadOnly(True)
        self.maceditline.setText(self.get_mac_address())
        self.grid.addWidget(self.maceditline, 0, 4, 1, 4)

        self.keylabel1 = QLabel("激活密钥1")
        self.grid.addWidget(self.keylabel1, 1, 0, 1, 4)

        self.keyeditline2 = QLineEdit()
        # self.keyeditline2.setText(self.get_mac_address())
        self.grid.addWidget(self.keyeditline2, 1, 4, 1, 4)

        self.keylabel=QLabel("激活密钥2")
        self.grid.addWidget(self.keylabel,2,0,1,4)

        self.keyeditline2=QLineEdit()
        self.grid.addWidget(self.keyeditline2, 2, 4, 1, 4)


        self.zhifubaocodelabel=QLabel()
        self.zhifubaocodelabel.setPixmap(QPixmap('zhifubao.jpg'))
        self.zhifubaocodelabel.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.zhifubaocodelabel,3,0,1,4)

        self.weixincodelabel=QLabel()
        self.weixincodelabel.setPixmap(QPixmap('weixin.jpg'))
        self.weixincodelabel.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.weixincodelabel,3,4,1,4)

        self.inftextlabel = QLabel()
        self.inftextlabel.setText("编写软件不易，您一包烟的钱，却是对我最大的鼓励！\n请备注上边激活明文(右键复制)后转账（支付宝左，微信右）五元激活！\n ")
        self.inftextlabel.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.inftextlabel, 4, 0, 1, 8)

        self.inflabel = QLabel()
        self.inflabel.setText("")
        self.inflabel.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.inflabel, 5, 0, 1, 8)

        self.keyactivebutton=QPushButton("单设备密钥激活")
        self.keyactivebutton.clicked.connect(self.keyactivebuttonclicked)
        self.grid.addWidget(self.keyactivebutton, 6, 0, 1, 4)

        self.webactivebutton=QPushButton("联网自动激活")
        self.webactivebutton.clicked.connect(self.webactivebuttonclicked)
        self.grid.addWidget(self.webactivebutton, 6, 4, 1, 4)








        self.setLayout(self.grid)



    def keyactivebuttonclicked(self):
        if self.keyeditline2.text() !="":
            mac=self.maceditline.text()
            mac1 = str((int(mac[0:2], 16) * 1218) % (256))
            mac2 = str((int(mac[2:4], 16) * 1219) % (256))
            mac3 = str((int(mac[4:6], 16) * 1220) % (256))
            mac4 = str((int(mac[6:8], 16) * 1221) % (256))
            mac5 = str((int(mac[8:10], 16) * 1222) % (256))
            mac6 = str((int(mac[10:12], 16) * 1223) % (256))
            macfinall=mac1+mac2+mac3+mac4+mac5+mac6
            if self.keyeditline2.text()==macfinall:
                self.inflabel.setText("激活成功！")
                self.savekey()
                self.close()
                self.succeedSignal.emit()
            else:
                self.inflabel.setText("激活失败！")





    def get_mac_address(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        # print(r"/x" + r'/x'.join([hex(ord(c)).replace('0x', '') for c in mac])
        #       )
        # print(type(mac))
        mac= "".join([mac[e:e + 2] for e in range(0, 11, 2)])
        # return mac[0:4]+"-"""".join([mac[e:e + 2] for e in range(0, 11, 2)])
        # return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
        return mac


    def webactivebuttonclicked(self):
        if self.keyeditline2.text()=="":
            address="47.105.38.117"
            user="root"
            pwd="1234"
            databasename="downloadpaperactive"
            port=3306
        else:
            strr=self.keyeditline2.text()
            add1=str(int((int(strr[0:4])-1000)/3))
            add2=str(int((int(strr[4:8])-1000)/3))
            add3=str(int((int(strr[8:12])-1000)/3))
            add4=str(int((int(strr[12:16])-1000)/3))
            address=add1+"."+add2+"."+add3+"."+add4
            print(address)
            databaseinfstr=strr[16:]
            ass=[]
            for i in range(int(len(databaseinfstr)/3)):
                reallyi=i*3
                ass.append(int(databaseinfstr[int(reallyi):int(reallyi+3)]))
            print("".join(map(chr, ass)))
            databaseinf="".join(map(chr, ass)).split("-")
            user=databaseinf[0]
            pwd=databaseinf[1]
            port=databaseinf[2]
            databasename=databaseinf[3]
        today="table"+datetime.date.today().strftime('%y%m%d')
        db = pymysql.connect(address, user, pwd, databasename, port=port, charset='utf8')
        db.autocommit(True) #自动提交
        cursor = db.cursor()
        # cursor = db.cursor(sursor=pymysql.cursors.DictCursor)
        sql = 'select mac from {table}'.format(table='macs')
        cursor.execute(sql)
        macs = cursor.fetchall()
        cursor.close()
        db.close()
        print(macs)
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        a=list(macs[:][0])
        print(a)
        if mac in list(chain.from_iterable(macs)):
            self.inflabel.setText("激活成功！")
            self.updatadatabase()
            self.savekey()
            self.close()
            self.succeedSignal.emit()
        else:
            self.inflabel.setText("激活失败，此设备未注册！")


    def savekey(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = "".join([mac[e:e + 2] for e in range(0, 11, 2)])
        mac1 = str((int(mac[0:2], 16) * 1218) % (256))
        mac2 = str((int(mac[2:4], 16) * 1219) % (256))
        mac3 = str((int(mac[4:6], 16) * 1220) % (256))
        mac4 = str((int(mac[6:8], 16) * 1221) % (256))
        mac5 = str((int(mac[8:10], 16) * 1222) % (256))
        mac6 = str((int(mac[10:12], 16) * 1223) % (256))
        macfinall = mac1 + mac2 + mac3 + mac4 + mac5 + mac6
        activefilepath = os.getcwd() + "/act.data"
        with open(activefilepath, "wb") as file:
            pickle.dump(macfinall, file, True)

    def updatadatabase(self):
        pass




class getactivethread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(list)

    def __init__(self, urls, title, trans, page=1):
        self.urls = urls
        self.title = title
        self.page = page
        self.trans = trans
        super(getactivethread, self).__init__()

    def run(self):
        pass