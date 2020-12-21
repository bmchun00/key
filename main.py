import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt

typenum = 0
class communicate(QObject):
    getnum = pyqtSignal()

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main = MainTap()
        self.text = TextTap()
        self.news = QWidget()
        self.stat = QWidget()
        self.changelog = QWidget()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.main, 'Main')
        self.tabs.addTab(self.text, 'Internal Text')
        self.tabs.addTab(self.news, 'News')
        self.tabs.addTab(self.stat, 'Stat')
        self.tabs.addTab(self.changelog, 'ChangeLog')

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabs)

        self.tabs.currentChanged.connect(self.tcEvent)
        print(self.tabs.currentIndex())

        self.setLayout(self.vbox)

        self.setWindowTitle('key(가제) 1.01a')
        self.setGeometry(300, 300, 500, 300)
        self.show()

    def tcEvent(self):
        changedInd = self.tabs.currentIndex()
        if changedInd == 1 or changedInd == 2:
            num, ok = QInputDialog.getInt(self, '문장 수', '수행할 문장 수를 입력해 주세요.')
            if ok:
                self.text.pbar.setMaximum(num)
                self.text.pbar.setValue(0)
                self.text.progressNum = 0
                self.text.maxNum = num
            else:
                self.tabs.setCurrentIndex(0)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return and self.text.get.text() != '':
            self.text.get.setText('')
            val = self.text.pbar.value()
            self.text.pbar.setValue(val+1)
            self.text.progressNum += 1
            if self.text.progressNum == self.text.maxNum:
                print('fin')



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
        self.title = QLabel("아무거나 입력해 시작합니다.", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.get = QLineEdit(self)
        self.get.setAlignment(Qt.AlignCenter)
        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(Qt.AlignVCenter)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.get)
        self.vbox.addWidget(self.pbar)
        self.setLayout(self.vbox)
    progressNum = 0
    maxNum = 0


if __name__ == '__main__':
    typenum = 0
    app = QApplication(sys.argv)
    ex = MyApp()
    print(typenum)
    sys.exit(app.exec_())
