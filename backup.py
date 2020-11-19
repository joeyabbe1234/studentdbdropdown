import mysql.connector
db=mysql.connector.connect(host="localhost",user="user",password="abonitalla123",db="studentdb")
dbcursor = db.cursor()
def collegecount():
    dbcursor.execute("SELECT * FROM college")
    x = dbcursor.fetchall()
    y = []
    for z in x:
        y.append(z[1])
    return y

def coursecount():
    dbcursor.execute("SELECT * FROM course")
    x = dbcursor.fetchall()
    y = []
    for z in x:
        y.append(z[1])
    return y

def departmentcount():
    dbcursor.execute("SELECT * FROM department")
    x = dbcursor.fetchall()
    y = []
    for z in x:
        y.append(z[1])
    return y
