import pytumblr
import os
LstHost={
1:"sock000",#Sock
2:"pangci000",#Pangci
3:"bibibibi"#Pussy
}
host=""
piclst=[]
taglst=[]
client = pytumblr.TumblrRestClient(
  'Dl6kRefS0zDClWFuhnzcNMi2DkUcqF0h1nifYNjFl37kznKFok',
  'CZyho1KXgrf1sgRwOUJzrqFCcXvC20543p3UxdxlYMGN3wW7v9',
  'yul3Rm7qx9zdgyMUzKONnkdQuIQtdT4YNqpBo0NVusxtyCBF4X',
  '7xeDM4ocEv0TG0Nksp4xqCEKic1LFPrM6xQjQ5x8RtuzpatO9Z'
)
def UploadPics(host,tagLst,picLst,title):
	client.create_photo(host, state="published", tags=tagLst, format="markdown", data=picLst, caption=title)

print("Welcome!")



input1=input("Please choose the type:\n1 ----> Sock\n2 ----> Pangci\n3 ----> Pussy\nEnter A Num---->")
print("")
try:
	# print("[Your Choice is "+str(input1)+"]")
	host=LstHost[input1]
except:
	host=LstHost[1]
	print("Use Default Settings [Sock]")



input2=input("Everything or one by one? \n1 ----> Add Whole Mulu\n2 ---->Add one by one\nEnter A Num---->")
if input2==1:
	input3=raw_input("Input the mulu \n ---->")
	if input3[-1]!="/":
		input3+="/"
	try:
		tmplst=os.listdir(input3)
	except:
		tmplst=[]
	count=0
	for line in tmplst:
		if (line.split(".")[-1]=="png" or line.split(".")[-1]=="jpg" or line.split(".")[-1]=="gif" or line.split(".")[-1]=="jpeg" or line.split(".")[-1]=="bmp"):
			piclst.append(input3+line)
			count+=1
	print ("[Total]"+str(count)+"P")
elif input2==2:
	while(1):
		tmp=raw_input("Enter -->")
		if(tmp!=''):
			piclst.append(tmp)
		else:
			break
else:
	print("Err")


while(1):
	count=0
	for item in piclst:
		count+=1
		print("["+str(count)+"]"+item.split("/")[-1])
	print("Sure? or input the id to delete q to back")
	tmp=raw_input("Enter -->")
	if tmp.isdigit():
		tmp=int(tmp)
		if(tmp!=''):
			del piclst[tmp-1]
	else:
		break

print("Now Enter The Tags")
while(1):
		tmp=raw_input("Enter Tags-->")
		if(tmp!=''):
			taglst.append(tmp)
		else:
			break
# for item in taglst:
# 	print(item)

title=raw_input("Enter Title->")
UploadPics(host,taglst,piclst,title)