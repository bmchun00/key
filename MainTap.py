from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MainTap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.title = QLabel("key(가제) 1.10a", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.tfont = self.title.font()
        self.tfont.setFamily('맑은 고딕')
        self.tfont.setPointSize(20)
        self.title.setFont(self.tfont)

        self.sub = QLabel("Internal Text에서 내부 텍스트를 불러올 수 있습니다.\nNews에서 뉴스를 불러올 수 있습니다.\n다만 뉴스의 경우 문자열 길이에 대한 처리가 아직 필요합니다.\nLyrics에서 멜론 Top50 랜덤 곡의 가사를 불러올 수 있습니다.",self)
        self.sfont = self.sub.font()
        self.sub.setAlignment(Qt.AlignCenter)
        self.sfont.setFamily('맑은 고딕')
        self.sub.setFont(self.sfont)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.sub)

        self.setLayout(self.vbox)