import sys
sys.path.append('D:\Facultate\PythonApps\EasyBox')
from conn import conn
curs = conn.cursor()

class Packages():
    
    def __init__(self, pack_id = None, prod_id = None, user_id = None):
        self.pack_id = pack_id
        self.prod_id = prod_id
        self.user_id = user_id
        
    def insertIntoPackages(self):
        try:
            curs.execute("INSERT INTO packages(pack_id, prod_id, user_id) VALUES (%s, %s, %s)", (self.pack_id, self.prod_id, self.user_id))
            conn.commit()
           
        except:
            print("Ceva nu a mers bine ")

