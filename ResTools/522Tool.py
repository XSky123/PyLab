#encoding=utf8
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error,http.cookiejar,gzip
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1  
import time,os
import re
import queue,threading
import sys
__PROGRAM_TITLE__="FiveTwenty-two Tool"
__VER__="v2.4"
__AUTHOR__="XSky123"
__ADDR__="http://www.522yw.cc"
__SAVE_MULU__="522yw"
__ITEM_ONE_TIME__=3
__IS_SHOWN_CONTENT__=0
__QUEUE__ = queue.Queue()
__COOKIE__=""
__TYPELIST__={
'1':"SiWa",
'2':"MianWa",
'3':"PangCi",
'5':"Shoes",
'6':"Novel",
'41':"Ropes",
}

# Functions
def line(text="",length=40):
	line=''
	space=round((length-len(text))/2+1)
	for x in range(space):
		line+='='
	line+=text
	for x in range(space):
		line+='='
	print(line)
def memu():
	line(" "+__PROGRAM_TITLE__+" ")
	# print(__PROGRAM_TITLE__)
	print("[Version]",__VER__)
	print("[Author]",__AUTHOR__)
	line("[Type List]")
	# print("[Type List]")
	for key in sorted(__TYPELIST__.keys()):
		print  ("["+key+"]",__TYPELIST__[key])
	line()
	type_id=input("[INFO]ENTER A NUMBER:")
	return type_id
def mkmulu(addr):
	if os.path.isdir(addr): 
		pass 
	else: 
		os.mkdir(addr)
def getcookie():
	loginUrl = "http://www.522yw.cc/article/43465.html"
	cj =http.cookiejar.CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	urllib.request.install_opener(opener)
	resp = urllib.request.urlopen(loginUrl)
	cookie_=""
	for index, cookie in enumerate(cj):
		cookie_=re.findall('<Cookie (.*?) for',str(cookie),re.S)[0]
	return cookie_
def fetchlist(type_id,page=1):
	URL=__ADDR__+"/article/list_"+type_id+'_'+str(page)+".html"
	time1=time.time()
	html=OpenURL(URL)
	time2=time.time()
	lst_original=re.findall('class=list>(.*?)</DIV',html,re.S)
	time3=time.time()
	line()
	print("[TYPE]",__TYPELIST__[type_id],"\n[Page]  ",page)
	print("[OpenTime]",round(time2-time1))
	print("[FetchTime]",time3-time2)
	#  =====================================
	#  To Test BS4 Speed!
	#  =====================================
	# time4=time.time()
	# html1=OpenURL_BS(URL)
	# time5=time.time()
	# lst_original1=html1.find("div",class_="text1_1text").find_all("div",class_="list")
	# time6=time.time()
	# print("OpenWithBS4:",time5-time4,"And Fetch:",time6-time5)
	lst=[]
	lst_save=[]
	savedURLid=0
	count=1
	for item in lst_original:
		lst.append([re.findall('href="(.*?)"',item,re.S)[0].strip(),re.findall('target=_blank>(.*?)</A>',item,re.S)[0].strip(),re.findall('0>(.*?)</FONT>',item,re.S)[0].strip()])
		# ===FETCH===
	while(1):
		begin=(count-1)*__ITEM_ONE_TIME__
		if(count*__ITEM_ONE_TIME__>len(lst)):# ===IF MORE THAN THE LENGTH,CUT THEM===
			end=len(lst)
		else:
			end=count*__ITEM_ONE_TIME__
		line()
		for x in range(begin,end):
			print("[ID]",x+1)
			print("[DATE]",lst[x][2])
			print("[URL]",lst[x][0])
			print("[TITLE]",lst[x][1])
			line()
		while(1):
			tmp=input("[INFO]Enter the id you'd like to save,[Q] to quit,[Other] to continue:")
			if(tmp.isdigit()):
				savedURLid=int(tmp)
				if(savedURLid>begin and savedURLid<=end):
					try:
						if(lst_save.index(lst[savedURLid-1][0])>=0):
							print("[ERROR]",lst[savedURLid-1][1],"has already added")
					except:
						lst_save.append([lst[savedURLid-1][0],type_id])
						print("[ADD]",lst[savedURLid-1][1])
				else:
					print("[ERROR]Wrong ID!")
			else:
				if(tmp.lower()=="q"):
					count=len(lst)/__ITEM_ONE_TIME__
				break
		count+=1
		if(len(lst)%__ITEM_ONE_TIME__==0):# ===IF JUST OK,Compare Length;or minus one before compare ===
		# === E.g When [len(lst)] is 30 but [__ITEM_ONE_TIME__] is 20 Then count++ means it get to 40,over 30. ===
			if(count*__ITEM_ONE_TIME__>len(lst)):
				break
		else:
			if((count-1)*__ITEM_ONE_TIME__>len(lst)):
				break
	line()
	while(1):
		tmp1=input("[INFO]Page "+str(page)+" has added,press [Y] to go on next page,[ENTER] to back:")
		if(tmp1.lower()=="y"):
			lst_save.extend(fetchlist(type_id,page+1))
			return lst_save
		elif(tmp1==""):
			return lst_save
		else:
			print("[ERROR]Wrong Input!")
def fetchcontent(URL):
	time1=time.time()
	html=OpenURL(URL)
	time2=time.time()
	title= re.findall('<H2>(.*?)</H2>',html,re.S)[0]
	date=re.findall('</H2>(.*?) 来源',html,re.S) [0]
	html_bs=BeautifulSoup(html)
	content_block=html_bs.find(class_="centen2",id="content")
	link=[]
	line()
	for lnk in content_block.findAll("img"):
		# print ("http://www.522yw.cc"+lnk["src"])
		link.append("http://www.522yw.cc"+lnk['src'])
	print ("[TITLE]",title)
	print("[DATE]",date)
	print("[COUNT]",str(len(link))+"P")
	print("[OpenTime]",round(time2-time1),"seconds")
	if(__IS_SHOWN_CONTENT__):
		print ("[CONTENT]",content_block.text)
	
	callback=[title,date,link,content_block.text]
	line()
	return callback
class Downloader(threading.Thread):
	def __init__(self,queue,mulu):
		threading.Thread.__init__(self)
		self.queue = queue
		self.mulu=mulu
	def run(self):
		URL=self.queue.get()
		mulu=self.mulu+"/"+URL.split("/")[-1]
		try:
			with open(mulu, 'wb') as file:			
					image_data = OpenURL(URL,False)
					file.write(image_data)
		except:
			print("[ERR]Can Not Download"+URL)
			
			# urllib.request.urlretrieve(URL,mulu)   # reporthook 为回调钩子函数，用于显示下载进度
		print("    [FINISH]",URL)
		self.queue.task_done()
def downloadpic(content_lst):
	title=content_lst[0][0]
	date=content_lst[0][1]
	link=content_lst[0][2]
	content=content_lst[0][3]
	mulu=__SAVE_MULU__+"/"+__TYPELIST__[content_lst[1]]+"/"+title
	mkmulu(__SAVE_MULU__)
	mkmulu(__SAVE_MULU__+"/"+__TYPELIST__[content_lst[1]])
	mkmulu(mulu)
	fp = open(mulu+"/"+title+".txt","a")
	filecontent="[TITLE]"+title+"\n"+"[DATE]"+date+"\n"+"[COUNT]"+str(len(link))+"P"+"\n"+"[CONTENT]\n"+content+"\n"
	fp.write(filecontent)
	print("[DOWN]FINISHED WRITTEN CONTENT FILE")
	for i in range(len(link)):
		t = Downloader(__QUEUE__,mulu)
		t.setDaemon(True)
		t.start()
	for url in link:
		__QUEUE__.put(url)
	print("[DOWN]",title,"Downloading start.")
	time1=time.time()
	__QUEUE__.join()
	time2=time.time()
	print("[DOWN]",title,"Downloading finished.Used",round(time2-time1),"seconds")
	line()
def Opener(cookie=""):
	head = {
	'Connection': 'Keep-Alive',
	'Accept': 'text/html, application/xhtml+xml, */*',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	}
	if(cookie!=""):
		head['Cookie']=cookie
		# cj = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener()
	header = []
	for key, value in head.items():
	    elem = (key, value)
	    header.append(elem)
	opener.addheaders = header
	return opener
def OpenURL(URL,decode=True):
	if(URL.startswith("http://")==0):
		URL="http://"+URL
	opener=Opener(__COOKIE__)
	try:
		htmlOriginal =opener.open(URL, timeout = 10).read()
	except urllib.error.HTTPError as e:
		return e
	# socket=urllib.request.urlopen(URL)
	if(htmlOriginal.startswith(b'\x1f\x8b')):
		htmlOriginal=gzip.decompress(htmlOriginal).decode("gbk")
	if(decode):
		htmlSource=htmlOriginal.decode("gbk")
	else:
		htmlSource=htmlOriginal
	return htmlSource
def OpenURL_BS(URL):
	soup=BeautifulSoup(OpenURL(URL))
	return soup
FIRST_RUN=1

while(1):
	lst=[]
	while(1):
		type_id=memu()
		print("[INFO]LOADING...")
		if(FIRST_RUN):
			__COOKIE__=getcookie()
			FIRST_RUN=0
		lst+=(fetchlist(type_id))
		# print (lst)
		line()
		print("[INFO]Current List")
		for x in lst:
			print(x[0]+" [TYPE: "+__TYPELIST__[x[1]]+"]")
		if (len(lst)==0):
			print("(empty)")
		line()
		tmp=input("[INFO]Start Fetch Content?[ENTER] to begin ,[other] to back to memu to go on:")
		if(tmp==""):
			break
	for URL in lst:
		print("[FETCH]begin to fetch",URL[0]+" [TYPE: "+__TYPELIST__[URL[1]]+"]")
		imglst=[fetchcontent(URL[0]),URL[1]]
		downloadpic(imglst)
	tmp=input("Press [Enter] to go on.")
	if(tmp==""):
		print()
