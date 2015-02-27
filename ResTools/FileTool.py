# coding=utf8
"""
*------------------------------------------------------------ 
* Model : FileTool 
* Version : 1.6.1
* Designer : XSky123
*
* About UI,FileIO,zip...
* 伦家会努力让你喜欢的～喵～～
*------------------------------------------------------------
"""
import os,sys
import zipfile
class UI:
	def memu(self,options,direction=0):
		tmp=" "
		optionTXT=""
		count=1
		nbsp = "    "#空格
		for item in options:
			if direction == 1:#横向排版
				optionTXT += ("["+str(count)+"]"+item)
				optionTXT += nbsp
				if count % 5 == 0 and count != len(options):# 5 Files Per Line
					optionTXT += "\n"
			else:#纵向排版
				optionTXT += "[" + str(count) + "] " + item
				if count<len(options):
					optionTXT += "\n"
			count += 1
		print("* —— 我想想哈（选哪个好呢）")
		print (optionTXT)
		while True:
			#if version = 2.x
			if sys.version_info.major == 2:
				tmp = raw_input("* —— 好啦，我选:")
			#if version = 3.x
			else:
				tmp = input("* —— 好啦，我选:")
			if tmp.isdigit() and int(tmp)>0 and int(tmp)<count:
				return int(tmp)
			else:
				print ("* —— 等等，好像不对...")
		print("*------------------------------------------------------------")
	def memu2(self,options):
		count = len(options) + 1
		while True:
			#if version = 2.x
			if sys.version_info.major == 2:
				tmp = raw_input("* —— 好啦，我选:")
			#if version = 3.x
			else:
				tmp = input("* —— 好啦，我选:")
			if tmp.isdigit() and int(tmp)>0 and int(tmp)<count:
				return int(tmp)
			else:
				print ("* —— 等等，好像不对...")
		print("*------------------------------------------------------------")
	def drawline(self):
		print("*------------------------------------------------------------")
def mkdir(path):
	"""
	Make the dir if path not exist.
	Because Linux cannot make the whole path for a time,
	use this could solve the problem.
	"""
	if os.path.exists(path): 
		pass 
	else: 
		os.makedirs(path)
	# myPath = path.split('/')
	# for i in range(1,len(myPath)):
	# 	myPath[i] = myPath[i-1] + '/' + myPath[i]
	# 	# print("[path]"+myPath[i])
	# del myPath[0]#delete the first path
	# for addr in myPath:
	# 	print("[Now Addr]"+ addr)
	# 	if os.path.isdir(addr): 
	# 		# print(addr)
	# 		pass 
	# 	else: 
	# 		print("[md]"+addr)
	# 		os.mkdir(addr)
def ls(path):
	"""
	Get files list in complated path
	"""
	#Add "/" to path
	if path[-1]!="/":
		path+="/"
	fileList = os.listdir(path)
	filePathList=[]
	for line in fileList:
		filePathList.append(path+line)
	return filePathList
def zipFolder(path):
	"""
	Zip the whole folder.
	"""

	#Add "/" to path
	if path[-1]!="/":
		path+="/"
	# Use "except" in case of the Folder is in the same dir with py.
	try:
		folderName = path.split('/')[-2]
	except:
		folderName = path.split('/')[-1]
	filePathList=ls(path)
	z = zipfile.ZipFile(path+folderName+".zip",mode='a')
	for item in filePathList:
		# print(item)
		z.write(item,item.split('/')[-1])

def cutTxt(path,WordsPerItem):
	try:
		f = open(path,"r")
	except:
		print("Path error!")
		return 0
	seprated = []
	fp.read(WordsPerItem)