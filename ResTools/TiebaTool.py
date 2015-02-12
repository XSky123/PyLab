from WebTool import *
import time,os
import re
def welcome():
	print ("""*------------------------------------------------------------ 
* Programe : 贴吧萌萌哒(CuteTieba) 
* Version : Preview 1
* Designer : XSky123
* I hope you enjoy this Programe! 
* 伦家会努力让你喜欢的～喵～～
*------------------------------------------------------------""")
def memu():
	tmp=" "
	print("* —— Hi！有什么吩咐？")
	while True:
		print("""* —— 我想想哈（选哪个好呢）
	[1] 美图美美哒
	[2] 文字萌萌哒
	[3] 别抢～都是我哒！""")
		tmp=input("* —— 好啦，我选:")
		if tmp.isdigit() and int(tmp)==1:
			return 1
		elif tmp.isdigit() and int(tmp)==2:
			return 2
		elif tmp.isdigit() and int(tmp)==3:
			return 3
		else:
			print ("* —— 等等，好像不对...")
	print("*------------------------------------------------------------")
class CuteTieba:
	# initialize
	def __init__(self,postID):
		self.baseURL =  "http://tieba.baidu.com/p/" + str(postID) + "?see_lz=1"
		self.list = []
	#Framework
	def CuteImg(self):
		myPage = OpenURL(self.baseURL)
		endPage = self.getPage(myPage)
		title = self.getTitle(myPage)
		ImgList = self.getImg(myPage,endPage)
		self.downImg(title,ImgList)
	#Detail
	def getImg(self,myPage,endPage):
		ImgList=[]
		for page in range(endPage):
			#If Page = 1 Then Use Last Open Directly To Improve Efficiency
			if endPage==1:
				ImgList=self.getImgLst(myPage)
			else:
				ImgList+=self.getImgLst(OpenURL(self.baseURL + "&pn=" + str(page+1)))
		
		return ImgList
	def getImgLst(self,myPage):
		#Care! myPage is an OpenURL Obj NOT URL
		Page = BeautifulSoup(myPage)
		OriLst = Page.find_all(class_="BDE_Image")
		Lst = []
		for addr in OriLst:
			Lst.append(addr["src"])
		return Lst
	def getPage(self,myPage):
		myMatch = re.search(r'class="red">(\d+?)</span>', myPage, re.S)
		if myMatch:  
			endPage = int(myMatch.group(1))
			print ('共有%d页' % endPage)
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
	def downImg(self,title,ImgList):
		self.mkdir('tieba')
		self.mkdir('tieba/img')
		self.mkdir('tieba/img/'+title)
		count=0
		#Need to add threading
		#Need to have sleep() in each threading
		for item in ImgList:
			urllib.request.urlretrieve(item,'tieba/img/'+title+'/%s.jpg' % count)
			count+=1
			print("Finish"+str(count))
	def mkdir(self,addr):
		if os.path.isdir(addr): 
			pass 
		else: 
			os.mkdir(addr)

welcome()
postID = input('Enter ID:')
#str(postID) has been added in __init__()
cutetieba = CuteTieba(postID)
cutetieba.CuteImg()