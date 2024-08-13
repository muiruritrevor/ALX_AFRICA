import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "tking",
    database = "alx_exercise"

)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for i in mycursor:
    print(i)