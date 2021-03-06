import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.picture_gui import runimage
from gui.cameraset import Camera
import os
from gui.yolo_gui_vedio import YOLO
from PIL import Image
import numpy as np
import cv2
import time
import tensorflow as tf
import threading
import datetime


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("火焰烟雾检测系统")
        self.resize(1080, 760)
        self.bar = self.menuBar()
        self.setup = self.bar.addMenu("配置")
        self.help = self.bar.addMenu("帮助")
        self.exit = self.bar.addMenu("退出")
        self.toolbar = QToolBar()
        self.toolbar = self.addToolBar("工具栏")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        '''------------------config------------------'''
        mainpath = os.getcwd()
        self.name = []
        self.guiimgpath = mainpath+'/guiimg/'
        self.setuppath = mainpath+'/setup'
        self.default_imgsavepath = mainpath+'/outimage'
        self.camsetpath = mainpath+'/camsetup/camset.txt'
        self.recordpath = mainpath + '/record'
        '''------------------------------------------'''
        self.curr_time = datetime.datetime.now()
        self.time_str = datetime.datetime.strftime(self.curr_time, '%Y-%m-%d %H:%M:%S')
        self.time_record = datetime.datetime.strftime(self.curr_time, '%Y.%m.%d.%H.%M')
        self.createset = QAction("新建场景")
        self.createset.setShortcut("Ctrl+N")
        self.createset.triggered.connect(self.CreateSit)
        self.deleteset = QAction("删除场景")
        self.deleteset.setShortcut("Ctrl+D")
        self.deleteset.triggered.connect(self.DeleteSit)
        self.camera = QAction("摄像头设置")
        self.camera.setShortcut("Ctrl+C")
        self.camera.triggered.connect(self.cameraset)
        self.setup.addAction(self.createset)
        self.setup.addAction(self.deleteset)
        self.setup.addAction(self.camera)

        self.connectus = QAction("联系我们")
        self.connectus.triggered.connect(self.connect_us)
        self.help.addAction(self.connectus)

        self.exitsys = QAction("退出系统")
        self.exitsys.setShortcut("Ctrl+E")
        self.exitsys.triggered.connect(self.onClick_exit)
        self.exit.addAction(self.exitsys)

        self.newsit = QAction(QIcon(self.guiimgpath+'newsit.png'), "新建场景", self)
        self.newsit.triggered.connect(self.CreateSit)
        self.toolbar.addAction(self.newsit)
        self.delete = QAction(QIcon(self.guiimgpath+'delete.png'), "删除场景", self)
        self.delete.triggered.connect(self.DeleteSit)
        self.toolbar.addAction(self.delete)
        self.newcamera = QAction(QIcon(self.guiimgpath+'camera.png'), "摄像头配置", self)
        self.newcamera.triggered.connect(self.cameraset)
        self.toolbar.addAction(self.newcamera)
        self.picture = QAction(QIcon(self.guiimgpath+'picture.png'), "图像识别", self)
        self.picture.triggered.connect(self.picturemode)
        self.toolbar.addAction(self.picture)
        self.record = QAction(QIcon(self.guiimgpath+'record.png'), "查看日志", self)
        self.record.triggered.connect(self.recordshow)
        self.toolbar.addAction(self.record)
        self.exitsystool = QAction(QIcon(self.guiimgpath+'exit.png'), "退出系统", self)
        self.exitsystool.triggered.connect(self.onClick_exit)
        self.toolbar.addAction(self.exitsystool)

        self.status = self.statusBar()
        self.status.showMessage('欢迎进入明火烟雾检测系统！', 5000)
        self.createright()
        self.createleft()
        self.createdown()
        self.mainbox = QWidget()
        self.mainlayout = QGridLayout()
        self.mainlayout.addWidget(self.leftBox, 0, 0, 5, 1)
        self.mainlayout.addWidget(self.rightBox, 0, 1, 5, 4)
        self.mainlayout.addWidget(self.downBox, 5, 0, 2, 5)
        self.mainbox.setLayout(self.mainlayout)
        self.setCentralWidget(self.mainbox)
        self.showinfo.append(self.time_str+' 欢迎进入明火烟雾智能检测系统！')
    '''------------------新建场景------------------'''
    def CreateSit(self):
        self.createdialog = QDialog()
        self.createdialog.setWindowTitle('新建应用场景')
        self.createdialog.setWindowModality(Qt.ApplicationModal)

        self.nameLabel = QLabel('&Name', self)
        self.nameLabel.setText('场景名称(&N)')
        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.setPlaceholderText('请输入新建场景名称')
        # 设置伙伴控件
        self.nameLabel.setBuddy(self.nameLineEdit)

        self.weightLabel = QLabel('&Weight', self)
        self.weightLabel.setText('场景权重(&W)')
        self.weightLineEdit = QLineEdit(self)
        self.weightLineEdit.setPlaceholderText('请输入场景权重文件地址')
        self.weightLabel.setBuddy(self.weightLineEdit)
        self.weightButton = QPushButton('加载权重')
        self.weightButton.clicked.connect(self.onClick_weight)

        self.classLabel = QLabel('&Class', self)
        self.classLabel.setText('场景类别(&C)')
        self.classLineEdit = QLineEdit(self)
        self.classLineEdit.setPlaceholderText('请输入场景类别文件地址')
        self.classLabel.setBuddy(self.classLineEdit)
        self.classButton = QPushButton('加载类别')
        self.classButton.clicked.connect(self.onClick_class)

        self.anchorLabel = QLabel('&Anchor', self)
        self.anchorLabel.setText('多窗口尺度(&C)')
        self.anchorLineEdit = QLineEdit(self)
        self.anchorLineEdit.setPlaceholderText('请输入Anchor文件地址')
        self.anchorLabel.setBuddy(self.anchorLineEdit)
        self.anchorButton = QPushButton('加载anchor')
        self.anchorButton.clicked.connect(self.onClick_anchor)

        self.btnOK = QPushButton('确定')
        self.btnOK.clicked.connect(self.savesetup)
        self.btnCancel = QPushButton('取消')
        self.btnCancel.clicked.connect(self.nameLineEdit.clear)
        self.btnCancel.clicked.connect(self.weightLineEdit.clear)
        self.btnCancel.clicked.connect(self.classLineEdit.clear)
        self.btnExit = QPushButton('退出')
        self.btnExit.clicked.connect(self.createdialog.reject)

        self.createLayout = QGridLayout(self)
        self.createLayout.addWidget(self.nameLabel, 0, 0)
        self.createLayout.addWidget(self.nameLineEdit, 0, 1, 1, 3)

        self.createLayout.addWidget(self.weightLabel, 1, 0)
        self.createLayout.addWidget(self.weightLineEdit, 1, 1, 1, 2)
        self.createLayout.addWidget(self.weightButton, 1, 3, 1, 1)

        self.createLayout.addWidget(self.classLabel, 2, 0)
        self.createLayout.addWidget(self.classLineEdit, 2, 1, 1, 2)
        self.createLayout.addWidget(self.classButton, 2, 3, 1, 1)

        self.createLayout.addWidget(self.anchorLabel, 3, 0)
        self.createLayout.addWidget(self.anchorLineEdit, 3, 1, 1, 2)
        self.createLayout.addWidget(self.anchorButton, 3, 3, 1, 1)

        self.createLayout.addWidget(self.btnOK, 4, 1)
        self.createLayout.addWidget(self.btnCancel, 4, 2)
        self.createLayout.addWidget(self.btnExit, 4, 3)
        self.createdialog.setLayout(self.createLayout)

        self.createdialog.exec()

    def savesetup(self):
        if self.nameLineEdit.text() != '':
            f = open(self.setuppath + '/' + self.nameLineEdit.text() + '.txt',
                     'w')
            f.write(self.weightLineEdit.text() + ' ' + self.classLineEdit.text()+ ' '+ self.anchorLineEdit.text())
            f.close()
            self.showinfo.append(self.time_str+' 已成功保存场景配置！')
            self.createdialog.reject()
            self.name = []
            self.setinfo()
            self.combox.clear()
            self.combox.addItems(self.name)

    def onClick_weight(self):
        weightpath, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.h5 )')
        self.weightLineEdit.setText(weightpath)
        self.showinfo.append(self.time_str+' 已成功载入场景权重！')

    def onClick_class(self):
        classpath, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.txt )')
        self.classLineEdit.setText(classpath)
        self.showinfo.append(self.time_str+' 已成功载入场景类别！')
    def onClick_anchor(self):
        anchorpath, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.txt )')
        self.anchorLineEdit.setText(anchorpath)
        self.showinfo.append(self.time_str+' 已成功载入anchor文件！')

    '''------------------联系我们------------------'''
    def connect_us(self):
        self.showinfo.append('请联系邮箱:zgshang@nuaa.edu.cn')
        QMessageBox.question(self, '信息', '请联系邮箱:zgshang@nuaa.edu.cn', QMessageBox.Yes)
    '''------------------查看日志------------------'''
    def recordshow(self):
        self.showinfo.append(self.time_str + ' 已打开视频检测日志')
        self.recordWindow()
    '''------------------日志查看窗口------------------'''
    def recordWindow(self):
        self.recorddialog = QDialog()
        self.recorddialog.setWindowTitle('查看日志')
        self.recorddialog.setWindowModality(Qt.ApplicationModal)

        self.recordnameLabel = QLabel('日志名称', self)
        self.recordnamecombox = QComboBox()
        self.recordnamecombox.setPlaceholderText('请选择要查看的日志名称')
        self.recordname = []
        def listdir(path, list_name):
            for file in os.listdir(path):
                file_path = file
                if os.path.isdir(file_path):
                    listdir(file_path, list_name)
                elif os.path.splitext(file_path)[1] == '.txt':
                    list_name.append(os.path.splitext(file_path)[0])
            return list_name
        self.recordname = listdir(self.recordpath, self.recordname)
        self.recordnamecombox.addItems(self.recordname)

        self.recordbtnDel = QPushButton('删除')
        self.recordbtnDel.clicked.connect(self.deleterecord)
        self.recordbtnOK = QPushButton('确定')
        self.recordbtnOK.clicked.connect(self.showrecord)
        self.recordbtnExit = QPushButton('退出')
        self.recordbtnExit.clicked.connect(self.recorddialog.reject)
        self.recordinfo = QTextBrowser()
        self.recordinfo.resize(640, 480)

        self.recordLayout = QGridLayout(self)
        self.recordLayout.addWidget(self.recordnameLabel, 0, 0, 1, 1)
        self.recordLayout.addWidget(self.recordnamecombox, 0, 1, 1, 2)
        self.recordLayout.addWidget(self.recordinfo, 1, 0, 1, 3)
        self.recordLayout.addWidget(self.recordbtnDel, 2, 0, 1, 1)
        self.recordLayout.addWidget(self.recordbtnOK, 2, 1, 1, 1)
        self.recordLayout.addWidget(self.recordbtnExit, 2, 2, 1, 1)
        self.recorddialog.setLayout(self.recordLayout)

        self.recorddialog.exec()

    def showrecord(self):
        self.filename = self.recordnamecombox.currentText()
        for _ in range(len(self.recordname)):
            if self.filename == self.recordname[_]:
                flag = 0
                break
            else:
                flag = 1
        if flag == 0:
            file = open(self.recordpath + '/' + self.filename + '.txt', "r")
            fileContent = file.read()
            file.close()
            self.recordinfo.append(fileContent)
            self.showinfo.append(self.time_str + ' 已成功显示日志！')
        else:
            self.showinfo.append(self.time_str + ' 请选择日志名称！')
            self.recordtipshow()

    def deleterecord(self):
        self.filename = self.recordnamecombox.currentText()
        for _ in range(len(self.recordname)):
            if self.filename == self.recordname[_]:
                flag = 0
                break
            else:
                flag = 1
        if flag == 0:
            filename = self.recordpath + '/' + self.recordnamecombox.currentText() + '.txt'
            os.remove(filename)
            self.showinfo.append(self.time_str + ' 已成功删除日志！')
            self.recordname = []
            self.recordnamecombox.clear()

            def listdir(path, list_name):
                for file in os.listdir(path):
                    file_path = file
                    if os.path.isdir(file_path):
                        listdir(file_path, list_name)
                    elif os.path.splitext(file_path)[1] == '.txt':
                        list_name.append(os.path.splitext(file_path)[0])
                return list_name

            self.recordname = listdir(self.recordpath, self.recordname)
            self.recordnamecombox.addItems(self.recordname)
        else:
            self.showinfo.append(self.time_str + ' 请选择日志名称！')
            self.recordtipshow()

    def recordtipshow(self):
        QMessageBox.question(self, '信息', '未选择日志名称，请选择日志名称!', QMessageBox.Yes)
    '''------------------删除场景------------------'''
    def DeleteSit(self):
        self.deledialog = QDialog()
        self.deledialog.setWindowTitle('删除应用场景')
        self.deledialog.setWindowModality(Qt.ApplicationModal)

        self.delenameLabel = QLabel('场景名称', self)
        self.delenamecombox = QComboBox()
        self.delenamecombox.setPlaceholderText('请选择要删除的场景名称')
        self.name = []
        self.setinfo()
        self.delenamecombox.addItems(self.name)

        self.delebtnOK = QPushButton('确定')
        self.delebtnOK.clicked.connect(self.deletesetup)
        self.delebtnExit = QPushButton('退出')
        self.delebtnExit.clicked.connect(self.deledialog.reject)

        self.deleLayout = QGridLayout(self)
        self.deleLayout.addWidget(self.delenameLabel, 0, 0, 1, 1)
        self.deleLayout.addWidget(self.delenamecombox, 0, 1, 1, 2)
        self.deleLayout.addWidget(self.delebtnOK, 1, 1, 1, 1)
        self.deleLayout.addWidget(self.delebtnExit, 1, 2, 1, 1)
        self.deledialog.setLayout(self.deleLayout)

        self.deledialog.exec()
    '''删除配置'''
    def deletesetup(self):
        if self.delenamecombox.currentText() != ' ':
            filename = self.setuppath + '/' + self.delenamecombox.currentText() + '.txt'
            os.remove(filename)
            self.showinfo.append(self.time_str + ' 已成功删除场景配置！')
            self.deledialog.reject()
            self.name = []
            self.setinfo()
            self.combox.clear()
            self.combox.addItems(self.name)
    '''------------------摄像头配置------------------'''
    def cameraset(self):
        self.camdialog = QDialog()
        self.camdialog.setWindowTitle('摄像头配置')
        self.camdialog.resize(300, 220)
        self.camdialog.setWindowModality(Qt.ApplicationModal)

        self.cambutton = QPushButton('获取摄像头配置')
        self.camcombox = QComboBox()
        self.camcombox.setPlaceholderText('请选择摄像头编号')
        self.camsetbutton = QPushButton('确定摄像头配置')

        self.cambutton.clicked.connect(self.caminfo)
        self.camsetbutton.clicked.connect(self.backcaminfo)

        self.camlayout = QVBoxLayout()
        self.camlayout.addWidget(self.cambutton)
        self.camlayout.addWidget(self.camcombox)
        self.camlayout.addWidget(self.camsetbutton)
        self.camdialog.setLayout(self.camlayout)

        self.camdialog.exec()

    def caminfo(self):
        self.camname = []
        num, self.camname = Camera()
        self.camcombox.clear()
        self.camcombox.addItems(self.camname)
        self.showinfo.append(self.time_str + ' 已成功获取摄像头配置')
        QMessageBox.question(self, '信息', '摄像头检测完成，请选择摄像头序号!', QMessageBox.Yes)

    def backcaminfo(self):
        camsetfile = open(self.camsetpath, 'w')

        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass

            try:
                import unicodedata
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass

            return False

        if is_number(self.camcombox.currentText()):
            camsetfile.write(self.camcombox.currentText())
        else:
            camsetfile.write('0')
        camsetfile.close()
        self.showinfo.append(self.time_str + ' 已成功完成摄像头配置！')
        self.camdialog.reject()

    '''------------------右侧主页面设计------------------'''
    def createright(self):
        self.rightBox = QGroupBox()
        self.rightlayout = QGridLayout()
        self.graphic1 = QLabel()
        self.graphic1.setPixmap(QPixmap(self.guiimgpath+'NUAA_logo.png'))
        self.graphic2 = QLabel()
        self.graphic2.setPixmap(QPixmap(self.guiimgpath+'haier_logo.png'))
        self.graphic3 = QLabel()
        self.graphic3.setPixmap(QPixmap(self.guiimgpath+'txt.png'))
        self.rightlayout.addWidget(self.graphic1, 0, 0, 1, 1)
        self.rightlayout.addWidget(self.graphic2, 0, 1, 1, 1)
        self.rightlayout.addWidget(self.graphic3, 1, 0, 1, 2)
        self.rightlayout.setSpacing(20)
        self.vedio = QLabel()
        self.rightlayout.addWidget(self.vedio)
        self.vedio.hide()
        self.rightBox.setLayout(self.rightlayout)
    '''------------------左侧主页面设计------------------'''
    def createleft(self):
        self.leftBox = QGroupBox()
        self.layout = QVBoxLayout()
        self.label = QLabel("请选择应用场景！")
        self.combox = QComboBox()

        self.combox.setPlaceholderText('请选择场景名称')
        self.setinfo()
        self.combox.addItems(self.name)
        self.buttonexit = QPushButton("退出应用程序")
        self.buttonexit.clicked.connect(self.onClick_exit)
        self.buttonok = QPushButton("确定应用场景")
        self.buttonok.clicked.connect(self.vediosetupcheck)
        self.buttonstop = QPushButton("停止视频检测")
        self.buttonstop.clicked.connect(self.stopvedio)
        self.firelogo = QLabel()
        self.firelogo.setPixmap(QPixmap(self.guiimgpath+'nofire.png'))
        self.layout.addStretch(1)
        self.layout.addWidget(self.label, 0)
        self.layout.setStretchFactor(self.label, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.combox, 1)
        self.layout.setStretchFactor(self.combox, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.buttonok, 3)
        self.layout.setStretchFactor(self.buttonok, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.buttonstop, 4)
        self.layout.setStretchFactor(self.buttonstop, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.buttonexit, 5)
        self.layout.setStretchFactor(self.buttonexit, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.firelogo, 6)
        self.layout.setStretchFactor(self.firelogo, 1)
        self.leftBox.setLayout(self.layout)
    '''------------------下侧主页面设计------------------'''
    def createdown(self):
        self.downBox = QGroupBox()
        self.downlayout = QHBoxLayout()
        self.showinfo = QTextBrowser()

        self.downlayout.addWidget(self.showinfo)
        self.downBox.setLayout(self.downlayout)
    '''------------------配置信息------------------'''
    def setinfo(self):
        def listdir(path, list_name):
            for file in os.listdir(path):
                file_path = file
                if os.path.isdir(file_path):
                    listdir(file_path, list_name)
                elif os.path.splitext(file_path)[1] == '.txt':
                    list_name.append(os.path.splitext(file_path)[0])
            return list_name
        self.name = listdir(self.setuppath, self.name)
    '''------------------退出系统------------------'''
    def onClick_exit(self):
        app = QApplication.instance()
        app.quit()
    '''权重地址'''
    def selectionChange(self):
        global fp
        fp = self.comboBox.currentText()
    '''------------------图像检测------------------'''
    def picturemode(self):
        self.imgdialog = QDialog()
        self.imgdialog.setWindowTitle('图像检测')
        self.imgdialog.resize(360, 300)
        self.setWindowModality(Qt.ApplicationModal)
        self.showinfo.append(self.time_str + ' 已成功打开图像检测窗口！')

        self.layout = QGridLayout()
        self.button1 = QPushButton('加载图片')
        self.button1.clicked.connect(self.loadImage)
        self.imageLabel1 = QLabel()
        self.imgpathbuttton = QPushButton('选择文件保存路径')
        self.imgpath = QLineEdit()
        self.imgpathbuttton.clicked.connect(self.imgsavepath)
        self.button2 = QPushButton('运行检测')
        self.button2.clicked.connect(self.setupcheck)
        self.imageLabel2 = QLabel()
        self.button3 = QPushButton('查看结果')
        self.button3.clicked.connect(self.seeout)

        self.layout.addWidget(self.button1, 0, 0, 1, 1)
        self.layout.addWidget(self.imgpathbuttton, 0, 1, 1, 1)
        self.layout.addWidget(self.imgpath, 1, 0, 1, 2)
        self.layout.addWidget(self.imageLabel1, 2, 0, 2, 2)
        self.layout.addWidget(self.button2, 4, 0, 1, 1)
        self.layout.addWidget(self.button3, 4, 1, 1, 1)
        self.layout.addWidget(self.imageLabel2, 5, 0, 2, 2)
        self.imgdialog.setLayout(self.layout)
        self.imgdialog.exec()

    def loadImage(self):
        self.fname,_ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.jpg *.png)')
        self.imageLabel1.setPixmap(QPixmap(self.fname))
        self.showinfo.append(self.time_str + ' 已成功加载图片！')

    def setupcheck(self):
        self.setname = self.combox.currentText()
        for _ in range(len(self.name)):
            if self.setname == self.name[_]:
                flag = 0
                break
            else:
                flag = 1
        if flag == 0:
            self.runImage()
        else:
            self.showinfo.append(self.time_str + ' 请选择场景配置！')
            self.tipshow()

    def tipshow(self):
        QMessageBox.question(self, '信息', '未选择场景配置，请选择场景配置!', QMessageBox.Yes)

    def imgsavepath(self):
        self.imgsavepath = QFileDialog.getExistingDirectory(self, '保存路径')
        self.imgpath.setText(self.imgsavepath)
        self.showinfo.append(self.time_str + ' 已成功设置检测图像保存路径！')

    def runImage(self):
        f = open(self.setuppath+'/'+self.setname+'.txt', 'r')
        line = f.read()
        f.close()
        fp1, fp2, fp3 = line.split()
        YOLO.update(fp1=fp1, fp2=fp2, fp3=fp3)
        if self.imgsavepath:
            self.imageoutpath = runimage(self.fname, self.default_imgsavepath)
        else:
            self.imageoutpath = runimage(self.fname, self.imgsavepath)
        self.showinfo.append(self.time_str + ' 已成功完成图像检测！')

    def seeout(self):
        self.imageLabel2.setPixmap(QPixmap(self.imageoutpath))
        self.showinfo.append(self.time_str + ' 已显示图像检测的结果！')
    '''------------------视频检测------------------'''
    def vediosetupcheck(self):
        self.setname = self.combox.currentText()
        for _ in range(len(self.name)):
            if self.setname == self.name[_]:
                flag = 0
                break
            else:
                flag = 1
        if flag == 0:
            self.run()
        else:
            self.showinfo.append(self.time_str + ' 请选择场景配置！')
            self.tipshow()

    def run(self):
        setname = self.combox.currentText()
        f = open(self.setuppath+'/'+setname+'.txt', 'r')
        line = f.read()
        f.close()
        fp1, fp2, fp3 = line.split()
        YOLO.update(fp1=fp1, fp2=fp2, fp3=fp3)
        self.updatelayout()

    def updatelayout(self):
        self.graphic1.hide()
        self.graphic2.hide()
        self.graphic3.hide()
        self.vedio.show()
        self.showinfo.append(self.time_str + ' 已成功运行视频检测！')
        self.frecord = open(self.recordpath + '/' + self.time_record + '_record.txt', "a")
        self.showvedio()

    def showvedio(self):
        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        yolo = YOLO()
        # 调用摄像头
        f = open(self.camsetpath, 'r')
        n = f.read()
        f.close()
        self.capture = cv2.VideoCapture(int(n))  # capture=cv2.VideoCapture("1.mp4")
        fps = 0.0
        t1 = time.time()
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        while (True):
            t1 = time.time()
            # 读取某一帧
            ref, frame = self.capture.read()
            # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(frame))
            # 进行检测
            img, flag = yolo.detect_image(frame)
            frame = np.array(img)
            # RGBtoBGR满足opencv显示格式
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            fps = (fps + (1. / (time.time() - t1))) / 2
            # print("fps= %.2f" % (fps))
            frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            frame = cv2.resize(frame, (800, 600))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            show = frame
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.vedio.setPixmap(QPixmap.fromImage(showImage))
            t1 = time.time()
            self.c = cv2.waitKey(1) & 0xff
            if flag:
                self.firelogo.setPixmap(QPixmap(self.guiimgpath + 'fire.png'))
                self.frecord.write(self.time_str + ' ' + str(flag) + '\n')
            else:
                self.firelogo.setPixmap(QPixmap(self.guiimgpath + 'nofire.png'))
            if self.c == 27:
                self.capture.release()
                break
            if True == self.stopEvent.is_set():
                # 关闭事件置为未触发，清空显示label
                self.capture.release()
                self.frecord.close()
                break
        tf.keras.backend.clear_session()
        cv2.destroyAllWindows()

    def stopvedio(self):
        self.vedio.hide()
        self.graphic1.show()
        self.graphic2.show()
        self.graphic3.show()
        self.stopEvent.set()
        self.showinfo.append(self.time_str + ' 已成功停止视频检测！')



if __name__ =='__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('guiimg/logo.ico'))
    main = MainWin()
    main.show()
    sys.exit(app.exec())
