#coding:utf-8
import re,os,urllib.request,time,codecs,shutil
import queue,threading
import WebTool
Q = queue.Queue()
wastelist = []
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

def getDuPanURL(path):
	with codecs.open(path, 'r', 'gbk') as handle:			
		line = handle.readline()
		myMatch = re.search(r'链接[：:](.*?) 密码', line, re.S)
		if myMatch:
			# print (myMatch.group(1))
			return myMatch.group(1).strip()#去空格
		else:
			return 0
def getDuPanPWD(path):
	with codecs.open(path, 'r', 'gbk') as handle:			
		line = handle.readline()
		myMatch = re.search(r'密码[：:](.*)', line, re.S)
		if myMatch:
			# print (myMatch.group(1))
			return myMatch.group(1)
		else:
			return "未找到密码"
def testDuPan(URL):
	# socket = urllib.request.urlopen(URL)
	myPage = WebTool.OpenURL(str(URL))
	# print(myPage)
	try:
		myMatch = re.search(r'<title>百度云 网盘-(.*?)</title>', myPage, re.S)
	except:
		return 0
	if myMatch:
		if myMatch.group(1) == "链接不存在":
			# print("不存在")
			return 0
		else:
			# print("连接有效")
			return 1
	else:
		# print("链接有效")
		return 1
# class Downloader(threading.Thread):
# 	def __init__(self,queue):
# 		threading.Thread.__init__(self)
# 		self.queue = queue
# 	def run(self):
# 		item = self.queue.get()
# 		try:
# 			URL = getDuPanURL(item)
# 			PWD = getDuPanPWD(item)
# 			if URL:
# 				if testDuPan(URL):
# 					# print(URL)
# 					filename = os.path.basename(item)
# 					print(str(filename) + " ---- " + str(PWD))
# 					print(URL)
# 					print("*----------------------------------")
# 				else:
# 					print("失效")
# 					wastelist.append(item)
# 		except:
# 			wastelist.append(item)
def run():
	path = input("EnterPath(cuz no check,make sure there are all txt):")
	mylist = ls(path)
	mylist.sort()
	for x in mylist:
		URL = getDuPanURL(x)
		PWD = getDuPanPWD(x)
		# print(x)
		if(testDuPan(URL)!=1):
			wastelist.append(x)
		else:
			print(os.path.basename(x))
			print(URL + " " + PWD)
			print("*----------------------------------")

	print("* 失效列表")
	for item in wastelist:
		print(os.path.basename(item))

		# item +="\n"
	
	# print(mylist)
	# for i in range(len(mylist)):
	# 	t = Downloader(Q)
	# 	t.setDaemon(True)
	# 	t.start()
	# for url in mylist:
	# 	Q.put(url)
	# Q.join()
	

	# print("*--------------------------------------")
	# print("* 失效列表")
	# for item in wastelist:
	# 	print(os.path.basename(item))

run()