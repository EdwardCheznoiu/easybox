import sys
sys.path.append('D:\Facultate\PythonApps\EasyBox')
from conn import conn
from flask import redirect, url_for
curs = conn.cursor()
class Users():
    
    def __init__(self, fname = None, lname = None, email = None, town= None, phone_nr = None):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.town = town
        self.phone_nr = phone_nr
        
    def insertUser(self):
        try:
            curs.execute("INSERT INTO users(fname, lname, email, town, phone_nr) VALUES (%s, %s, %s, %s, %s)",
                        (self.fname, self.lname, self.email, self.town, self.phone_nr,))
            conn.commit()
        except:
            return redirect(url_for('error_page'))
    
    def getUsers(self):
         curs.execute("SELECT * FROM users ORDER BY user_id")
         results = curs.fetchall()
         return results
     
    def getUser(self, id):
        try:
            curs.execute("SELECT * FROM users WHERE user_id = %s ", (id,))
            result = curs.fetchone() 
            return result
        except:
            print("Ceva nu a mers bine")
    
    
    def updateUser(self, user_id):
        try:
            curs.execute("update users set fname = %s, lname = %s, email = %s, town = %s, phone_nr = %s where user_id = %s", (self.fname, self.lname, self.email, self.town, self.phone_nr, user_id))
            conn.commit()
        except:
            print("Ceva nu a mers bine")
    
    def getLastUser(self):
        try:
            curs.execute("SELECT max(user_id) from users")
            result = curs.fetchone()
            return result
        except:
            print("Ceva nu a mers bine")
   
    def delUser(self, id):
        try:
            curs.execute("DELETE FROM users WHERE user_id = %s", (id,))
            conn.commit()
        except:
            print("Ceva nu a mers bine")
            
    def userSearch(self, something):
       curs.execute("SELECT user_id, fname, lname FROM users WHERE fname LIKE '{}%' OR lname LIKE '{}%' ORDER BY user_id".format(something, something))
       results = curs.fetchall()
       return results
   
 