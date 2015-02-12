from WebTool import *
import time,os
import re
baseURL = "http://www.javzoo.com/cn/search/"

def getInfo():
	serialNum = input ("请输入番号---------------->")
	listURL = baseURL+serialNum
	bsList = OpenURL_BS(listURL)
	listContent = bsList.find(class_="item pull-left")
	contentURL = listContent.a['href']
	if contentURL.split("/")[-2]!="movie":
		print("Not Found!")
	else:
		bsContent = OpenURL_BS(contentURL)
		title= re.findall(' (.*?)$',str(bsContent.h3.text),re.S)[0].strip()
		info = bsContent.find(class_="span3 info")
		serial = re.findall('<span style="color:#CC0000;">(.*?)</span>',str(info),re.S)[0].strip()
		pubDate = re.findall('发行时间:</span> (.*?)</p>',str(info),re.S)[0].strip()
		length = re.findall('长度:</span> (.*?)</p>',str(info),re.S)[0].strip()
		producer = re.findall('studio/.*">(.*?)</a></p>',str(info),re.S)[0].strip()
		publisher = re.findall('label/.*">(.*?)</a></p>',str(info),re.S)[0].strip()
		try:
			series = re.findall('series/.*">(.*?)</a></p>',str(info),re.S)[0].strip()
		except:
			series = ""
		types = re.findall('genre/.*?">(.*?)</a></span>',str(info))

		print("标题--------->"+title)
		print("番号--------->"+serial)
		print("发行日期--->"+pubDate)
		print("片长--------->"+length)
		print("制作商------>"+producer)
		print("发行商------>"+publisher)
		print("系列名------>"+series)
		print("类别--------->"+" ".join(types))

while(1):
		getInfo()
