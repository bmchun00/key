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