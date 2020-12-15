import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.video_gui import video
from gui.picture_gui import runimage
import os


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
        self.toolbar = QToolBar
        self.toolbar = self.addToolBar("工具栏")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.createset = QAction("新建场景")
        self.createset.setShortcut("Ctrl+N")
        self.createset.triggered.connect(self.CreateSit)
        self.deleteset = QAction("删除场景")
        self.deleteset.setShortcut("Ctrl+D")
        self.deleteset.triggered.connect(self.deletesit)
        self.camera = QAction("摄像头配置")
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

        self.newsit = QAction(QIcon('D:\\pythonfile\\yolov4-tiny-tf2-master\\gui\\image\\newsit.png'), "新建场景", self)
        self.newsit.triggered.connect(self.CreateSit)
        self.toolbar.addAction(self.newsit)
        self.delete = QAction(QIcon('D:\pythonfile\yolov4-tiny-tf2-master\gui\image\delete.png'), "删除场景", self)
        self.delete.triggered.connect(self.deletesit)
        self.toolbar.addAction(self.delete)
        self.newcamera = QAction(QIcon('D:\pythonfile\yolov4-tiny-tf2-master\gui\image\camera.png'), "摄像头配置", self)
        self.newcamera.triggered.connect(self.cameraset)
        self.toolbar.addAction(self.newcamera)
        self.picture = QAction(QIcon('D:\pythonfile\yolov4-tiny-tf2-master\gui\image\picture.png'), "图像识别", self)
        self.picture.triggered.connect(self.picturemode)
        self.toolbar.addAction(self.picture)
        self.exitsystool = QAction(QIcon('D:\pythonfile\yolov4-tiny-tf2-master\gui\image\exit.png'), "退出系统", self)
        self.exitsystool.triggered.connect(self.onClick_exit)
        self.toolbar.addAction(self.exitsystool)

        self.status = self.statusBar()
        self.status.showMessage('欢迎进入明火烟雾检测系统！', 5000)
        self.createright()
        self.createleft()
        self.mainbox = QWidget()
        self.mainlayout = QHBoxLayout()
        self.mainlayout.addWidget(self.leftBox)
        self.mainlayout.addWidget(self.rightBox)
        self.mainbox.setLayout(self.mainlayout)
        self.setCentralWidget(self.mainbox)
    '''新建场景'''
    def CreateSit(self):
        self.dialog = QDialog()
        self.setWindowTitle('新建应用场景')
        self.setWindowModality(Qt.ApplicationModal)

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

        self.classLabel = QLabel('&Class', self)
        self.classLabel.setText('场景类别(&C)')
        self.classLineEdit = QLineEdit(self)
        self.classLineEdit.setPlaceholderText('请输入场景类别文件地址')
        self.classLabel.setBuddy(self.classLineEdit)

        def savesetup():
            if self.nameLineEdit.text() != '':
                f = open('D:\\pythonfile\\yolov4-tiny-tf2-master\\gui\\setup\\' + self.nameLineEdit.text() + '.txt',
                         'w')
                f.write(self.nameLineEdit.text() + ' ' + self.weightLineEdit.text() + ' ' + self.classLineEdit.text())
                self.dialog.reject()

        self.btnOK = QPushButton('确定')
        self.btnOK.clicked.connect(savesetup)
        self.btnCancel = QPushButton('取消')
        self.btnCancel.clicked.connect(self.nameLineEdit.clear)
        self.btnCancel.clicked.connect(self.weightLineEdit.clear)
        self.btnCancel.clicked.connect(self.classLineEdit.clear)
        self.btnExit = QPushButton('退出')
        self.btnExit.clicked.connect(self.dialog.reject)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.nameLabel, 0, 0)
        self.mainLayout.addWidget(self.nameLineEdit, 0, 1, 1, 2)

        self.mainLayout.addWidget(self.weightLabel, 1, 0)
        self.mainLayout.addWidget(self.weightLineEdit, 1, 1, 1, 2)

        self.mainLayout.addWidget(self.classLabel, 2, 0)
        self.mainLayout.addWidget(self.classLineEdit, 2, 1, 1, 2)

        self.mainLayout.addWidget(self.btnOK, 3, 0)
        self.mainLayout.addWidget(self.btnCancel, 3, 1)
        self.mainLayout.addWidget(self.btnExit, 3, 2)
        self.dialog.setLayout(self.mainLayout)

        self.dialog.exec()
    '''联系我们'''
    def connect_us(self):
        pass
    '''删除场景'''
    def deletesit(self):
        self.deledialog = QDialog()
        self.setWindowTitle('删除应用场景')
        self.setWindowModality(Qt.ApplicationModal)
        path = 'D:\pythonfile\yolov4-tiny-tf2-master\gui\setup'
        name = []

        def listdir(path, list_name):
            for file in os.listdir(path):
                file_path = file
                if os.path.isdir(file_path):
                    listdir(file_path, list_name)
                elif os.path.splitext(file_path)[1] == '.txt':
                    list_name.append(os.path.splitext(file_path)[0])
            return list_name

        name = listdir(path, name)

        self.nameLabel = QLabel('场景名称', self)
        self.namecombox = QComboBox()
        self.namecombox.setPlaceholderText('请选择新建场景名称')
        self.namecombox.addItems(name)

        def deleteset():
            if self.namecombox.currentText()!=' ':
                filename = 'D:\\pythonfile\\yolov4-tiny-tf2-master\\gui\\setup\\' + self.namecombox.currentText() + '.txt'
                os.remove(filename)
                self.deledialog.reject()

        self.btnOK = QPushButton('确定')
        self.btnOK.clicked.connect(deleteset)
        self.btnExit = QPushButton('退出')
        self.btnExit.clicked.connect(self.deledialog.reject)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.namecombox, 0, 1, 1, 2)
        self.mainLayout.addWidget(self.btnOK, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.btnExit, 1, 2, 1, 1)
        self.deledialog.setLayout(self.mainLayout)

        self.deledialog.exec()
    '''摄像头设置'''
    def cameraset(self):
        pass
    '''主界面设计'''
    def createright(self):
        self.rightBox = QGroupBox()
        self.layout = QGridLayout()
        self.graphic1 = QLabel()
        self.graphic1.setPixmap(QPixmap('D:\\pythonfile\\yolov4-tiny-tf2-master\\gui\\image\\NUAA_logo.png'))
        self.graphic2 = QLabel()
        self.graphic2.setPixmap(QPixmap('D:\\pythonfile\\yolov4-tiny-tf2-master\\gui\\image\\haier_logo.png'))
        self.graphic3 = QLabel()
        self.graphic3.setPixmap(QPixmap('D:\\pythonfile\\yolov4-tiny-tf2-master\\gui\\image\\txt.png'))
        self.layout.addWidget(self.graphic1, 0, 0, 1, 1)
        self.layout.addWidget(self.graphic2, 0, 1, 1, 1)
        self.layout.addWidget(self.graphic3, 1, 0, 1, 2)
        self.layout.setSpacing(20)
        self.rightBox.setLayout(self.layout)

    def createleft(self):
        self.leftBox = QGroupBox()
        self.layout = QVBoxLayout()
        self.label = QLabel("请选择应用场景！")
        self.combox = QComboBox()
        path = 'D:\pythonfile\yolov4-tiny-tf2-master\gui\setup'
        name = []

        def listdir(path, list_name):
            for file in os.listdir(path):
                file_path = file
                if os.path.isdir(file_path):
                    listdir(file_path, list_name)
                elif os.path.splitext(file_path)[1] == '.txt':
                    list_name.append(os.path.splitext(file_path)[0])
            return list_name

        name = listdir(path, name)
        self.combox.addItems(name)
        self.buttonexit = QPushButton("退出应用程序")
        self.buttonexit.clicked.connect(self.onClick_exit)
        self.buttonok = QPushButton("确定应用场景")
        self.buttonok.clicked.connect(self.run)
        self.layout.addStretch()
        self.layout.addWidget(self.label, 0)
        self.layout.addStretch()
        self.layout.addWidget(self.combox, 1)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonok, 3)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonexit, 4)
        self.layout.addStretch()
        self.leftBox.setLayout(self.layout)
    '''退出系统'''
    def onClick_exit(self):
        app = QApplication.instance()
        app.quit()
    '''权重地址'''
    def selectionChange(self):
        global fp
        fp = self.comboBox.currentText()
    '''图像检测'''
    def picturemode(self):
        self.dialog = QDialog()
        self.setWindowTitle('图像检测')
        self.dialog.resize(360, 300)
        self.setWindowModality(Qt.ApplicationModal)

        self.layout = QVBoxLayout()
        self.button1 = QPushButton('加载图片')
        self.button1.clicked.connect(self.loadImage)
        self.imageLabel1 = QLabel()
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.imageLabel1)
        self.button2 = QPushButton('运行检测')
        self.button2.clicked.connect(self.runImage)
        self.imageLabel2 = QLabel()
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.imageLabel2)
        self.button3 = QPushButton('查看结果')
        self.button3.clicked.connect(self.seeout)
        self.layout.addWidget(self.button3)

        self.dialog.setLayout(self.layout)
        self.dialog.exec()
    def loadImage(self):
        global fname
        fname,_ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.jpg *.png)')
        print(fname)
        self.imageLabel1.setPixmap(QPixmap(fname))
    def runImage(self):
        print(fname)
        self.image = runimage(fname)
    def seeout(self):
        self.imageLabel2.setPixmap(QPixmap(self.image))
    '''视频检测'''
    def run(self):
        video(fp)

if __name__ =='__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('D:\pythonfile\yolov4-tiny-tf2-master\gui\image\logo.ico'))
    main = MainWin()
    main.show()
    sys.exit(app.exec())


