import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import time
import os, glob

def getInternal():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    flist = glob.glob(BASE_DIR+'\internal\*.txt')
    todo = []
    for i in flist:
        tf = open(i,"rt",encoding='UTF-8')
        txtlist = tf.readlines()
        for j in range(0,len(txtlist)):
            todo.append(txtlist[j].replace("\n", ""))

    return todo

def getWrong(user, cor):
    cnt = 0
    lc = len(cor)
    if user == cor:
        return 100
    else:
        user = list(user)
        cor = list(cor)
        print(len(cor))
        while cor:
            c = cor.pop(0)
            if user:
                u = user.pop(0)
                if c!=u:
                    cnt+=1
            else:
                cnt+=1
        return (lc-cnt)/lc * 100

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
        tabfont = self.tabs.font()
        tabfont.setFamily('맑은 고딕')
        self.tabs.setFont(tabfont)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabs)

        self.tabs.currentChanged.connect(self.tcEvent)

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
            if self.text.progressNum == 0: #유예
                self.text.prevtime = time.time()
                self.text.title.setText(self.text.toList[self.text.progressNum])
                self.text.progressNum += 1
                self.text.get.setText('')
            else:
                user = self.text.get.text()
                cor = self.text.toList[self.text.progressNum-1]
                duringtime = time.time() - self.text.prevtime
                self.text.prevtime = time.time()
                print(duringtime)
                self.text.userList.append(user)
                self.text.get.setText('')
                val = self.text.pbar.value()
                self.text.title.setText(self.text.toList[self.text.progressNum])
                self.text.pbar.setValue(val + 1)
                self.text.progressNum += 1
                wrong = getWrong(user,cor)
                self.text.wrongList.append(wrong)
                self.text.wrong.setText("정확도 : "+str(wrong))
                print(getWrong(user,cor))
                if self.text.progressNum == self.text.maxNum + 1:
                    print(self.text.userList)
                    print(self.text.toList[0:self.text.maxNum])


class MainTap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        title = QLabel("반갑습니다.", self)
        title.setAlignment(Qt.AlignCenter)
        tfont = title.font()
        tfont.setFamily('맑은 고딕')
        tfont.setPointSize(20)
        title.setFont(tfont)

        sub = QLabel("이 내용은 테스트입니다.이 내용은 테스트입니다.이 내용은 테스트입니다.\n이 내용은 테스트입니다.이 내용은 테스트입니다.",self)
        sfont = sub.font()
        sub.setAlignment(Qt.AlignVCenter)
        sfont.setFamily('맑은 고딕')
        sub.setFont(sfont)

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
        self.tasu = QLabel("분당 타수 : ", self)
        self.wrong = QLabel("정확도 : ", self)
        self.get = QLineEdit(self)
        self.get.setAlignment(Qt.AlignCenter)
        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(Qt.AlignVCenter)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.tasu)
        self.vbox.addWidget(self.wrong)
        self.vbox.addWidget(self.get)
        self.vbox.addWidget(self.pbar)
        self.setLayout(self.vbox)

    toList = getInternal()
    progressNum = 0
    maxNum = 0
    userList = []
    prevtime = 0
    wrongList = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
