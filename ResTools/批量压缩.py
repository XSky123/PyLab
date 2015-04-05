from FileTool import *
import os
while True:
	path = input("输入需要压缩文件夹的母目录：")
	print("Begin")
	myList = ls(path)
	for item in myList:
		if os.path.isdir(item):
			zipFolder(item)
			print("Done ---- "+item)