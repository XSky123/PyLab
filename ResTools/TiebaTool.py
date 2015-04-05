from WebTool import *
from FileTool import *
import xskysql
import socket
import threading,queue
import time,os
import re
timeout = 10
socket.setdefaulttimeout(timeout)
#TimeOut
UI = UI()
__QUEUE__ = queue.Queue()
__ERRList__ = []

def welcome():
	print ("""*------------------------------------------------------------ 
* Programe : 贴吧萌萌哒(CuteTieba) 
* Version : 2.0.3
* Designer : XSky123
*
* I hope you enjoy this Programe! 
* 伦家会努力让你喜欢的～喵～～
*------------------------------------------------------------""")

class Downloader(threading.Thread):
	def __init__(self,queue,path,count):
		threading.Thread.__init__(self)
		self.queue = queue
		self.path = path
		self.count = count

	def run(self):
		URL = self.queue.get()
		filename = str(self.count) + '.jpg'
		filePath = self.path + '/' + filename
		try:
			urllib.request.urlretrieve(URL,filePath)
			# xskysql.write(self.title,filename,URL,filePath)
		except Exception as e:
			print (e)
			__ERRList__.append([self.path,self.count,URL])
		self.queue.task_done()

class CuteTieba:
	# initialize
	def __init__(self,postID):
		self.baseURL =  "http://tieba.baidu.com/p/" + str(postID) + "?see_lz=1"
		self.myPage = OpenURL(self.baseURL)
		self.title = self.getTitle(self.myPage)
		self.path = 'tieba/' + self.title
		self.endPage = self.getPage(self.myPage)
		self.author = self.getAuthor(self.myPage)
		print("*------------------------------------------------------------")
		print("* Title : " + self.title)
		print("* Author : " + self.author)
		print("* ID : " + postID)
		print("* Page : " + str(self.endPage))
		print("*------------------------------------------------------------")
	#Framework
	def CuteImg(self):
		ImgList = self.getData(1,self.myPage,self.endPage)
		self.downImg(self.title,ImgList)
		# self.zipImg(self.path)
		print("* Download finished!")

	def CuteTxt(self):
		rawData = self.getData(2,self.myPage,self.endPage)
		self.downTxt(self.title,rawData)
		print("* Download finished!")
	#Detail
	def getData(self,mode,myPage,endPage):
		rawData = []
		for page in range(endPage):
			#If Page = 1 Then Use Last Open Directly To Improve Efficiency
			if endPage==1:
				if mode==2:
					rawData=self.getDataGroup(myPage)
				elif mode==1:
					rawData=self.getImgLst(myPage)
			else:
				if mode==2:
					rawData+=self.getDataGroup(OpenURL(self.baseURL + "&pn=" + str(page+1)))
				elif mode==1:
					rawData+=self.getImgLst(OpenURL(self.baseURL + "&pn=" + str(page+1)))
		if mode==1:
			print("* Count : "+str(len(rawData))+" P")
			print("*------------------------------------------------------------")
		return rawData
	def getImgLst(self,myPage):
		#Care! myPage is an OpenURL Obj NOT URL
		Page = BeautifulSoup(myPage)
		OriLst = Page.find_all(class_="BDE_Image")
		Lst = []
		for addr in OriLst:
			Lst.append("http://imgsrc.baidu.com/forum/pic/item/"+addr["src"].split("/")[-1])
			# Lst.append(addr["src"])
		return Lst
	def getDataGroup(self,myPage):
		Page = BeautifulSoup(myPage)
		OriLst = Page.find_all(class_="d_post_content")
		Lst = []
		for item in OriLst:
			data = Replace_Char(item.text.replace("\n",""))
			#Tips : In order to miss the waste words,line < 15 words will be deleted
			if len(data)>=25:
				Lst.append(data+'\n')
		return Lst
	def getPage(self,myPage):
		myMatch = re.search(r'class="red">(\d+?)</span>', myPage, re.S)
		if myMatch:  
			endPage = int(myMatch.group(1))
			# print ('共有%d页' % endPage)
		else:
			endPage = 1
			print ('Cannot fetch pages！')
		return endPage
	def getTitle(self,myPage):
		# 匹配 <h1 class="core_title_txt" title="">xxxxxxxxxx</h1> 找出标题
		myMatch = re.search(r'<h1.*?>(.*?)</h1>', myPage, re.S)
		title = u'暂无标题'
		if myMatch:
			title  = myMatch.group(1)
		else:
			print ('无法加载文章标题！')
		# 文件名不能包含以下字符： \ / ： * ? " < > |
		title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')
		return title
	def getAuthor(self,myPage):
		Page = BeautifulSoup(myPage)
		tmp = Page.find(class_="p_author_name")
		author = u'Author'
		if(tmp!=None):
			author = tmp.text
		else:
			print ('Author Not Found!')
		return author
	def downImg(self,title,ImgList):
		print("* Begin downloading...")
		path = self.path
		mkdir(path)
		count = 1
		for i in range(len(ImgList)):
			t = Downloader(__QUEUE__,path,count)
			t.setDaemon(True)
			t.start()
			count += 1
		for item in ImgList:
			__QUEUE__.put(item)
		__QUEUE__.join()
		xskysql.write(self.title,"",self.baseURL,os.getcwd()+'/'+self.path)
		self.dealERR()
	def downTxt(self,title,rawData):
		path = 'tieba/txt/'
		mkdir(path)
		f = open(path + title + '.txt','w+')
		f.writelines(rawData)
		f.close()
	def zipImg(self,path):
		zipFolder(path)
	def dealERR(self):
		while len(__ERRList__) >0:
			tmp = input("* 尝试再次下载失败的项目?[Enter] to start.[other] to quit:")
			if tmp == "":
				for x in __ERRList__:
					t = Downloader(__QUEUE__,x[0],x[1])
					t.setDaemon(True)
					t.start()
					__QUEUE__.put(x[2])
					__ERRList__.remove(x)
				# for i in range(len(__ERRList__)):
				# 	print(__ERRList__[i])
				# 	t = Downloader(__QUEUE__,__ERRList__[i][0],__ERRList__[i][1])
				# 	t.setDaemon(True)
				# 	t.start()
				# 	__QUEUE__.put(__ERRList__[i][2])
				# 	del(__ERRList__[i])
				__QUEUE__.join()
			else:
				print("[ERR Files]")
				for item in __ERRList__:
					print("[Path]" + item[0])
					print("[URL]" + item[2])
					UI.drawline()
				break
welcome()
while (True):
	ID = []
	while(True):
		postID = input('ID or URL(空行退出):')
		if not postID.isdigit():
			if postID.startswith("http://"):
				postID = postID.split("/")[-1]
			elif(postID == "" and len(ID) > 0):
				break
			else:
				print("* 输入有误！")
				continue
		ID.append(postID)
	#str(postID) has been added in __init__()
	print("* 请选择类别")
	if(UI.memu(["美图美美哒","文字萌萌哒"])==1):
		for x in ID:
			cutetieba = CuteTieba(x)
			cutetieba.CuteImg()
	else:
		for x in ID:
			cutetieba = CuteTieba(x)
			cutetieba.CuteTxt()
	input("* Press To Continue *")
	print("*------------------------------------------------------------")