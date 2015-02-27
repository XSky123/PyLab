# coding=utf8
#This script should use python 2.x to compile!
import sys
if sys.version_info.major != 2:
	raise ImportError("This script must be ran in Python 2.x")
#import
import pytumblr
import threading,Queue
import os
from FileTool import *
"""
Globle variables
"""
__ListOfHost__ = {
	"SOCK":"52sock",
	"PANGCI":"aiyuanwei",
	"NUDE":"itonlyart"
}
__Host__ = __ListOfHost__["SOCK"]
__type__ = 1
__fileList__ = []
__tags__ = []
__TagList__ = [
"[取消]",#不再添加标签时
#袜型 t为type
"t短丝袜",
"t裤袜",
"t棉袜",
"t船袜",
"t过膝袜",
#颜色 c为color
"c白丝",
"c黑丝",
"c肉丝",
"c白棉",
"c卡通",
#特点 w表示袜
"w可爱",
"w重口味",
"w萝莉",
#其他
"t裸足",
"t帆布鞋"
]
UI = UI()
client = pytumblr.TumblrRestClient(
  'Dl6kRefS0zDClWFuhnzcNMi2DkUcqF0h1nifYNjFl37kznKFok',
  'CZyho1KXgrf1sgRwOUJzrqFCcXvC20543p3UxdxlYMGN3wW7v9',
  'KHgicFKa0PyMZRMQvDct1o4uIoRK3iOQ6wL3QXaYTJ1ORYmcj8',
  'u8qV0QF76yYryxHfKkhTUn0s84595bNZAE8pAd0X0FJnAbeW0x'
)
"""
Functions()
"""
def welcome():
	print ("""*------------------------------------------------------------ 
* Programe : Tumblr上传工具(Up2Tumblr) 
* Version : 1.0.4 Alpha
* Designer : XSky123
*
* I hope you enjoy this Programe! 
* 伦家会努力让你喜欢的～喵～～
*------------------------------------------------------------""")

def GetFileList(mode):
	tmpLst = []
	if mode == 1:
		path = raw_input("* 输入路径:")
		tmpLst = ls(path)
	else:
		while(True):
			tmp = raw_input("* 路径:")
			if tmp == "":
				break
			tmpLst.append(tmp)
			print("* " + tmp("/")[-1] + "已添加")
	return tmpLst
def checkList(lst,mode):
	tmpLst = []
	for line in lst:
		if mode == 1:#img
			try:
				if (line.split(".")[-1]=="png" or line.split(".")[-1]=="jpg" or line.split(".")[-1]=="gif" or line.split(".")[-1]=="jpeg" or line.split(".")[-1]=="bmp"):
					tmpLst.append(line)
			except:
				pass
		elif mode == 2:#txt&other
			if(line.split(".")[0] != line):#有后缀的视为正确路径
				tmpLst.append(line)
		else:#mulu
			if(line.split(".")[0] == line):#无后缀的视为正确路径
				tmpLst.append(line)
	return tmpLst

def showList(lst):
	count = 0
	tmp = ""
	nbsp = "    "#空格
	for item in lst:
		count += 1
		fName = item.split("/")[-1]
		tmp += fName
		tmp += nbsp
		if count % 3 == 0 and count != len(lst):# 3 Files Per Line
			tmp += "\n"
	UI.drawline()
	print("* 当前文件列表")
	print(tmp)
	print("* ---- 共 " + str(count) + " 文件 ---- *")

def editLst(lst):
	if raw_input("* 是否编辑列表? 按 [Y] 以编辑 其他以继续:").lower() == "y":
		baseURL = os.path.split(lst[0])[0] + "/" #Get Path
		while True:
			tmp = raw_input("* 请输入要剔除的文件名称,回车退出:")
			if(tmp == ""):
				break
			if len(lst) == 0:
				# 如果为空,需要添加
				print("* 列表为空,请添加")
				print("* 上传整个目录或单独添加?")
				inputMode = UI.memu(["整个目录","单独添加"])
				UI.drawline()
				lst = GetFileList(inputMode)
				lst = checkList(__fileList__,__type__)
				UI.drawline()
				print("* 当前文件列表")
				showList(__fileList__)
				continue
			try:
				lst.remove(baseURL + tmp)
			except:
				print("* 好像不对.重新输入吧:")
			showList(__fileList__)
	return lst

def dividePicLst(lst):
	LstGroup = []
	totalsize = len(lst)
	eachsize = 0
	if totalsize <= 10:
		LstGroup.append(lst)
	else:#算法原则:尽可能使长度够大
		for i in range(5,10):
			if totalsize % i >= (i / 2):
				eachsize = i
		for i in range(0,totalsize,eachsize):
			LstGroup.append(lst[i:i+eachsize])
	return LstGroup

def getTags(TagsGroup):
	ChoosedTags = []
	#Show Tag Groups and get first input
	tmp = UI.memu(TagsGroup,1)
	ChoosedTags.append(TagsGroup[tmp-1])
	#Get other input
	while(tmp!=1):
		tmp = UI.memu2(TagsGroup)
		if tmp!=1:
			ChoosedTags.append(TagsGroup[tmp-1])
	#Print Tags
	out = ""
	for x in ChoosedTags:
		out +=x.decode("utf8")+"    "
	print(out)
	#return
	return ChoosedTags

"""
Run
"""
__Q__ = Queue.Queue()
class Uploader(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self.queue = queue
	def run(self):
		item = self.queue.get()
		print(item[1] + "开始上传")
		try:
			if len(item[0]) == 1:
				client.create_photo(__ListOfHost__ ["SOCK"], state="published", tags=item[2], format="markdown", data=item[0][0], caption=item[1])
			else:
				count = 0
				for x in item[0]:
					count += 1
					client.create_photo(__ListOfHost__ ["SOCK"], state="published", tags=item[2], format="markdown", data=x, caption=item[1]+'('+str(count)+')')
			print(item[1] + " 上传成功!")
		except:
			print(item[1] + "上传失败")
		self.queue.task_done()
def PiLiangAddImg():
	mulu = raw_input("* 请输入待传的目录(有子文件夹的):")
	pathLst = ls(mulu)
	ITEMLIST = []
	for item in pathLst:
		"""
		每文件夹
			得到路径
			得到路径里的图片
			show一下图片数
			show一下标题
			show一下标签列表
			直接写号空格分割
			开始获取
		"""
		imgLst = checkList(ls(item),1)
		title = item.split("/")[-1]
		imgCount = len(imgLst)

		print(title)
		print("共" + str(imgCount) + "张")

		count = 0 #tagsCount
		optionTXT = ""
		nbsp = "    "#nbsp
		#draw choices
		for item in __TagList__:
			optionTXT += ("["+str(count)+"]"+item)
			optionTXT += nbsp
			if count % 5 == 0 and count != len(__TagList__):# 5 Files Per Line
				optionTXT += "\n"
			count  += 1
		print(optionTXT)

		#input choices
		mytags = raw_input("输入编号,用空格分隔:")
		tagsInTxt = []

		#add choices
		if mytags.endswith(" "):#remove last nbsp
			mytags = mytags[:-1]
		for x in mytags.split(" "):
			tagsInTxt.append(__TagList__[int(x)])

		#print results
		out = ""
		for x in tagsInTxt:
			out +=x.decode("utf8")+"    "
		print(out)
		uploadLst =  dividePicLst(imgLst)

		print [uploadLst,title,tagsInTxt]
		ITEMLIST.append([uploadLst,title,tagsInTxt])
		UI.drawline()
	for i in range(len(ITEMLIST)):
		t = Uploader(__Q__)
		t.setDaemon(True)
		t.start()
	for x in ITEMLIST:
		__Q__.put(x)
	__Q__.join()
welcome()
PiLiangAddImg()
# while(True):
# 	if(raw_input("* 回车直接进入目录传图:")==""):
# 		__type__ = 1
# 		inputType = 1
# 		__Host__ = __ListOfHost__["SOCK"]
# 		inputMode = 1
# 	else:
# 		print("* 请选择上传类别")
# 		__type__ = UI.memu(["img 美图美美哒","txt 文字萌萌哒"])
# 		UI.drawline()

# 		print("* 请选择上传站点")
# 		inputType = UI.memu(["52sock","AiYuanWei","JustArt"])
# 		if inputType == 1:
# 			__Host__ = __ListOfHost__["SOCK"]
# 		elif inputType == 2:
# 			__Host__ = __ListOfHost__["PANGCI"]
# 		elif inputType == 3:
# 			__Host__ = __ListOfHost__["NUDE"]
# 		UI.drawline()

# 		print("* 上传整个目录或单独上传?")
# 		inputMode = UI.memu(["整个目录","分别上传"])
# 		UI.drawline()

# 	__fileList__ = GetFileList(inputMode)
# 	__fileList__ = checkList(__fileList__,__type__)
# 	showList(__fileList__)
# 	__fileList__ = editLst(__fileList__)
# 	UI.drawline()

# 	__autoFetchedTitle__ = __fileList__[0].split("/")[-2]
# 	__title__ = raw_input("* 使用[" + __autoFetchedTitle__ + "]请[回车] 或输入标题:")
# 	if(__title__ == ""):
# 		__title__ = __autoFetchedTitle__
# 	UI.drawline()

# 	print("* 请选择标签")
# 	__tags__ = getTags(__TagList__)

# 	if __type__ == 1:
# 		__fileList__ =  dividePicLst(__fileList__)
# 		print("开始上传...")
# 		if len(__fileList__) == 1:
# 			client.create_photo(__Host__, state="published", tags=__tags__, format="markdown", data=__fileList__[0], caption=__title__)
# 		else:
# 			count = 0
# 			for x in __fileList__:
# 				count += 1
# 				client.create_photo(__Host__, state="published", tags=__tags__, format="markdown", data=x, caption=__title__+'('+str(count)+')')
# 		print("* 上传成功!")
# 		__tags__ = []#清空tag
# 		UI.drawline()
# 	else:
# 		print("文字上传暂未开放!")
