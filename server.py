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

# sql = "INSERT INTO usr (username, password, real_pass, uid, fName, lName) VALUES ('admin', 'admin', 'admin', 0, 'Y', 'pers')"
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

##############################VALID USERNAME FOR REGISTERATION
#in client -> fname & lname -> username
def valid_username_reg (name, fname, lname) :
    sql = "SELECT username FROM usr WHERE username = name"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0 :
        return False
    return True
##########################################

##############################VALID USERNAME
def valid_username (name) :
    sql = "SELECT username FROM usr WHERE username = name"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0 :
        return True
    return False
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

#############################CHANGE PASSWORD
def change_password (name, hsh, newhsh, newpwd) :
    if check_password(name, hsh) :
        sql = "UPDATE usr SET password = "+newhsh+" WHERE username = name";
        mycursor.execute(sql)
        connection.commit()

        sql = "UPDATE usr SET real_pass = "+newpwd+" WHERE username = name";
        mycursor.execute(sql)
        connection.commit()
        return True
    return False
############################################

#############################DELETE ACCOUNT
def dlt_account (name, hsh) :
    if check_password(name, hsh) :
        reset_database_user(name)
        return True
    return False
############################################

#############################SECURITY QUESTIONS
def secure_question (name, ans1, ans2, ans3) :
    sql = "INSERT INTO question (username, answer1, answer2, answer3) VALUES ("+name+", "+ans1+", "+ans2+", "+ans3+")";
    mycursor.execute(sql)
    connection.commit()
###############################################

#############################CHECK ANSWER OF QUESTION
def check_security_answer(name, ans1, ans2, ans3) :
    flag = True
    sql = "SELECT answer1 FROM question WHERE username = name"
    mycursor.execute(sql)
    mycursor = mycursor.fetchall()
    if mycursor != ans1 :
        flag = False

    sql = "SELECT answer2 FROM question WHERE username = name"
    mycursor.execute(sql)
    mycursor = mycursor.fetchall()
    if mycursor != ans2 :
        flag = False

    sql = "SELECT answer3 FROM question WHERE username = name"
    mycursor.execute(sql)
    mycursor = mycursor.fetchall()
    if mycursor != ans3 :
        flag = False
    return flag
#####################################################

#############################CHANGE SECURITY QUESTIONS ANSWERS
def change_ans (name, qst, ans) :
    if qst == 1 :
        sql = "UPDATE question SET answer1 = "+ans+" WHERE username = name";
        mycursor.execute(sql)
        connection.commit()
        return True
    if qst == 2 :
        sql = "UPDATE question SET answer2 = "+ans+" WHERE username = name";
        mycursor.execute(sql)
        connection.commit()
        return True
    if qst == 3 :
        sql = "UPDATE question SET answer3 = "+ans+" WHERE username = name";
        mycursor.execute(sql)
        connection.commit()
        return True
    return False
##############################################################

#############################ADD FRIEND
#should be check
def add_friend (name, new_frnd) :
    if valid_username(new_frnd) == False :
        return False
    sql = "SELECT friend_cnt FROM contact WHERE username = name"
    mycursor.execute(sql)
    counter = mycursor.fetchall()

    sql = "UPDATE contact SET friend_cnt = counter + 1 WHERE username = name";
    mycursor.execute(sql)
    connection.commit()

    sql = "SELECT friends FROM contact WHERE username = name"
    mycursor.execute(sql)
    friends_list = mycursor.fetchall()

    sql = "UPDATE contact SET friends = friends_list + "+new_frnd+" WHERE username = name";
    mycursor.execute(sql)
    connection.commit()
    return True
#######################################