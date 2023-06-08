import pymysql
db=mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    passwd="",
    database="test"
)
mycursor = db.cursor()

