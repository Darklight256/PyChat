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
#################################################

##############################DATABASE ERASE
def reset_database_user (name) :
    sql = "DELETE FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    connection.commit()
#############################################

##############################SET NEW PASSWORD
def set_new_password(name, fname, lname, pwd) :
    sql = "SELECT MAX(uid) FROM `usr`"
    mycursor.execute(sql)
    UID = mycursor.fetchall()[0] + 1

    hsh = hashlib.pbkdf2_hmac('sha256', pwd, b'salt', 100000)

    sql = "INSERT INTO `usr` (username, password, real_pass, uid, fName, lName) VALUES ("+name+", "+hsh+", "+pwd+" , "+str(UID)+", "+fname+", "+lname+")";
    mycursor.execute(sql)
    connection.commit()
##############################################

##############################VALID USERNAME FOR REGISTERATION
#in client -> fname & lname -> username
def valid_username_reg (name, fname, lname) :
    sql = "SELECT username FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0 :
        return False
    return True
##########################################

##############################VALID USERNAME
def valid_username (name) :
    sql = "SELECT username FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0 :
        return True
    return False
##########################################

#############################CHECK PASSWORD
def check_password(name, hsh) :
    sql = "SELECT password FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult == hsh :
        return True
    return False
###########################################

#############################CHANGE PASSWORD
def change_password (name, hsh, newhsh, newpwd) :
    if check_password(name, hsh) :
        sql = "UPDATE `usr` SET password = "+newhsh+" WHERE username = " + name
        mycursor.execute(sql)
        connection.commit()

        sql = "UPDATE `usr` SET real_pass = "+newpwd+" WHERE username = " + name
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
    sql = "INSERT INTO `question` (username, answer1, answer2, answer3) VALUES ("+name+", "+ans1+", "+ans2+", "+ans3+")";
    mycursor.execute(sql)
    connection.commit()
###############################################

#############################CHECK ANSWER OF QUESTION
def check_security_answer(name, ans1, ans2, ans3) :
    sql = "SELECT answer1, answer2, answer3 FROM `question` WHERE username = " + name
    mycursor.execute(sql)
    myres = mycursor.fetchall()
    if myres[0] == ans1 and myres[1] == ans2 and myres[2] == ans3:
        return True
    return False
#####################################################

#############################CHANGE SECURITY QUESTIONS ANSWERS
def change_ans (name, qst, ans) :
    if qst == 1 :
        sql = "UPDATE `question` SET answer1 = "+ans+" WHERE username = " + name
        mycursor.execute(sql)
        connection.commit()
        return True
    if qst == 2 :
        sql = "UPDATE `question` SET answer2 = "+ans+" WHERE username = " + name
        mycursor.execute(sql)
        connection.commit()
        return True
    if qst == 3 :
        sql = "UPDATE `question` SET answer3 = "+ans+" WHERE username = " + name
        mycursor.execute(sql)
        connection.commit()
        return True
    return False
##############################################################

#############################ADD FRIEND
def add_friend (name, new_frnd) :
    if valid_username(new_frnd) == False :
        return False

    sql = "SELECT uid FROM `usr` WHERE username = " + new_frnd
    mycursor.execute(sql)
    new_uid = mycursor.fetchall()

    sql = "SELECT fuid FROM `contact` WHERE username = " + name + "and fuid = " + str(new_uid)
    mycursor.execute(sql)
    exist = mycursor.fetchall()

    if len(exist) > 0 :
        return False

    sql = "INSERT INTO `contact` (fuid) VALUES (str(new_id))"
    mycursor.execute(sql)
    connection.commit()

    return True
#######################################

#############################DELETE FRIEND
def del_friend (name, del_frnd) :
    if valid_username(del_frnd) == False :
        return False
    sql = "SELECT uid FROM `usr` WHERE username = " + del_frnd
    mycursor.execute(sql)
    new_uid = mycursor.fetchall()

    sql = "DELETE FROM `contact` WHERE username = " + name + "and fuid = " + new_uid
    mycursor.execute(sql)
    connection.commit()

    return True
#######################################