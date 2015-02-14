import os
import zipfile
import urllib.request
def mkdir(path):
	"""
	Make the dir if path not exist.
	Because Linux cannot make the whole path for a time,
	use this could solve the problem.
	"""
	myPath = path.split('/')
	for i in range(1,len(myPath)):
		myPath[i] = myPath[i-1] + '/' + myPath[i]
	for addr in myPath:
		if os.path.isdir(addr): 
			pass 
		else: 
			os.mkdir(addr)
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
def txtformat(path):
	pass