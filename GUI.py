from datetime import datetime
import datetime
import numpy as np
import cv2
import math
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QColorDialog
from PyQt5.QtCore import QRect, Qt
import pickle
import os
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication,QFont
from PyQt5 import QtCore
import os
from PyQt5 import QtGui, QtWidgets
from os import startfile
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from PyQt5.QtWebEngineWidgets import *
from Thread import getartThread,updateurlsThread,saveachethread
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
# 主对话框


class artobject():
    def __init__(self, parent=None):
        self.filename=""
        self.path=""
        self.allpath=""
        self.data=""
        self.datastr=""

class main(QMainWindow):
    # 图片改变信号
    imagechangedSignal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        # todo:软件配置
        self.setFont(QFont("Microsoft YaHei", 12))
        self.setWindowTitle('论文下载软件')
        # self.setWindowIcon(QIcon('xyjk.png'))
        # self.progressBar = QProgressBar()
        # self.progressBar.setVisible(False)
        # self.statusBar().addPermanentWidget(self.progressBar)
        # self.setStyleSheet("background-color:rgb(198,47,47,115);")
        self.move(20, 10)
        self.grid = QGridLayout()
        # 文件名输入框
        self.textedit=QTextEdit()
        self.grid.addWidget(self.textedit,0,0,1,2)



        self.urls=[]
        self.arts=[]
        self.time=0
        self.savepath=os.getcwd()+"/savefile/"
        self.achepath = os.getcwd() + "/history.ache"
        self.savepathachepath = os.getcwd() + "/savepath.ache"

        self.list1 = QTableWidget()
        # self.list1 = QTableWidget()
        self.list1.setColumnCount(3)
        self.list1.setRowCount(0)
        self.list1.clicked.connect(self.list1clicked)
        self.list1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list1.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list1.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list1.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.list1.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.list1.setDragDropMode(QAbstractItemView.InternalMove)
        # self.list1.setVerticalHeaderLabels(["论文名称"])
        self.list1.setHorizontalHeaderLabels(["论文名称","文件路径","保存时间"])
        self.grid.addWidget(self.list1,0,1,1,2)
        
        
        self.listDetailed = QTableWidget()
        # self.listDetailed = QTableWidget()
        self.listDetailed.setColumnCount(3)
        self.listDetailed.setRowCount(0)
        self.listDetailed.clicked.connect(self.listDetailedclicked)
        self.listDetailed.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.listDetailed.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.listDetailed.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listDetailed.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listDetailed.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listDetailed.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.listDetailed.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.listDetailed.setDragDropMode(QAbstractItemView.InternalMove)
        # self.listDetailed.setVerticalHeaderLabels(["论文名称"])
        self.listDetailed.setVerticalHeaderLabels(["论文名称","文件路径","保存时间"])
        self.grid.addWidget(self.listDetailed,0,1,1,2)

        self.savepathlineedit=QLineEdit()
        self.savepathlineedit.setText(self.savepath)
        self.savepathlineedit.setReadOnly(True)
        self.grid.addWidget(self.savepathlineedit, 1, 0, 1, 3)

        self.savepathbutton=QPushButton("保存路径")
        self.savepathbutton.clicked.connect(self.savepathbuttonclicked)
        self.grid.addWidget(self.savepathbutton, 1, 2, 1, 1)

        self.updataurlsbutton=QPushButton("更新可用线路")
        self.updataurlsbutton.clicked.connect(self.updateurls)
        self.grid.addWidget(self.updataurlsbutton, 2, 0, 1, 1)


        self.downloadbutton=QPushButton("开始下载")
        self.downloadbutton.clicked.connect(self.downloadbuttonclick)
        self.grid.addWidget(self.downloadbutton, 2, 1, 1, 1)


        self.widget=QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        self.loadache()
        self.updateurls()


    def list1clicked(self):
        print("self.fileindex:", self.list1.currentIndex().row())
        index=self.list1.currentIndex().row()
        filepath=self.arts[index].allpath
        os.startfile(filepath)




    def savepathbuttonclicked(self):
        path = QFileDialog.getExistingDirectory(self, "请选择文章保存目录")
        if path != "":
            self.savepath=path
            # temppath, tempfilename = os.path.split(self.savepathachepath)
            if (not os.path.exists(self.savepathachepath)):
                os.makedirs(self.savepathachepath)
            with open(self.savepathachepath, "wb") as file:
                pickle.dump(self.savepath, file, True)


    def updateurls(self):
        self.updateurlsthread=updateurlsThread()
        self.updateurlsthread.messageSingle.connect(self.statusBar().showMessage)
        self.updateurlsthread.enddingSingle.connect(self.dateurlsendding)
        self.updateurlsthread.start()

    def dateurlsendding(self,urls):
        self.urls=urls
        if len(self.urls)!=0:
            self.statusBar().showMessage("线路获取成功！")
        else:
            self.statusBar().showMessage("所有线路获取失败！（请检查网络连接）")

    def downloadbuttonclick(self):
        title=self.textedit.toPlainText()

        if len(self.urls)==0:
            self.statusBar().showMessage("请更新线路信息！")
            return
        self.getartthread=getartThread(self.urls,title,self.savepath)
        self.getartthread.messageSingle.connect(self.statusBar().showMessage)
        self.getartthread.enddingSingle.connect(self.getartend)
        self.getartthread.start()


    def getartend(self,path="",filename=""):
        if path!="" and filename!="":
            tempartobject=artobject()
            tempartobject.filename=filename
            tempartobject.path=path
            tempartobject.allpath=path+"/"+filename
            tempartobject.data=datetime.datetime.now()
            tempartobject.datastr=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
            exietindex=[index for index in range(len(self.arts)) if self.arts[index].filename==tempartobject.filename]
            if len(exietindex)!=0:
                self.arts.pop(exietindex[0])
            self.arts.insert(0, tempartobject)
        self.list1.clearContents()
        self.list1.setRowCount(len(self.arts))
        self.list1.setColumnCount(3)
        for i in range(len(self.arts)):
            self.list1.setItem(i, 0,QTableWidgetItem(str(self.arts[i].filename)))
            self.list1.setItem(i, 1,QTableWidgetItem(str(self.arts[i].path)))
            self.list1.setItem(i, 2,QTableWidgetItem(str(self.arts[i].datastr)))
        self.saveache()

    def saveache(self):
        print(self.achepath)
        self.saveachethread=saveachethread(self.achepath,self.arts)
        self.saveachethread.messageSingle.connect(self.statusBar().showMessage)
        # self.saveachethread.enddingSingle.connect(self.getartend)
        self.saveachethread.start()

    def loadache(self):
        if os.path.exists(self.achepath):
            f = open(self.achepath, 'rb')
            self.arts = pickle.load(f)
            self.statusBar().showMessage("已加载缓存信息！")
            self.getartend()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())