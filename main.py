import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main = MainTap()
        text = TextTap()
        news = QWidget()
        stat = QWidget()
        changelog = QWidget()

        tabs = QTabWidget()
        tabs.addTab(main, 'Main')
        tabs.addTab(text, 'Internal Text')
        tabs.addTab(news, 'News')
        tabs.addTab(stat, 'Stat')
        tabs.addTab(changelog, 'ChangeLog')


        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('alpha')
        self.setGeometry(300, 300, 500, 300)
        self.show()

class MainTap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        title = QLabel("반갑습니다.", self)
        title.setAlignment(Qt.AlignCenter)
        tfont = title.font()
        #tfont.setFamily('맑은 고딕')
        tfont.setPointSize(20)
        title.setFont(tfont)



        sub = QLabel("이 내용은 테스트입니다.이 내용은 테스트입니다.이 내용은 테스트입니다.\n이 내용은 테스트입니다.이 내용은 테스트입니다.",self)
        sfont = sub.font()
        sub.setAlignment(Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(title)
        vbox.addWidget(sub)

        self.setLayout(vbox)

class TextTap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.Tapclick()

    def Tapclick(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())