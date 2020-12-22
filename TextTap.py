from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from getTxt import *
import random

class TextTap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title = QTextBrowser(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.tasu = QLabel("", self)
        self.wrong = QLabel("", self)
        self.get = QLineEdit(self)
        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(Qt.AlignCenter)
        self.pbar.setTextVisible(False)
        self.pbar.setFixedSize(300,10)
        self.vbox = QVBoxLayout(self)
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.pbar)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.title)
        self.vbox.addStretch(2)
        self.vbox.addWidget(self.tasu)
        self.vbox.addWidget(self.wrong)
        self.vbox.addWidget(self.get)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def initALL(self, type):
        if type == 'internal':
            self.toList = getInternal()
        if type == 'news' :
            self.toList = getNews()
        if type == 'lyrics' :
            self.toList = getLyrics(random.randint(1,50))
        self.progressNum = 0
        self.maxNum = 0
        self.userList = []
        self.prevtime = 0
        self.wrongList = []
        self.atList = []
        self.tasu.setText("")
        self.wrong.setText("")
        self.title.setText("아무거나 입력해 시작합니다.")
        self.title.setAlignment(Qt.AlignCenter)

    toList = []
    progressNum = 0
    maxNum = 0
    userList = []
    prevtime = 0
    wrongList = []
    atList = []