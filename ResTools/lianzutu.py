import urllib.request,urllib,re,os,threading,queue,time
import socket
import FileTool,WebTool
from bs4 import BeautifulSoup
socket.setdefaulttimeout(10.0) 
UI = FileTool.UI()
__QUEUE__ = queue.Queue()
__ERRList__ = []
    
def get_Type():
    print("* 请选择类型:")
    typeid = UI.memu(["棉袜","丝袜","玉足","美腿志"])
    baseURL = "http://www.lianzutu.com/lztp/"
    if typeid == 1:
        baseURL += "ywmw/list_31_"
    elif typeid == 2:
        baseURL += "swmt/list_30_"
    elif typeid == 3:
        baseURL += "xxyz/list_29_"
    else:
        baseURL += "meituizhi/list_33_"
    return [typeid,baseURL]

def getPage(URL):
        # socket=urllib.request.urlopen(URL)
        # myPage=socket.read().decode('gb2312')
        myPage=WebTool.OpenURL(URL,True)
        myMatch = re.search(r'pageinfo">共 <strong>(\d+?)</strong>页', myPage, re.S)
        if myMatch:  
            endPage = int(myMatch.group(1))
            # print ('共有%d页' % endPage)
        else:
            endPage = 1
            print ('Cannot fetch pages！')
        return endPage

def getTitle(myPage):
    myMatch = re.search(r'<SPAN id=txtTitle>(.*?)</SPAN>', myPage, re.S)
    title = u'暂无标题'
    if myMatch:
        title  = myMatch.group(1)
    else:
        print ('无法加载文章标题！')
    # 文件名不能包含以下字符： \ / ： * ? " < > |
    title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')
    return title

def getType(myPage):
    myMatch = re.search(r'恋足图片</a> > <a href=.*?>(.*?)</a>', myPage, re.S)
    title = u'其他类别'
    if myMatch:
        title  = myMatch.group(1)
    else:
        print ('无法加载文章标题！')
    # 文件名不能包含以下字符： \ / ： * ? " < > |
    return title

def get_link(url):
    # socket=urllib.request.urlopen(url)
    # htmlSource=socket.read().decode('gb2312')
    #openurl
    soup=WebTool.OpenURL_BS(url,True)
    content=soup.find(class_="lpic lpiclist")
    links=content.find_all('a',text=re.compile('(?!<)'))
    baseURL = "http://www.lianzutu.com"
    #beautifulsoup
    linkgroups = []

    # i=0

    for lnk in links:
        linkgroups.append(baseURL + lnk['href'])
        # #Only Five
        # if i >= 5:
        #     break
        # i += 1
        # print (baseURL + lnk['href'])
    # print("****************************************")
    return linkgroups
        
def get_Img(myPage):
    htmlSource=myPage
    getlink=re.compile(r'(?<=<dl><dt><dd>).*?(?=<dd>)')
    #非贪婪以匹配第一个dd标签
    links=re.findall(getlink,htmlSource)
    #print("[计数]共"+str(len(links))+"项")
    link_out=[]
    for lnk in links:
        lnk="http://www.lianzutu.com"+lnk#链接补全
        link_out.append(lnk)
        #print(lnk)
    return link_out

def get_Everylink(typeid,baseURL):
    firstpage = baseURL + "1.html"
    pages = getPage(firstpage)
    links = []

    print("* 本分类共",pages,"页")
    tmp = input("全部下载 [回车] | 指定下载页数:")
    if tmp == "":
        for i in range(1,pages + 1):
            URL = baseURL + str(i) +".html"
            links += get_link(URL)
            print("* Page " + str(i) + " has added.")
    else:
        URL = baseURL + tmp +".html"
        links += get_link(URL)
        print("* Page " + tmp + " has added.")
    return links

class Downloader(threading.Thread):
    def __init__(self,queue,path,isFirst=0):
        threading.Thread.__init__(self)
        self.queue = queue
        self.path = path
        self.isFirst = isFirst
    def run(self):
        URL = self.queue.get()
        fName = URL.split("/")[-1]
        # FileTool.mkdir(self.path)
        # with open("./" + self.path + "/" + fName, 'wb') as file:          
        #             image_data = WebTool.OpenURL(URL)
        #             file.write(image_data)
        try:
            with open("./" + self.path + "/" +fName, 'wb') as file:          
                    image_data = WebTool.OpenURL(URL)
                    file.write(image_data)
                    print("    [FINISH]",URL)
        except Exception as e:
            # print("    [ERR]"+URL)
            print (e)
            __ERRList__.append([self.path,URL])

        # urllib.request.urlretrieve(URL,self.path + "/" + fName)
        # try:
        #     urllib.request.urlretrieve(URL,self.path + "/" + fName)
        #     print("    [FINISH]",URL)
        # except:
        #     print("    [ERR]"+URL)
        #     __ERRList__.append([self.path,URL])
        self.queue.task_done()

def get_Item(URL):
    # socket = urllib.request.urlopen(URL)
    # myPage = socket.read().decode('gb2312')
    myPage = WebTool.OpenURL(URL,True)

    myTitle = getTitle(myPage)
    myType = getType(myPage)
    myImg = get_Img(myPage)
    myCount = len(myImg)

    myPath = "lianzutu/" + myType +"/" + myTitle
    if os.path.exists(myPath): 
            # print("已存在!") 
        pass
    else: 
        os.makedirs(myPath)

    print("[标题]" + myTitle)
    print("[类别]" + myType)
    print("[张数]" + str(myCount))

    print("* 开始下载...")
    for i in range(len(myImg)):
        if i==0:
            t = Downloader(__QUEUE__,myPath,1)
        else:
            t = Downloader(__QUEUE__,myPath,0)
        t.setDaemon(True)
        t.start()
    for url in myImg:
        __QUEUE__.put(url)
    __QUEUE__.join()

    print("* 下载成功")
    UI.drawline()

def dealERR():
    while len(__ERRList__) >0:
        tmp = input("* 尝试再次下载失败的项目?[Enter] to start.[other] to quit:")
        if tmp == "":
            for i in range(len(__ERRList__)):
                t = Downloader(__QUEUE__,__ERRList__[i][0])
                t.setDaemon(True)
                t.start()
                __QUEUE__.put(__ERRList__[i][1])
                del(__ERRList__[i])
            __QUEUE__.join()
        else:
            print("[ERR Files]")
            for item in __ERRList__:
                print("[Path]" + item[0])
                print("[URL]" + item[1])
                UI.drawline()
            break

def main():
    myType = get_Type()
    myLink = get_Everylink(myType[0],myType[1])
    for x in myLink:
        get_Item(x)
    #Err try..
    dealERR()


while(True):
    main()