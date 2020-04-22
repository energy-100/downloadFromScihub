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
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QFont
from PyQt5 import QtCore
import os
from PyQt5 import QtGui, QtWidgets
from os import startfile
import sys
from PyQt5.QtWidgets import *

from PyQt5.QtCore import *
import time
from PyQt5.QtWebEngineWidgets import *
from Thread2 import getartThread, updateurlsThread, saveachethread,translatethread,savefilethread,artobject
from googletrans import Translator
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

# 主对话框



class main(QMainWindow):
    # 图片改变信号
    imagechangedSignal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        # todo:软件配置
        self.setFont(QFont("Microsoft YaHei", 12))
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('论文检索&下载程序')
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progressBar)
        # self.setWindowIcon(QIcon('xyjk.png'))
        # self.progressBar = QProgressBar()
        # self.progressBar.setVisible(False)
        # self.statusBar().addPermanentWidget(self.progressBar)
        # self.setStyleSheet("background-color:rgb(198,47,47,115);")
        self.move(20, 10)
        self.grid = QGridLayout()
        # 文件名输入框
        # self.textedit = QTextEdit()
        # self.grid.addWidget(self.textedit, 2, 0, 1, 2)

        self.urls = []
        self.arts = []
        self.artlist=[]
        self.time = 0
        self.page=1
        self.trans=True
        self.savepath = os.getcwd() + "/savefile/"
        self.achepath = os.getcwd() + "/history.ache"
        self.savepathachepath = os.getcwd() + "/savepath.ache"

        self.titletextedit=QLineEdit()
        self.titletextedit.setPlaceholderText('请输入或粘贴关键词！')
        # self.titletextedit.returnPressed.connect(lambda: self.inLineEditfinished())
        self.titletextedit.textChanged.connect(lambda: self.titletexteditChanged())
        self.grid.addWidget(self.titletextedit, 0, 0, 1, 10)

        self.titlechinesetextedit=QLineEdit()
        self.titlechinesetextedit.setPlaceholderText('关键词中文')
        self.titlechinesetextedit.setReadOnly(True)
        # self.titletextedit.returnPressed.connect(lambda: self.inLineEditfinished())
        # self.titlechinesetextedit.textChanged.connect(lambda: self.inLineEditfinished())
        self.grid.addWidget(self.titlechinesetextedit, 1, 0, 1, 10)

        self.artlistlabel=QLabel("检索列表")
        self.grid.addWidget(self.artlistlabel, 2, 0, 1, 5)

        self.artinflabel=QLabel("文章详细信息")
        self.grid.addWidget(self.artinflabel, 2, 5, 1, 5)

        self.artlistTable = QTableWidget()
        # self.artlistTable = QTableWidget()
        self.artlistTable.setColumnCount(1)
        self.artlistTable.setRowCount(0)
        self.artlistTable.clicked.connect(self.artlistTableclicked)
        self.artlistTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.artlistTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.artlistTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.artlistTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.artlistTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.artlistTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.artlistTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.artlistTable.setDragDropMode(QAbstractItemView.InternalMove)
        # self.artlistTable.setVerticalHeaderLabels(["论文名称"])
        self.artlistTable.setHorizontalHeaderLabels(["文章名称"])
        self.grid.addWidget(self.artlistTable, 3, 0, 1, 5)

        self.artInfTable = QTableWidget()
        # self.artInfTable = QTableWidget()
        self.artInfTable.setColumnCount(1)
        self.artInfTable.setRowCount(5)
        # self.artInfTable.clicked.connect(self.artInfTableclicked)
        self.artInfTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.artInfTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.artInfTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.artInfTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.artInfTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.artInfTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.artInfTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.artInfTable.setDragDropMode(QAbstractItemView.InternalMove)
        # self.artInfTable.setVerticalHeaderLabels(["论文名称"])
        self.artInfTable.setVerticalHeaderLabels(["文章名称","中文名称", "作者", "期刊","DOI","文章地址"])
        self.artInfTable.setHorizontalHeaderLabels(["文章信息"])
        self.grid.addWidget(self.artInfTable, 3, 5, 2, 5)


        self.artdownloadlabel=QLabel("历史下载文章列表")
        self.grid.addWidget(self.artdownloadlabel, 5, 0, 1, 5)

        self.downloadedartlistTable = QTableWidget()
        # self.downloadedartlistTable = QTableWidget()
        self.downloadedartlistTable.setColumnCount(3)
        self.downloadedartlistTable.setRowCount(0)
        self.downloadedartlistTable.doubleClicked.connect(self.downloadedartlistTableclicked)
        self.downloadedartlistTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.downloadedartlistTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.downloadedartlistTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.downloadedartlistTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.downloadedartlistTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.downloadedartlistTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.downloadedartlistTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.downloadedartlistTable.setDragDropMode(QAbstractItemView.InternalMove)
        # self.downloadedartlistTable.setVerticalHeaderLabels(["论文名称"])
        self.downloadedartlistTable.setHorizontalHeaderLabels(["论文名称", "文件路径", "保存时间"])
        self.grid.addWidget(self.downloadedartlistTable, 6, 0, 1, 10)

        # self.listDetailed = QTableWidget()
        # # self.listDetailed = QTableWidget()
        # self.listDetailed.setColumnCount(3)
        # self.listDetailed.setRowCount(0)
        # self.listDetailed.clicked.connect(self.listDetailedclicked)
        # self.listDetailed.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.listDetailed.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.listDetailed.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.listDetailed.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.listDetailed.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.listDetailed.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        # self.listDetailed.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        # self.listDetailed.setDragDropMode(QAbstractItemView.InternalMove)
        # # self.listDetailed.setVerticalHeaderLabels(["论文名称"])
        # self.listDetailed.setVerticalHeaderLabels(["论文名称", "文件路径", "保存时间"])
        # self.grid.addWidget(self.listDetailed, 0, 1, 1, 2)

        self.prebutton = QPushButton("上一页")
        self.prebutton.clicked.connect(self.prebuttonclick)
        self.grid.addWidget(self.prebutton, 4, 0, 1, 1)

        self.nextbutton = QPushButton("下一页")
        self.nextbutton.clicked.connect(self.nextbuttonclick)
        self.grid.addWidget(self.nextbutton, 4, 1, 1, 1)

        self.pagelabel=QLabel("当前页码:")
        self.grid.addWidget(self.pagelabel, 4, 2, 1, 1)

        self.renovatebutton = QPushButton("刷新检索列表")
        self.renovatebutton.clicked.connect(self.renovatebuttonclick)
        self.grid.addWidget(self.renovatebutton, 4, 3, 1, 1)

        self.downloadbutton = QPushButton("下载文章")
        self.downloadbutton.clicked.connect(self.downloadbuttonclick)
        self.grid.addWidget(self.downloadbutton, 4, 4, 1, 1)

        self.savepathlineedit = QLineEdit()
        self.savepathlineedit.setText(self.savepath)
        self.savepathlineedit.setReadOnly(True)
        self.grid.addWidget(self.savepathlineedit, 7, 0, 1, 4)

        self.savepathbutton = QPushButton("更改保存路径")
        self.savepathbutton.clicked.connect(self.savepathbuttonclicked)
        self.grid.addWidget(self.savepathbutton, 7, 4, 1, 1)

        self.openpathbutton = QPushButton("打开保存路径")
        self.openpathbutton.clicked.connect(self.openpathbuttonclicked)
        self.grid.addWidget(self.openpathbutton, 7, 5, 1, 1)

        self.updataurlsbutton = QPushButton("更新可用线路")
        self.updataurlsbutton.clicked.connect(self.updateurls)
        self.grid.addWidget(self.updataurlsbutton, 7, 6, 1, 1)

        self.transcheck = QCheckBox("检索时翻译标题")
        self.transcheck.stateChanged.connect(self.transcheckselect)
        self.transcheck.setChecked(self.trans)
        self.grid.addWidget(self.transcheck, 7, 7, 1, 1)
        #
        # self.codelabel=QLabel()
        # self.grid.addWidget(self.transcheck, 8, 1, 1, 10)

        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        self.loadache()
        self.updateurls()

    def prebuttonclick(self):
        if self.page==1:
            self.statusBar().showMessage("已到最前页！")
            return
        self.page -= 1
        self.pagelabel.setText("当前页码:"+str(self.page))
        self.getartthread=getartThread(self.urls,self.titletextedit.text(),self.trans,self.page)
        self.getartthread.messageSingle.connect(self.statusBar().showMessage)
        self.getartthread.enddingSingle.connect(self.getartend)
        self.getartthread.start()

    def nextbuttonclick(self):
        self.page += 1
        self.pagelabel.setText("当前页码:"+str(self.page))
        self.getartthread=getartThread(self.urls,self.titletextedit.text(),self.trans,self.page)
        self.getartthread.messageSingle.connect(self.statusBar().showMessage)
        self.getartthread.enddingSingle.connect(self.getartend)
        self.getartthread.start()

    def titletexteditChanged(self):
        if self.titletextedit.text() =="":
            return
        self.pagelabel.setText("当前页码:"+str(self.page))
        self.translatethread=translatethread(self.titletextedit.text())
        self.translatethread.enddingSingle.connect(self.titlechinesetextedit.setText)
        self.translatethread.start()

        self.getartthread=getartThread(self.urls,self.titletextedit.text(),self.trans)
        self.getartthread.messageSingle.connect(self.statusBar().showMessage)
        self.getartthread.enddingSingle.connect(self.getartend)
        self.getartthread.start()

    def artlistTableclicked(self):
        index=self.artlistTable.currentIndex().row()
        print(index)
        if index == -1 :
            return
        self.artInfTable.clearContents()
        self.artInfTable.setItem(0, 0, QTableWidgetItem(str(self.artlist[index].title)))
        self.artInfTable.setItem(1, 0, QTableWidgetItem(str(self.artlist[index].chinesetitle)))
        self.artInfTable.setItem(2, 0, QTableWidgetItem(str(self.artlist[index].authors)))
        self.artInfTable.setItem(3, 0, QTableWidgetItem(str(self.artlist[index].extra)))
        self.artInfTable.setItem(4, 0, QTableWidgetItem(str(self.artlist[index].doi)))
        self.artInfTable.setItem(5, 0, QTableWidgetItem(str(self.artlist[index].arturl)))


    def openpathbuttonclicked(self):
        if(os.path.exists(self.savepath)):
            startfile(self.savepath)  # 打开文件夹窗口
        else:
            self.statusBar().showMessage("文件夹不存在，请检查！")

    def downloadedartlistTableclicked(self):
        print("self.fileindex:", self.downloadedartlistTable.currentIndex().row())
        index = self.downloadedartlistTable.currentIndex().row()
        filepath = self.arts[index].allpath
        os.startfile(filepath)

    def renovatebuttonclick(self):
        self.titletexteditChanged()

    def transcheckselect(self):
        istrans=self.transcheck.isChecked()
        self.trans=istrans
        if istrans:
            self.statusBar().showMessage("启用检索翻译功能会降低检索速度")

    def savepathbuttonclicked(self):
        path = QFileDialog.getExistingDirectory(self, "请选择文章保存目录")
        if path != "":
            self.savepath = path
            # temppath, tempfilename = os.path.split(self.savepathachepath)
            if (not os.path.exists(self.savepathachepath)):
                os.makedirs(self.savepathachepath)
            with open(self.savepathachepath, "wb") as file:
                pickle.dump(self.savepath, file, True)

    def updateurls(self):
        self.updateurlsthread = updateurlsThread()
        self.updateurlsthread.messageSingle.connect(self.statusBar().showMessage)
        self.updateurlsthread.enddingSingle.connect(self.dateurlsendding)
        self.updateurlsthread.start()

    def dateurlsendding(self, urls):
        self.urls = urls
        if len(self.urls) != 0:
            self.statusBar().showMessage("线路获取成功！")
        else:
            self.statusBar().showMessage("所有线路获取失败！（请检查网络连接）")

    def downloadbuttonclick(self):
        title = self.titletextedit.text()
        index = self.artlistTable.currentIndex().row()
        art=self.artlist[index]

        if len(self.urls) == 0:
            self.statusBar().showMessage("请更新线路信息！")
            return
        self.savefilethread = savefilethread(self.urls[0], art, self.savepath)
        self.savefilethread.messageSingle.connect(self.statusBar().showMessage)
        self.savefilethread.enddingSingle.connect(self.savefileend)
        self.savefilethread.progressSingle.connect(self.progressBar.setValue)
        self.savefilethread.progressvisualSingle.connect(self.progressBar.setVisible)
        self.savefilethread.codeimageSingle.connect(self.showcode)
        self.savefilethread.start()

    def showcode(self,image):
        # res = requests.get(image)
        # img = QImage.fromData(res.content)
        self.codelabel.setPixmap(image)



    def savefileend(self,art=[]):
        if art!=[]:
            self.arts.append(art)
            exietindex = [index for index in range(len(self.arts)) if
                              self.arts[index].title == art.title]
            if len(exietindex) != 0:
                self.arts.pop(exietindex[0])
            self.arts.insert(0, art)
        self.downloadedartlistTable.clearContents()
        self.downloadedartlistTable.setRowCount(len(self.arts))
        self.downloadedartlistTable.setColumnCount(3)
        for i in range(len(self.arts)):
            self.downloadedartlistTable.setItem(i, 0, QTableWidgetItem(str(self.arts[i].title)))
            self.downloadedartlistTable.setItem(i, 1, QTableWidgetItem(str(self.arts[i].path)))
            self.downloadedartlistTable.setItem(i, 2, QTableWidgetItem(str(self.arts[i].datastr)))
        self.saveache()


    def getartend(self, artlist=[]):
        if artlist != []:
            self.artlist=artlist
            self.artlistTable.clearContents()
            self.artlistTable.setRowCount(len(artlist))
            self.artlistTable.setColumnCount(1)
            for i,art in enumerate(artlist):
                self.statusBar().showMessage("正在加载数据 "+str(i+1)+"/"+str(len(artlist)))
                self.artlistTable.setItem(i, 0, QTableWidgetItem(str(art.title)))

            self.artInfTable.clearContents()
            self.artInfTable.setItem(0, 0, QTableWidgetItem(str(artlist[0].title)))
            self.artInfTable.setItem(1, 0, QTableWidgetItem(str(artlist[0].chinesetitle)))
            self.artInfTable.setItem(2, 0, QTableWidgetItem(str(artlist[0].authors)))
            self.artInfTable.setItem(3, 0, QTableWidgetItem(str(artlist[0].extra)))
            self.artInfTable.setItem(4, 0, QTableWidgetItem(str(artlist[0].doi)))
            self.artInfTable.setItem(5, 0, QTableWidgetItem(str(artlist[0].arturl)))
            self.statusBar().showMessage("检索成功!")
        else:
            self.statusBar().showMessage("检索失败!")


        #     tempartobject = artobject()
        #     tempartobject.filename = filename
        #     tempartobject.path = path
        #     tempartobject.allpath = path + "/" + filename
        #     tempartobject.data = datetime.datetime.now()
        #     tempartobject.datastr = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
        #     exietindex = [index for index in range(len(self.arts)) if
        #                   self.arts[index].filename == tempartobject.filename]
        #     if len(exietindex) != 0:
        #         self.arts.pop(exietindex[0])
        #     self.arts.insert(0, tempartobject)
        # self.downloadedartlistTable.clearContents()
        # self.downloadedartlistTable.setRowCount(len(self.arts))
        # self.downloadedartlistTable.setColumnCount(3)
        # for i in range(len(self.arts)):
        #     self.downloadedartlistTable.setItem(i, 0, QTableWidgetItem(str(self.arts[i].filename)))
        #     self.downloadedartlistTable.setItem(i, 1, QTableWidgetItem(str(self.arts[i].path)))
        #     self.downloadedartlistTable.setItem(i, 2, QTableWidgetItem(str(self.arts[i].datastr)))
        # self.saveache()

    def saveache(self):
        print(self.achepath)
        self.saveachethread = saveachethread(self.achepath, self.arts)
        self.saveachethread.messageSingle.connect(self.statusBar().showMessage)
        # self.saveachethread.enddingSingle.connect(self.getartend)
        self.saveachethread.start()

    def loadache(self):
        if os.path.exists(self.achepath):
            f = open(self.achepath, 'rb')
            self.arts = pickle.load(f)
            self.savefileend()
            self.statusBar().showMessage("已加载缓存信息！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())