import hashlib
import pymysql
import mysql.connector
from mysql.connector import Error

##############################DATABASE CONNECTION
connection = mysql.connector.connect(host='localhost',
                                    database='user_of_PyChat',
                                    user='root',
                                    password='root',
                                    port=8889)
print(connection)
mycursor = connection.cursor()

# sql = "INSERT INTO usr (username, password, uid, fName, lName) VALUES ('admin', 'admin', 0, 'Y', 'pers')"
# mycursor.execute(sql)
# connection.commit()

mycursor.execute("SELECT * FROM `usr`")
myresult = mycursor.fetchall()

for x in myresult:
  print(x)
#################################################

##############################DATABASE ERASE
def reset_database_user (name) :
    sql = "DELETE FROM usr WHERE username = name"
    mycursor.execute(sql)
    connection.commit()
#############################################

##############################SET NEW PASSWORD
def set_new_password(name, fname, lname, pwd) :
    sql = "SELECT MAX(uid) FROM usr"
    mycursor.execute(sql)
    UID = mycursor.fetchall()[0] + 1

    hsh = hashlib.pbkdf2_hmac('sha256', pwd, b'salt', 100000)

    sql = "INSERT INTO usr (username, password, real_pass, uid, fName, lName) VALUES ("+name+", "+hsh+", "+pwd+" , "+str(UID)+", "+fname+", "+lname+")";
    mycursor.execute(sql)
    connection.commit()

##############################################

##############################REGISTERATION
#in client -> fname & lname -> username
def valid_username (name, fname, lname) :
    sql = "SELECT username FROM usr WHERE username = name"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0 :
        return False
    return True
##########################################

#############################CHECK PASSWORD
def check_password(name, hsh) :
    sql = "SELECT password FROM usr WHERE username = name"
    mycursor.execute(sql)
    mycursor = mycursor.fetchall()
    if mycursor == hsh :
        return True
    return False
###########################################

#############################DELETE ACCOUNT
def dlt_acc (name, hsh) :
    if check_password(name, hsh) :
        reset_database_user(name)
        return True
    return False
###########################################