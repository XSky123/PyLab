from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error,http.cookiejar,gzip
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1  
def Opener(cookie=""):
	head = {
	'Connection': 'Keep-Alive',
	'Accept': 'text/html, application/xhtml+xml, */*',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	}
	if(cookie!=""):
		head['Cookie']=cookie
		# cj = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener()
	header = []
	for key, value in head.items():
	    elem = (key, value)
	    header.append(elem)
	opener.addheaders = header
	return opener
def OpenURL(URL,decode=False):
	if(URL.startswith("http://")==0):
		URL="http://"+URL
	opener=Opener()
	htmlOriginal =opener.open(URL, timeout = 1000).read()
	# print("Access"+URL+"Finished")
	htmlSource=""
	# socket=urllib.request.urlopen(URL)
	if(htmlOriginal.startswith(b'\x1f\x8b')):
		htmlOriginal=gzip.decompress(htmlOriginal).decode("utf-8")
	if(decode):
		htmlSource=htmlOriginal.decode("GBK")
	else:
		htmlSource=htmlOriginal

	return htmlSource
def OpenURL_BS(URL):
	soup=BeautifulSoup(OpenURL(URL))
	# print("BeautifulSoup"+URL+"Finished")
	return soup