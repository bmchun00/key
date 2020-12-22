import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import time
import os, glob
import requests
from bs4 import BeautifulSoup

def getInternal(): #개선 필요
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    flist = glob.glob(BASE_DIR+'\internal\*.bmc')
    todo = []
    for i in flist:
        tf = open(i,"rt",encoding='UTF-8')
        txtlist = tf.readlines()
        for j in range(0,len(txtlist)):
            todo.append(txtlist[j].replace("\n", ""))
    return todo

def getNews():
    headers = {"User-Agent": "Mozilla/5.0"}
    url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=001&aid=0011343153'
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,"html.parser")
    cont = soup.select("._article_body_contents")[0].get_text()
    cont = cont.replace("\n","")
    cont = cont.replace("\t", "")
    cont = cont.replace("\'", "")
    cont = cont.replace("    ", "\n")
    output = cont.split("\n")
    return output[0:len(output)-1]

def getAt(cor, time, wrong):
    cnt = 0
    cl = list(cor)
    while cl:
        tmp = cl.pop(0)
        if '가'<=tmp<='힣':
            cnt+=2.6 #수정 필요(불확실성)
        else:
            cnt+=1
    return cnt/time*60*wrong/100


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

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.center()
        self.main = MainTap()
        self.text = TextTap()
        self.news = TextTap()
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

        self.setWindowTitle('key(가제) 1.05a')
        self.setFixedSize(500,300)
        self.show()

    def tcEvent(self):
        changedInd = self.tabs.currentIndex()
        if changedInd == 1:
            tab = self.text
            tab.initALL('internal')
        if changedInd == 2:
            tab = self.news
            tab.initALL('news')
        if changedInd == 1 or changedInd == 2:
            num, ok = QInputDialog.getInt(self, '문장 수', '수행할 문장 수를 입력해 주세요.', 1, 1, len(tab.toList)-1)
            if ok:
                tab.pbar.setMaximum(num)
                tab.pbar.setValue(0)
                tab.progressNum = 0
                tab.maxNum = num
            else:
                self.tabs.setCurrentIndex(0)

    def keyPressEvent(self, e):
        changedInd = self.tabs.currentIndex()
        if changedInd == 1:
            tab = self.text
        if changedInd == 2:
            tab = self.news
        if e.key() == Qt.Key_Return and tab.get.text() != '':
            if tab.progressNum == 0: #유예
                tab.prevtime = time.time()
                tab.title.setText(tab.toList[tab.progressNum])
                tab.progressNum += 1
                tab.get.setText('')
                tab.title.setAlignment(Qt.AlignCenter)
            else:
                user = tab.get.text()
                cor = tab.toList[tab.progressNum-1]
                duringtime = time.time() - tab.prevtime
                tab.prevtime = time.time()
                tab.userList.append(user)
                tab.get.setText('')
                val = tab.pbar.value()
                tab.pbar.setValue(val + 1)
                tab.progressNum += 1
                wrong = getWrong(user,cor)
                tab.wrongList.append(wrong)
                tab.wrong.setText("정확도 : "+str(int(wrong))+"%")
                at = getAt(cor,duringtime,wrong)
                tab.atList.append(at)
                tab.tasu.setText("분당 타수 : "+str(int(at)))
                tab.title.setAlignment(Qt.AlignCenter)
                if tab.progressNum == tab.maxNum + 1:
                    tab.title.setText('')
                    res = QMessageBox()
                    res.setWindowTitle("결과")
                    res.setText("평균 분당 타수 : "+str(int(sum(tab.atList)/len(tab.atList)))+"\n평균 정확도 : "+str(int(sum(tab.wrongList)/len(tab.wrongList)))+"%")
                    res.exec()
                    self.tabs.setCurrentIndex(0)
                else:
                    tab.title.setText(tab.toList[tab.progressNum])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MainTap(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.title = QLabel("key(가제) 1.05a", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.tfont = self.title.font()
        self.tfont.setFamily('맑은 고딕')
        self.tfont.setPointSize(20)
        self.title.setFont(self.tfont)

        self.sub = QLabel("이 내용은 테스트입니다.이 내용은 테스트입니다.이 내용은 테스트입니다.\n이 내용은 테스트입니다.이 내용은 테스트입니다.",self)
        self.sfont = self.sub.font()
        self.sub.setAlignment(Qt.AlignCenter)
        self.sfont.setFamily('맑은 고딕')
        self.sub.setFont(self.sfont)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.sub)

        self.setLayout(self.vbox)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
