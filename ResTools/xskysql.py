import mysql.connector
config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'python'
}
cnx = mysql.connector.connect(**config)
# def getType():
# 	lst = []
# 	cursor = cnx.cursor()
# 	query = "SELECT * FROM imagelist"
# 	cursor.execute(query)
# 	for (tagid,tagname) in cursor:
# 		lst.append(tagname)
# 	return lst
# 	cursor.close()
def write(groupname,filename,source,savedpath):
	cursor = cnx.cursor()
	query = "INSERT INTO imagelist (groupname,filename,sourceurl,savedpath) VALUES (%s, %s, %s,%s)"
	data = (groupname,filename,source,savedpath)
	cursor.execute(query,data)
	cnx.commit()
	cursor.close()
def close():
	cnx.close()