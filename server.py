import hashlib
import random
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

##############################GET INFO CLASS
#1.fname 2.lname 3.username 4.uid 5.random status
class usr_info :
    def __init__ (self, fname, lname, name, uID, stts) :
        self.Fname(fname)
        self.Lname(lname)
        self.username(name)
        self.UID(uID)
        self.rand_stts(stts)
############################################

##############################GET INFO FUNCTION
def all_info_uid (uID) :
    sql = "SELECT fName FROM `usr` WHERE uid = " + uID
    mycursor.execute(sql)
    usrfname = mycursor.fetchall()

    sql = "SELECT lName FROM `usr` WHERE uid = " + uID
    mycursor.execute(sql)
    usrlname = mycursor.fetchall()

    sql = "SELECT username FROM `usr` WHERE uid = " + uID
    mycursor.execute(sql)
    usrname = mycursor.fetchall()

    sql = "SELECT uid FROM `random` WHERE uid = " + uID
    mycursor.execute(sql)
    res_size = mycursor.fetchall()
    
    rndstts = 0

    if len(res_size) > 0 :
        rndstts = 1

    result = usr_info(usrfname, usrlname, usrname, str(uID), str(rndstts))
    return result
###############################################

##############################GET INFO FUNCTION
def all_info_usrname (name):
    sql = "SELECT fName FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    usrfname = mycursor.fetchall()

    sql = "SELECT lName FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    usrlname = mycursor.fetchall()

    sql = "SELECT uid FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    UID = mycursor.fetchall()

    sql = "SELECT uid FROM `random` WHERE uid = " + UID
    mycursor.execute(sql)
    res_size = mycursor.fetchall()

    rndstts = 0

    if len(res_size) > 0:
        rndstts = 1

    result = usr_info(usrfname, usrlname, name, str(UID), str(rndstts))
    return result
###############################################

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
###############################################################

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

#############################INSERT ANSWERS
def secure_question (name, ans1, ans2, ans3) :
    sql = "INSERT INTO `question` (username, answer1, answer2, answer3) VALUES ("+name+", "+ans1+", "+ans2+", "+ans3+")";
    mycursor.execute(sql)
    connection.commit()
###########################################

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
##########################################

#############################CHANGE RANDOM STATUS
def change_random_status (name, stts) :
    sql = "SELECT uid FROM `usr` WHERE username = " + name
    mycursor.execute(sql)
    name_uid = mycursor.fetchall()

    if stts == 1 :
        sql = "SELECT uid FROM `random` WHERE uid = " + str(name_uid)
        mycursor.execute(sql)
        myres = mycursor.fetchall()
        if myres > 0 :
            pass
        sql = "INSERT INTO `random` (uid) VALUES (str(name_uid))"
        mycursor.execute(sql)
        connection.commit()
    else :
        sql = "DELETE FROM `random` WHERE uid = " + str(name_uid)
        mycursor.execute(sql)
        connection.commit()
##########################################

#############################RANDOM MATCHING
#random match by @darklight256
#########################################