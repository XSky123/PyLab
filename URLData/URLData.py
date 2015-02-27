import re
import FileTool,WebTool,xskysql
UI = FileTool.UI()
__TypeName__ = [
"Tumblr",
"LOFTER",
"福利搜索",
"福利图站",
"二次元",
"福利论坛"
]
def parseURL(originalURL,mode):
	"""
	Parse URL
	获取纯净的URL以便去重复及储存
	[example]
	In: http://www.fengnu.com/daohang/
	Out:
	    [Mode 1] Near Origin
	        www.fengnu.com/daohang
	    [Mode 2] pure Host
	        fengnu.com
	    [Mode 3]Host & IP
	        www.fengnu.com"""

	# pure Host
	if mode == 2:
		#为匹配服务 所有均加入"/"
		tmpURL = originalURL + "/"
		#URL 以http 开头或 https开头则去掉, 注意可能有局限性.
		#待后续解决这个问题
		if tmpURL.startswith("http://")or tmpURL.startswith("https://"):
			tmpURL = re.search(r'(?<=//)(.*\..*)',tmpURL).group()
		#选择第一部分
		tmpURL = tmpURL.split('/')[0]
		#选择域名主机部分
		tmpURL = tmpURL.split('.')[-2]+"."+tmpURL.split('.')[-1]
		return tmpURL
		# print(tmpURL)
		# myParse = re.search(r'(?<=\.)(.*)(?<=\.)(.*?)(?=/)',tmpURL)
		# return myParse.group()
	elif mode == 3:
		#为正则表达式匹配服务 所有均加入/
		tmpURL = originalURL + "/"
		#URL 以http 开头或 https开头则去掉, 注意可能有局限性.
		#待后续解决这个问题
		if tmpURL.startswith("http://") or tmpURL.startswith("https://"):
			tmpURL = re.search(r'(?<=//)(.*\..*)',tmpURL).group()
		tmpURL = tmpURL.split('/')[0]
		return tmpURL
	else:
		tmpURL = originalURL
		#URL "/"结束 则去掉
		if tmpURL.endswith("/"):
			tmpURL = tmpURL[:-1]
		#URL 以http 开头或 https开头则去掉, 注意可能有局限性.
		#待后续解决这个问题
		if tmpURL.startswith("http://")or tmpURL.startswith("https://"):
			tmpURL = re.search(r'(?<=//)(.*\..*)',tmpURL).group()
		else:
			myParse = re.search(r'(.*\..*?)',tmpURL).group()
		return tmpURL
def getURL():
	URL = input("* 请输入URL:").lower()
	
	try:
		parsedURL = [parseURL(URL,1),parseURL(URL,2),parseURL(URL,3)]
	except:
		print("* 输入错误!")
		return 0
	print("* 请选择一个地址类型:")
	return parsedURL[UI.memu(parsedURL) - 1]

def getType(URL):
	typeid = 0
	try:
		if URL.index("tumblr") >= 0:
			typeid = 0
	except:
		try:
			if URL.index("lofter") >= 0:
				typeid = 1
		except:
			pass

		typeid = UI.memu(__TypeName__)-1
	return typeid

def getTitle(URL):
	title = ""
	try:
		page = str(WebTool.urllib.request.urlopen(URL).read())
		charset = re.search(r'(?<=meta charset=")(.*?)(?=" />)',page).group()
		title = WebTool.OpenURL_BS(URL,charset).find("title").text
	except:
		try:
			title = WebTool.OpenURL_BS(URL).find("title").text
		except:
			print("Can not get title automaticly!")
			title = URL
	if title != "":
		print("[ENTER] to use [" + title + "] as title")
		# tmp = input("Or enter your own title:")
		# if tmp!="":
		# 	title = tmp
	return title

	f = Open("URL.html","r+")
	f.write(__Head__)

def main():
	URL = getURL()
	type_ = getType(URL)
	title = getTitle(URL)
	xskysql.write(URL,type_,title)
	print("Done!")

while True:
	main()