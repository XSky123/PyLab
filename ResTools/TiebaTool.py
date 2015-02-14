from WebTool import *
from FileTool import *
import time,os
import re
def welcome():
	print ("""*------------------------------------------------------------ 
* Programe : 贴吧萌萌哒(CuteTieba) 
* Version : Preview 1
* Designer : XSky123
*
* I hope you enjoy this Programe! 
* 伦家会努力让你喜欢的～喵～～
*------------------------------------------------------------""")
def memu():
	tmp=" "
	print("* —— Hi！有什么吩咐？")
	while True:
		print("""* —— 我想想哈（选哪个好呢）
	[1] 美图美美哒
	[2] 文字萌萌哒""")
		tmp=input("* —— 好啦，我选:")
		if tmp.isdigit() and int(tmp)==1:
			return 1
		elif tmp.isdigit() and int(tmp)==2:
			return 2
		else:
			print ("* —— 等等，好像不对...")
	print("*------------------------------------------------------------")
class CuteTieba:
	# initialize
	def __init__(self,postID):
		self.baseURL =  "http://tieba.baidu.com/p/" + str(postID) + "?see_lz=1"
		self.myPage = OpenURL(self.baseURL)
		self.title = self.getTitle(self.myPage)
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
			Lst.append(addr["src"])
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
		path = 'tieba/img/' + title
		mkdir(path)
		count = 0
		#Need to add threading
		#Need to have sleep() in each threading
		for item in ImgList:
			urllib.request.urlretrieve(item,'tieba/img/'+title+'/%s.jpg' % count)
			count+=1
	def downTxt(self,title,rawData):
		path = 'tieba/txt/'
		mkdir(path)
		f = open(path + title + '.txt','w+')
		f.writelines(rawData)
		f.close()
welcome()
while (True):
	postID = input('Enter ID:')
	#str(postID) has been added in __init__()
	if(memu()==1):
		cutetieba = CuteTieba(postID)
		cutetieba.CuteImg()
	else:
		cutetieba = CuteTieba(postID)
		cutetieba.CuteTxt()
	input("* Press To Continue *")
	print("*------------------------------------------------------------")