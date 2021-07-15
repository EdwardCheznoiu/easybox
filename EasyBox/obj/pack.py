import sys
sys.path.append('D:\Facultate\PythonApps\EasyBox')
from conn import conn
curs = conn.cursor()

class Packs():
    
    def __init__(self, pack_id = None):
        self.pack_id = pack_id
        
    def pk_id(self):
        return self.pack_id
        
    def insertIntoPack(self):
        try:
            curs.execute("INSERT INTO packs(pack_id) VALUES (%s)", (self.pack_id))
            conn.commit()
           
        except:
            print("Ceva nu a mers bine ")
    
 
    
    def getPacks(self):
          curs.execute("select pk.pack_id, us.fname, us.lname, pr.prod_name, pr.price from packs pk, products pr, packages pka, users us where pk.pack_id = pka.pack_id and pr.prod_id = pka.prod_id and us.user_id = pka.user_id")
          results = curs.fetchall()
          return results
      
    def getPackId(self):
        curs.execute("SELECT max(pack_id) from packs")
        result = curs.fetchone()
        return result