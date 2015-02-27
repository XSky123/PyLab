import mysql.connector
config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'python'
}
cnx = mysql.connector.connect(**config)
def getType():
	lst = []
	cursor = cnx.cursor()
	query = "SELECT * FROM taglist"
	cursor.execute(query)
	for (tagid,tagname) in cursor:
		lst.append(tagname)
	return lst
	cursor.close()
def write(URL,typeid,title):
	cursor = cnx.cursor()
	query = "INSERT INTO urlbase (typeid,name,url) VALUES (%s, %s, %s)"
	data = (str(typeid),title,URL)
	cursor.execute(query,data)
	cnx.commit()
	cursor.close()
def close():
	cnx.close()