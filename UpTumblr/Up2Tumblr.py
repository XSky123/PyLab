# coding=utf8
#This script should use python 2.x to compile!
import sys
if sys.version_info.major != 2:
	raise ImportError("This script must be ran in Python 2.x")
#IF NOT Python 3
import pytumblr
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
"短丝袜",
"短棉袜",
"绝对领域",
"裸足",
"重口味",
"裤袜",
"白丝",
"帆布鞋"
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
* Version : Preview 1
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
	if mode == 1:#img
		for line in lst:
			try:
				if (line.split(".")[-1]=="png" or line.split(".")[-1]=="jpg" or line.split(".")[-1]=="gif" or line.split(".")[-1]=="jpeg" or line.split(".")[-1]=="bmp"):
					tmpLst.append(line)
			except:
				pass
	else:
		if(line.split(".")[0] != line):#有后缀的视为正确路径
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
		if count % 5 == 0 and count != len(lst):# 5 Files Per Line
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


"""
Run
"""
welcome()
while(True):
	print("* 请选择上传类别")
	__type__ = UI.memu(["img 美图美美哒","txt 文字萌萌哒"])
	UI.drawline()

	print("* 请选择上传站点")
	inputType = UI.memu(["52sock","AiYuanWei","JustArt"])
	if inputType == 1:
		__Host__ = __ListOfHost__["SOCK"]
	elif inputType == 2:
		__Host__ = __ListOfHost__["PANGCI"]
	elif inputType == 3:
		__Host__ = __ListOfHost__["NUDE"]
	UI.drawline()

	print("* 上传整个目录或单独上传?")
	inputMode = UI.memu(["整个目录","分别上传"])
	UI.drawline()

	__fileList__ = GetFileList(inputMode)
	__fileList__ = checkList(__fileList__,__type__)
	showList(__fileList__)
	__fileList__ = editLst(__fileList__)
	UI.drawline()

	__autoFetchedTitle__ = __fileList__[0].split("/")[-2]
	__title__ = raw_input("* 请输入标题 回车使用[" + __autoFetchedTitle__ + "]:")
	if(__title__ == ""):
		__title__ = __autoFetchedTitle__
	UI.drawline()

	print("* 请选择标签")
	tmp = 0
	while(tmp!=1):
		tmp = UI.memu(__TagList__,1)
		if tmp!=1:
			__tags__.append(__TagList__[tmp-1])
	if __type__ == 1:
		__fileList__ =  dividePicLst(__fileList__)
		if len(__fileList__) == 1:
			client.create_photo(__Host__, state="published", tags=__tags__, format="markdown", data=__fileList__[0], caption=__title__)
		else:
			count = 0
			for x in __fileList__:
				count += 1
				client.create_photo(__Host__, state="published", tags=__tags__, format="markdown", data=x, caption=__title__+'('+str(count)+')')
	else:
		print("文字上传暂未开放!")
