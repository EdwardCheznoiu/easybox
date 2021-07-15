import sys
sys.path.append('D:\Facultate\PythonApps\EasyBox')
from conn import conn
curs = conn.cursor()

class Products():
    
    def __init__(self, name = None, price = None, weight = None, desc = None):
        self.name = name  
        self.price = price
        self.weight = weight
        self.desc =  desc
    
    def insertProd(self):
        try:
            curs.execute("INSERT INTO products(prod_name,price, weight, description) VALUES (%s, %s, %s, %s)",
                        (self.name, self.price, self.weight, self.desc))
            conn.commit()
        except:
            print("Ceva nu a mers bine ")
    
    def getProds(self):
        curs.execute("SELECT * from products")
        results = curs.fetchall()
        return results
    
    def delProd(self, id):
         try:
            curs.execute("DELETE FROM products WHERE prod_id = %s", (str(id), ))
            conn.commit()
         except:
            print("Ceva nu a mers bine")
            
    def prodSearch(self, something):
       curs.execute("SELECT prod_id, prod_name FROM products WHERE prod_name LIKE '{}%' ORDER BY prod_id".format(something))
       results = curs.fetchall()
       return results