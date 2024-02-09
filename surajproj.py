# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 22:31:34 2018

@author:SURAJNRAIKAR
"""


import sqlite3,time,sys
import hashlib
def create(dbname):
    
    with sqlite3.connect(dbname) as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS student(
                                           USN text PRIMARY KEY,
                                           name text NOT NULL,
                                           scheme text NOT NULL,
                                           email text,
                                           phno integer,
                                           stdno integer,
                                           FOREIGN KEY (stdno) REFERENCES department (dno));
                                           ''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS department(
                                           dno  integer PRIMARY KEY,
                                           dname   text,
                                           dofficeno int);
                                           ''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS subject (
                                            subcode  text PRIMARY KEY,
                                            subtitle  text NOT NULL,
                                            sem integer NOT NULL,
                                            sjdno int,
                                            FOREIGN KEY (sjdno) REFERENCES department (dno));
                                           ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS internal(
                                            iUSN  text PRIMARY KEY,
                                            first int,
                                            second int,
                                            third int,
                                            interavg int NOT NULL,
                                            scored int NOT NULL,
                                            subcode  text,
                                            FOREIGN KEY (iUSN) REFERENCES student (USN),
                                            FOREIGN KEY (subcode) REFERENCES subject (subcode));
                                            ''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS marks(
                                                mUSN text PRIMARY KEY,
                                                internal integer NOT NULL,
                                                external text,
                                                total text,
                                                result char(1),
                                                FOREIGN KEY (mUSN) REFERENCES student (USN));
                                                ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                username  text UNIQUE,
                                                firstname  text NOT NULL,
                                                surname text NOT NULL,
                                                password  text NOT NULL);
                                                ''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS login_session(
                                                id INTEGER PRIMARY KEY,
                                                date DATE,
                                                start_time TIME,
                                                end_time TIME,
                                                FOREIGN KEY (id) REFERENCES user (id));
                                                ''')
                                                     
        
        
        db.commit()
        cursor.execute("SELECT * FROM user")
        print(cursor.fetchall())
        cursor.close()
        
    
    
    
 
def login(dbname):
    
    
    while True:# for i in range(3):
        username = input("please enter your username: ")
        password = input("please enter your password: ")
        with sqlite3.connect(dbname) as db:
            cursor = db.cursor()
                
        
            
        m=hashlib.md5()
        m.update(password.encode('utf-8'))
        hash1=m.hexdigest()
        del m
        try:
            
            find_user =("SELECT * FROM user WHERE username = ? AND password = ?")
            cursor.execute(find_user,[(username),(hash1)])
            results = cursor.fetchall()

            if results:
                for i in results:
                    print("welcome user "+i[2])
                    #return("exit")
                break
            
            else:
                print("Username and password invalid")
                again =input("Do you want to try again?(y/n):")
                if again.lower() =="n":
                    print("see you later")
                    time.sleep(1)
                    #return("exit")
                    break
    
        except sqlite3.OperationalError as e:
            create(dbname)
        except Exception as e:
            print(e)
    cursor.close()
    db.close()
    
def newUser(dbname):
    m=hashlib.md5()
    found = 0
    while found == 0:
        username = input("please enter a username: ")
        with sqlite3.connect(dbname) as db:
                cursor = db.cursor()
        
        try:
            findUser = ("SELECT * FROM user WHERE username = ?")
            cursor.execute(findUser,[(username)])

            if cursor.fetchall():
                print("Username is taken, please try again")
            else:
                found = 1;
        
        except sqlite3.OperationalError as e:
            create(dbname)
        except Exception as e:
            print(e)
    firstname = input("Enter your first name: ")
    surname = input("Enter your lastname: ")
    password = input("please enter your password: ")
    password1 = input("please enter your password again: ")
    while password != password1:
        print("Your password didn't match, please try again!!!!!!")
        password = input("please enter your password: ")
        password1 = input("please enter your password again: ")
    m.update(password.encode('utf-8'))
    hash2=m.hexdigest()
    insertdata = '''INSERT INTO user(username,firstname,surname,password)
    VALUES(?,?,?,?)'''
    cursor.execute(insertdata,[(username),(firstname),(surname),(hash2)])
    db.commit()
    cursor.close()
    db.close()
    del m

def menu(dbname):
    while True:
        print("Welcome to database ....... ")
        menu =('''
   1 - Create New User login
   2 - Login
   3 - Exit\n''')
        
        userchoice = input(menu)


        if userchoice == "1":
           newUser(dbname)

           
        elif userchoice == "2":
            login(dbname)
            
        elif userchoice == "3":
             print("see you later")
             sys.exit()
             
        else:            
           print("Command not in given choice ")

if __name__ == "__main__":
    menu("studb1.db")
     
