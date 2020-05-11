

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget,  QLabel
import pymysql
import pickle
import uuid
from itertools import chain
import datetime
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import os
import sys
from PyQt5.QtWidgets import *
class main(QMainWindow):
    # 图片改变信号

    imagechangedSignal = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        # todo:软件配置
        self.setFont(QFont("Microsoft YaHei", 12))
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('批量激活程序(有限版)')
        # self.setWindowIcon(QIcon('xyjk.png'))
        # self.progressBar = QProgressBar()
        # self.progressBar.setVisible(False)
        # self.statusBar().addPermanentWidget(self.progressBar)
        # self.setStyleSheet("background-color:rgb(198,47,47,115);")
        # self.move(20, 10)
        self.grid = QGridLayout()
        # 文件名输入框
        # self.textedit = QTextEdit()
        # self.grid.addWidget(self.textedit, 2, 0, 1, 2)

        self.address = "47.105.38.117"
        self.user = "root"
        self.pwd = "1234"
        self.databasename = "downloadpaperactive"
        self.port = 3306

        self.addresslabel=QLabel("配置信息")
        self.grid.addWidget(self.addresslabel, 0, 0, 1, 1)
        self.addresseditline = QLineEdit()
        self.grid.addWidget(self.addresseditline, 0, 1, 1, 1)
        self.changeaddressbutton = QPushButton("修改")
        self.changeaddressbutton.clicked.connect(self.changeaddressbuttonclicked)
        self.grid.addWidget(self.changeaddressbutton, 0, 2, 1, 1)

        self.maclabel=QLabel("激活明文")
        self.grid.addWidget(self.maclabel,1,0,1,1)
        self.maceditline=QLineEdit()
        self.grid.addWidget(self.maceditline,1,1,1,2)

        self.startbutton=QPushButton("生成密钥")
        self.startbutton.clicked.connect(self.startbuttonclicked)
        self.grid.addWidget(self.startbutton,2,0,1,1)
        self.keyeditline=QLineEdit()
        self.grid.addWidget(self.keyeditline,2,1,1,2)

        self.countlabel=QLabel("已使用激活次数：")
        self.grid.addWidget(self.countlabel,3,0,1,1)
        self.countnumlabel=QLabel("0")
        self.grid.addWidget(self.countnumlabel,3,1,1,1)

        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        self.initprocess()

    def initprocess(self):
        settingpath=os.getcwd()+"setting.data"
        if os.path.exists(settingpath):
            with open(settingpath, 'rb') as f:
                strr = pickle.load(f)
                print("strr", strr)
                strr = self.keyeditline2.text()
                add1 = str(int((int(strr[0:4]) - 1000) / 3))
                add2 = str(int((int(strr[4:8]) - 1000) / 3))
                add3 = str(int((int(strr[8:12]) - 1000) / 3))
                add4 = str(int((int(strr[12:16]) - 1000) / 3))
                self.address = add1 + "." + add2 + "." + add3 + "." + add4
                print(self.address)
                databaseinfstr = strr[16:]
                ass = []
                for i in range(int(len(databaseinfstr) / 3)):
                    reallyi = i * 3
                    ass.append(int(databaseinfstr[int(reallyi):int(reallyi + 3)]))
                print("".join(map(chr, ass)))
                databaseinf = "".join(map(chr, ass)).split("-")
                self.user = databaseinf[0]
                self.pwd = databaseinf[1]
                self.port = databaseinf[2]
                self.databasename = databaseinf[3]
        # 获取次数信息
        db = pymysql.connect(self.address, self.user, self.pwd, self.databasename, port=self.port, charset='utf8')
        db.autocommit(True)  # 自动提交
        cursor = db.cursor()
        localmac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        sql = 'select mac from {table}'.format(table='activetools')
        cursor.execute(sql)
        macs = cursor.fetchall()
        localmac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        if localmac not in list(chain.from_iterable(macs)):
            self.statusBar().showMessage("此设备无激活权限！")
            cursor.close()
            db.close()
            return


        sql = "SELECT nowcount,countlimit from activetools WHERE mac = '{mac}'".format(mac=localmac)
        cursor.execute(sql)
        num = cursor.fetchall()
        cursor.close()
        db.close()
        self.countnumlabel.setText(str(num[0][0]) + "/" + str(num[0][1]))

    def changeaddressbuttonclicked(self):
        path=os.getcwd()+"/setting.data"
        addresscode=self.addresseditline.text()
        with open(path, "wb") as file:
            pickle.dump(addresscode, file, True)
        self.statusBar().showMessage("配置信息已更新！")



    def startbuttonclicked(self):
        if self.maceditline.text()=="":
            self.statusBar().showMessage("请输入明文！")
            return

        try:
            today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db = pymysql.connect(self.address, self.user, self.pwd, self.databasename, port=self.port, charset='utf8')
            db.autocommit(True)  # 自动提交
            cursor = db.cursor()
            # cursor = db.cursor(sursor=pymysql.cursors.DictCursor)
            sql = 'select mac from {table}'.format(table='activetools')
            cursor.execute(sql)
            macs = cursor.fetchall()

            localmac = uuid.UUID(int=uuid.getnode()).hex[-12:]
            if localmac not in list(chain.from_iterable(macs)):
                self.statusBar().showMessage("此设备无激活权限！")
                return

            mac = self.maceditline.text()
            mac1 = str((int(mac[0:2], 16) * 1218) % (256))
            mac2 = str((int(mac[2:4], 16) * 1219) % (256))
            mac3 = str((int(mac[4:6], 16) * 1220) % (256))
            mac4 = str((int(mac[6:8], 16) * 1221) % (256))
            mac5 = str((int(mac[8:10], 16) * 1222) % (256))
            mac6 = str((int(mac[10:12], 16) * 1223) % (256))
            key = mac1 + mac2 + mac3 + mac4 + mac5 + mac6
            sql="select mac from macs"
            cursor.execute(sql)
            macs = cursor.fetchall()
            temp=list(chain.from_iterable(macs))
            if mac in list(chain.from_iterable(macs)):
                self.keyeditline.setText(key)
                self.statusBar().showMessage("此设备已激活，不占用本次激活次数")
                # 获取次数信息
                sql = "SELECT nowcount,countlimit from activetools WHERE mac = '{mac}'".format(mac=localmac)
                cursor.execute(sql)
                num = cursor.fetchall()
                self.countnumlabel.setText(str(num[0][0]) + "/" + str(num[0][1]))

                cursor.close()
                db.close()
                return

            # 插入mac
            sql = "INSERT INTO macs(mac,frommac) VALUES ('{mac}', '{localmac}')".format(mac=mac,localmac=localmac)
            cursor.execute(sql)
            # 次数+1
            sql="UPDATE activetools SET nowcount = nowcount + 1 WHERE mac = '{mac}'".format(mac=localmac)
            cursor.execute(sql)
            # 更新时间
            sql = "UPDATE activetools SET lasttime= '{today}' WHERE mac = '{mac}'".format(mac=localmac,today=today)
            cursor.execute(sql)
            # 获取次数信息
            sql = "SELECT nowcount,countlimit from activetools WHERE mac = '{mac}'".format(mac=localmac)
            cursor.execute(sql)
            num = cursor.fetchall()
            self.countnumlabel.setText(str(num[0][0])+"/"+str(num[0][1]))
            
            cursor.close()
            db.close()
            self.keyeditline.setText(key)
        except Exception as e:
            self.statusBar().showMessage("连接异常！（"+str(e)+")")
            cursor.close()
            db.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())