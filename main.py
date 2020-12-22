import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import time
import os, glob
import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver

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
    url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=011&aid=0003845459'
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,"html.parser")
    cont = soup.select("._article_body_contents")[0].get_text()
    print(cont)
    cont = cont.replace("\n","")
    cont = cont.replace("\t", "")
    cont = cont.replace("\'", "")
    cont = cont.replace("\\", "")
    output = cont.split("다.")
    print(output)
    return output[0:len(output)-1]

def getLyrics(num):
    headers = {"User-Agent": "Mozilla/5.0"}
    #top num의 곡명과 가수명 수집
    url = 'https://www.melon.com/chart/index.htm'
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,"html.parser")
    title = soup.select(".ellipsis.rank01")[num].get_text()
    singer = soup.select(".ellipsis.rank02")[num].get_text()
    title = title.replace("\n","")
    singer = singer.replace("\n","")
    singer = singer[0:len(singer)//2]
    output = []
    output.append(title+" - "+singer)
    #top num의 가사 수집
    dsn = soup.find_all("tr", {"data-song-no": True})
    songno=[]
    for i in dsn:
        songno.append(i["data-song-no"])
    tosongno=songno[num]
    url = "https://www.melon.com/song/detail.htm?songId=" + tosongno
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    lyr = soup.find("div",{"class":"lyric"}).get_text("\n")
    lyr = lyr.replace("\t","")
    lyr = lyr.replace("\r","")
    lyr = lyr.split("\n")
    lyr = removeValuesFromList(lyr,'')
    for i in lyr:
        output.append(i.strip())
    return output

def removeValuesFromList(list, val):
    return [value for value in list if value != val]


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
        self.lyr = TextTap()
        self.stat = QWidget()
        self.changelog = QWidget()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.main, 'Main')
        self.tabs.addTab(self.text, 'Internal Text')
        self.tabs.addTab(self.news, 'News')
        self.tabs.addTab(self.lyr, 'Lyrics')
        self.tabs.addTab(self.stat, 'Stat')
        self.tabs.addTab(self.changelog, 'ChangeLog')
        tabfont = self.tabs.font()
        tabfont.setFamily('맑은 고딕')
        self.tabs.setFont(tabfont)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabs)

        self.tabs.currentChanged.connect(self.tcEvent)

        self.setLayout(self.vbox)

        self.setWindowTitle('key(가제) 1.10a')
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
        if changedInd == 3:
            tab = self.lyr
            tab.initALL('lyrics')
            print(tab.toList)
        if changedInd == 1 or changedInd == 2 or changedInd == 3:
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
        if changedInd == 3:
            tab = self.lyr
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
                    tab.title.setAlignment(Qt.AlignCenter)
                    res = QMessageBox()
                    res.setWindowTitle("결과")
                    res.setText("평균 분당 타수 : "+str(int(sum(tab.atList)/len(tab.atList)))+"\n평균 정확도 : "+str(int(sum(tab.wrongList)/len(tab.wrongList)))+"%")
                    res.exec()
                    self.tabs.setCurrentIndex(0)
                else:
                    tab.title.setText(tab.toList[tab.progressNum-1])
                    tab.title.setAlignment(Qt.AlignCenter)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
