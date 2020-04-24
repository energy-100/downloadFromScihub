
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
import pickle
import os
from PyQt5.QtGui import QImage, QFont
from PyQt5 import QtCore
import os
from PyQt5 import QtGui, QtWidgets
from os import startfile
import sys
from PyQt5.QtWidgets import *
from Thread2 import getartThread, updateurlsThread, saveachethread,translatethread,savefilethread,artobject,updateurlsThreadsingle
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')


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
        self.allurls = [
            "https://sci-hub.tw",
            "https://sci-hub.sci-hub.tw",
            "https://sci-hub.hk",
            "https://sci-hub.sci-hub.hk",
            "https://sci-hub.la",
            "https://sci-hub.mn",
            "https://sci-hub.name",
            "https://sci-hub.is",
            "https://sci-hub.tv",
            "https://sci-hub.ws",
            "https://www.sci-hub.cn",
            "https://sci-hub.sci-hub.mn",
            "https://sci-hub.sci-hub.tv"]


        self.urlsable = []
        self.urls = dict()
        self.arts = []
        self.artlist=[]
        self.time = 0
        self.page=1
        self.trans=True
        self.updateurling=False
        self.transconnect=True
        self.searchconnect=True
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


        self.artdownloadlabel=QLabel("历史下载文章列表(单击查看详细信息，双击打开)")
        self.grid.addWidget(self.artdownloadlabel, 5, 0, 1, 5)

        self.downloadedartlistTable = QTableWidget()
        # self.downloadedartlistTable = QTableWidget()
        self.downloadedartlistTable.setColumnCount(3)
        self.downloadedartlistTable.setRowCount(0)
        self.downloadedartlistTable.doubleClicked.connect(self.downloadedartlistTabledoubleclicked)
        self.downloadedartlistTable.clicked.connect(self.downloadedartlistTableclicked)
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
        self.grid.addWidget(self.downloadedartlistTable, 6, 0, 1, 7)

        self.artdownloadlabel=QLabel("线路信息")
        self.grid.addWidget(self.artdownloadlabel, 5, 7, 1, 1)

        self.channellistTable = QTableWidget()
        # self.downloadedartlistTable = QTableWidget()
        self.channellistTable.setColumnCount(2)
        self.channellistTable.setRowCount(len(self.allurls)+2)
        self.channellistTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.channellistTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.channellistTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.channellistTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.channellistTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.channellistTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.channellistTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.channellistTable.setDragDropMode(QAbstractItemView.InternalMove)
        # self.downloadedartlistTable.setVerticalHeaderLabels(["论文名称"])
        self.channellistTable.setHorizontalHeaderLabels(["线路", "连接时间"])

        self.channellistTable.setItem(0, 0, QTableWidgetItem("检索线路"))
        self.channellistTable.setItem(1, 0, QTableWidgetItem("翻译线路"))
        for i,url in enumerate(self.allurls):
            self.channellistTable.setItem(i+2, 0, QTableWidgetItem(str(url)))

        self.grid.addWidget(self.channellistTable, 6, 7, 1, 3)


        self.prebutton = QPushButton("上一页")
        self.prebutton.clicked.connect(self.prebuttonclick)
        self.grid.addWidget(self.prebutton, 4, 0, 1, 1)

        self.nextbutton = QPushButton("下一页")
        self.nextbutton.clicked.connect(self.nextbuttonclick)
        self.grid.addWidget(self.nextbutton, 4, 1, 1, 1)

        self.pagelabel=QLabel("当前页码:")
        self.grid.addWidget(self.pagelabel, 2, 3, 1, 1)

        self.renovatebutton = QPushButton("刷新检索列表")
        self.renovatebutton.clicked.connect(self.renovatebuttonclick)
        self.grid.addWidget(self.renovatebutton, 2, 4, 1, 1)

        self.downloadtitlebutton = QPushButton("根据输入下载文章")
        self.downloadtitlebutton.clicked.connect(self.downloadtitlebuttonclick)
        self.grid.addWidget(self.downloadtitlebutton, 4, 2, 1, 1)

        self.downloadbutton = QPushButton("下载文章")
        self.downloadbutton.clicked.connect(self.downloadbuttonclick)
        self.grid.addWidget(self.downloadbutton, 4, 4, 1, 1)

        self.deletedownloadartbutton = QPushButton("删除选中文章")
        self.deletedownloadartbutton.clicked.connect(self.deletedownloadartbuttonclick)
        self.grid.addWidget(self.deletedownloadartbutton, 5, 6, 1, 1)

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
        self.grid.addWidget(self.updataurlsbutton, 5, 9, 1, 1)

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
        self.updateurls()
        self.loadache()

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

    def downloadtitlebuttonclick(self):
        title = self.titletextedit.text()
        art=artobject()
        art.title=title
        if len(self.urlsable) == 0:
            self.statusBar().showMessage("请更新线路信息！")
            return
        url=min(self.urls,key=lambda x:self.urls[x])
        self.savefilethread = savefilethread(url, art, self.savepath)
        self.savefilethread.messageSingle.connect(self.statusBar().showMessage)
        self.savefilethread.enddingSingle.connect(self.savefileend)
        self.savefilethread.progressSingle.connect(self.progressBar.setValue)
        self.savefilethread.progressvisualSingle.connect(self.progressBar.setVisible)
        self.savefilethread.codeimageSingle.connect(self.showcode)
        self.savefilethread.start()


    def titletexteditChanged(self):
        if self.titletextedit.text() =="":
            return
        if self.trans:
            self.pagelabel.setText("当前页码:"+str(self.page))
            self.translatethread=translatethread(self.titletextedit.text())
            self.translatethread.enddingSingle.connect(self.titlechinesetextedit.setText)
            self.translatethread.start()

        self.getartthread=getartThread(" ",self.titletextedit.text(),self.trans)
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

    def deletedownloadartbuttonclick(self):
        index=self.downloadedartlistTable.currentIndex().row()
        art=self.arts.pop(index)
        if os.path.exists(art.allpath):
            try:
                os.remove(art.allpath)
            except Exception as a:
                print(a)
        self.savefileend()

    def openpathbuttonclicked(self):
        if(os.path.exists(self.savepath)):
            startfile(self.savepath)  # 打开文件夹窗口
        else:
            self.statusBar().showMessage("文件夹不存在，请检查！")

    def downloadedartlistTabledoubleclicked(self):
        print("self.fileindex:", self.downloadedartlistTable.currentIndex().row())
        index = self.downloadedartlistTable.currentIndex().row()
        filepath = self.arts[index].allpath
        if os.path.exists(filepath):
            self.statusBar().showMessage("正在打开文件--"+self.arts[index].title)
            os.startfile(filepath)
        else:
            self.statusBar().showMessage("文件已被删除，请重新下载！")

    def downloadedartlistTableclicked(self):
        print("self.fileindex:", self.downloadedartlistTable.currentIndex().row())
        index = self.downloadedartlistTable.currentIndex().row()
        self.artInfTable.clearContents()
        self.artInfTable.setItem(0, 0, QTableWidgetItem(str(self.arts[index].title)))
        self.artInfTable.setItem(1, 0, QTableWidgetItem(str(self.arts[index].chinesetitle)))
        self.artInfTable.setItem(2, 0, QTableWidgetItem(str(self.arts[index].authors)))
        self.artInfTable.setItem(3, 0, QTableWidgetItem(str(self.arts[index].extra)))
        self.artInfTable.setItem(4, 0, QTableWidgetItem(str(self.arts[index].doi)))
        self.artInfTable.setItem(5, 0, QTableWidgetItem(str(self.arts[index].arturl)))

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
        if self.updateurling:
            self.statusBar().showMessage("线路更新线程已在运行...")
            return
        self.updateurling=True
        self.urlsable=[]
        self.urls=dict()
        # self.channellistTable.removeColumn(2)

        self.updategoogleurlsthread = updateurlsThreadsingle("https://translate.google.cn/")
        self.updategoogleurlsthread.messageSingle.connect(self.statusBar().showMessage)
        self.updategoogleurlsthread.enddingSingle.connect(self.dateurlsendding)
        self.updategoogleurlsthread.start()

        self.updatecrossrefurlsthread = updateurlsThreadsingle("https://www.crossref.org/")
        self.updatecrossrefurlsthread.messageSingle.connect(self.statusBar().showMessage)
        self.updatecrossrefurlsthread.enddingSingle.connect(self.dateurlsendding)
        self.updatecrossrefurlsthread.start()

        for i in range(self.channellistTable.rowCount()):
            self.channellistTable.setItem(i, 1, QTableWidgetItem("更新中..."))
            self.channellistTable.item(i, 1).setBackground(QtGui.QColor(233, 255, 80))
        names = locals()
        for i,url in enumerate(self.allurls):
            exec('self.updateurlsthread{} = updateurlsThreadsingle(url)'.format(i))
            exec('self.updateurlsthread{}.messageSingle.connect(self.statusBar().showMessage)'.format(i))
            exec('self.updateurlsthread{}.enddingSingle.connect(self.dateurlsendding)'.format(i))
            exec('self.updateurlsthread{}.start()'.format(i))
            # self.updateurlsthread = updateurlsThreadsingle(url)
            # self.updateurlsthread.messageSingle.connect(self.statusBar().showMessage)
            # self.updateurlsthread.enddingSingle.connect(self.dateurlsendding)
            # self.updateurlsthread.start()

            # updateurlsthread = updateurlsThread()
        # updateurlsthread = updateurlsThread()
        # updateurlsthread.messageSingle.connect(self.statusBar().showMessage)
        # updateurlsthread.enddingSingle.connect(self.dateurlsendding)
        # updateurlsthread.start()

    def dateurlsendding(self, url,time):
        if url == "https://translate.google.cn/":
            index=1
            if time>10:
                self.trans=False
                print("self.trans",self.trans)
                self.transcheck.setChecked(self.trans)
                self.downloadedartlistTable.setItem(1, 0, QTableWidgetItem("翻译线路(已自动关闭)"))
            else:
                self.downloadedartlistTable.setItem(1, 0, QTableWidgetItem("翻译线路"))
        elif url == "https://www.crossref.org/":
            index = 0



        else:
            self.urls[url] = time
            index = self.allurls.index(url) + 2
            if time < 9999:
                self.urlsable.append(url)

        if time<9999:
            self.channellistTable.setItem(index, 1, QTableWidgetItem(str(time)+"s"))
            self.statusBar().showMessage(url+"线路连接成功！（连接时间"+str(time)+"s）")
            print(url+"线路连接成功！（连接时间"+str(time)+"s）")
            self.channellistTable.item(index, 1).setBackground(QtGui.QColor(80, 255, 80))
        elif time==10000:
            self.channellistTable.setItem(index, 1, QTableWidgetItem("返回值异常"))
            # self.statusBar().showMessage(url + "返回值异常！")
            print(url + "返回值异常！")
            self.channellistTable.item(index, 1).setBackground(QtGui.QColor(255, 80, 80))

        else:
            self.channellistTable.setItem(index, 1, QTableWidgetItem("超时"))
            # self.statusBar().showMessage(url+"线路超时！")
            print(url+"线路超时！")
            self.channellistTable.item(index, 1).setBackground(QtGui.QColor(255, 80, 80))
        if len(self.urls)==len(self.allurls):
            self.statusBar().showMessage("线路更新完成！（可用"+str(len(self.urlsable))+"/"+str(len(self.allurls))+")")
            self.updateurling=False

    def downloadbuttonclick(self):
        title = self.titletextedit.text()
        index = self.artlistTable.currentIndex().row()
        art=self.artlist[index]

        if len(self.urlsable) == 0:
            self.statusBar().showMessage("请更新线路信息！")
            return
        url = min(self.urls, key=lambda x: self.urls[x])
        self.savefilethread = savefilethread(url, art, self.savepath)
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
            # self.arts.append(art)
            exietindex = [index for index in range(len(self.arts)) if
                              self.arts[index].title == art.title]
            if len(exietindex) != 0:
                self.arts.pop(exietindex[0])
            self.arts.insert(0, art)
        self.downloadedartlistTable.clearContents()
        [self.arts.remove(art) for art in self.arts if not os.path.exists(art.allpath)]
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
            try:
                f = open(self.achepath, 'rb')
                self.arts = pickle.load(f)
                f.close()
                self.savefileend()
                self.statusBar().showMessage("已加载缓存信息！")
            except Exception as a:
                print("读取历史数据错误"+str(a))
            print("已加载缓存信息！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())