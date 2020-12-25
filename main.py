import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import time
from MainTap import MainTap
from TextTap import TextTap
from StatTap import StatTab
import os, glob

def writeTxt(at, wrong):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    flist = glob.glob(BASE_DIR + '\\record\stat.bstat')
    if not flist:
        tf = open(BASE_DIR+'\\record\stat.bstat',"w", encoding='UTF-8')
    else:
        tf = open(BASE_DIR+'\\record\stat.bstat',"a", encoding='UTF-8')
    tf.write(str(time.strftime('%Y%m%d%H%M',time.localtime(time.time())))+" "+str(at)+" "+str(wrong)+"\n")

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
        self.stat = StatTab()
        self.changelog = QWidget()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.main, 'Main')
        self.tabs.addTab(self.text, 'Internal Text')
        self.tabs.addTab(self.news, 'News')
        self.tabs.addTab(self.lyr, 'Lyrics')
        self.tabs.addTab(self.stat, 'Stat')
        self.tabs.addTab(self.changelog, 'ChangeLog')
        self.tabs.setTabShape(0)
        tabfont = self.tabs.font()
        tabfont.setFamily('맑은 고딕')
        self.tabs.setFont(tabfont)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabs)

        self.tabs.currentChanged.connect(self.tcEvent)

        self.setLayout(self.vbox)

        self.setWindowTitle('key(가제) 1.10a')
        self.setFixedSize(500,350)
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
        if changedInd == 4:
            self.stat.refresh()
            self.stat.initUI()

    def keyPressEvent(self, e):
        changedInd = self.tabs.currentIndex()
        if changedInd == 1:
            tab = self.text
        if changedInd == 2:
            tab = self.news
        if changedInd == 3:
            tab = self.lyr
        if changedInd in [1,2,3] and e.key() == Qt.Key_Return and tab.get.text() != '':
            if tab.progressNum == 0: #유예
                tab.prevtime = time.time()
                tab.title.setText(tab.toList[tab.progressNum])
                tab.progressNum += 1
                tab.get.setText('')
                tab.get.setAlignment(Qt.AlignCenter)
                tab.title.setAlignment(Qt.AlignCenter)
            else:
                user = tab.get.text()
                cor = tab.toList[tab.progressNum-1]
                duringtime = time.time() - tab.prevtime
                tab.prevtime = time.time()
                tab.userList.append(user)
                tab.get.setText('')
                tab.get.setAlignment(Qt.AlignCenter)
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
                    cb = QCheckBox("결과를 기록할래요")
                    tab.title.setText('')
                    tab.title.setAlignment(Qt.AlignCenter)
                    res = QMessageBox()
                    res.setWindowTitle("결과")
                    res.setText("평균 분당 타수 : "+str(int(sum(tab.atList)/len(tab.atList)))+"\n평균 정확도 : "+str(int(sum(tab.wrongList)/len(tab.wrongList)))+"%")
                    res.setCheckBox(cb)
                    res.exec()
                    self.tabs.setCurrentIndex(0)
                    if cb.checkState():
                        writeTxt(int(sum(tab.atList)/len(tab.atList)), int(sum(tab.wrongList)/len(tab.wrongList)))
                else:
                    tab.title.setText(tab.toList[tab.progressNum-1])
                    tab.title.setAlignment(Qt.AlignCenter)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
