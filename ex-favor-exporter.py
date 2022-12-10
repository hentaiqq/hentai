import requests as rq
from bs4 import BeautifulSoup as bs
import re
import os
import random
from concurrent.futures import ThreadPoolExecutor
import threading
import json
import time
# 这里配置你的cookies
# 有啥填啥，必填 {"ipb_member_id":"xxx","ipb_pass_hash":"xxx"}

desDir=".\\ex-favor\\"
if not os.path.exists(desDir):
    os.makedirs('ex-favor')

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

class link:
    def __init__(self,soup):
        self.title = iter(soup.find_all(attrs={'class':'glthumb'}))
        self.link = iter(soup.find_all(attrs={'class':'gl3c glname'}))
    def __iter__(self):
        return self
    def __next__(self):
        return (next(self.title),next(self.link))

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title

def saveImage(imgUrl,imgName):
    r = rq.get(imgUrl, stream=True)
    image = r.content
    imgName=validateTitle(imgName)
    print("save image "+imgName+"\n")
    try:
        with open(desDir+imgName+".jpg" ,"wb") as jpg:
            jpg.write(image)
            return
    except IOError:
        print("IO Error: "+imgUrl)
        return
jsondata = {}
def getfavor(curUrl):
    fakeua={}
    fakeua['user-agent']=random.choice(USER_AGENTS)
    soup=bs(rq.get(curUrl,cookies=cookies,headers=fakeua,proxies=proxies).text,'html.parser')
    count=0
    linklist = []
    name = []
    url = soup.find(attrs={'id':'unext'}).get('href')
    print(url)
    for i in iter(link(soup)):
        count+=1
        print(str(count)+'/'+'50')
        Name=i[0].div.img.attrs['title']
        Link=i[1].a.attrs["href"]
        data = {"method":"gdata","gidlist":[],"namespace":25}
        linklist.append(Link)
        name.append(Name)
        if len(linklist) == 25:
            for l in linklist:
                l = l.split("/")
                data["gidlist"].append([int(l[-3]),l[-2]])
            text = rq.post("https://api.e-hentai.org/api.php",data=json.dumps(data),proxies=proxies).text
            text = json.loads(text)
            for j in range(25):
                if not name[j] in jsondata:
                    jsondata[name[j]] = text['gmetadata'][j]['tags']
                
                #清洗tag
                #把female和male之外的标签全部清洗掉
                for tag in jsondata[name[j]]:
                    if "female" in tag or "male" in tag:
                        continue
                    jsondata[name[j]].remove(tag)

            name = []
            linklist = []
            time.sleep(1)
        print(Name,Link)
    return url
fakeua={}
fakeua['user-agent']=random.choice(USER_AGENTS)
cookies = {"ipb_member_id":os.environ["ipb_member_id"],"ipb_pass_hash":os.environ["ipb_pass_hash"]}
# proxies = {"https":'http://127.0.0.1:1081'}
proxies = {}
try:
    sp=bs(rq.get('https://e-hentai.org/favorites.php',cookies=cookies,headers=fakeua,proxies=proxies).text,'html.parser')
except AttributeError:
    print("请检查cookie是否配置正确、ip是否被ban")
url = sp.find(attrs={'id':'unext'}).get('href')
try:
    jsondata = json.load(open('list.json'))
except:
    jsondata = {}

try:
    count = 0
    while True:
        print("==========正在下载%d页==========" % (count))
        url = getfavor(url)
        if url is None:
            break
        count += 1
except Exception as e:
    print(e)
    print("在下载%d页时发生异常" % count)

#转换为bot使用的格式
with open("dict.json","w",encoding="utf-8") as f:
    f.write(json.dumps([{key:value} for key,value in jsondata.items()],ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))

with open("list.json","w",encoding="utf-8") as f:
    f.write(json.dumps(jsondata,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))

print('task end...')