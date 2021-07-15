import sys
sys.path.append('D:\Facultate\PythonApps\EasyBox')
from conn import conn
curs = conn.cursor()

class Couriers():
    
    def __init__(self, courier_name = None):
        self.courier_name = courier_name
    
    def getCouriers(self):
        try:
            curs.execute("select couriers.courier_id, couriers.currier_name, companies.company_name from couriers, companies where couriers.courier_id = companies.company_id")
            results = curs.fetchall()
            return results
        except: 
            print("Ceva nu a mers bine")
    
    def courierSearch(self, something):
       curs.execute("select couriers.courier_id, couriers.currier_name, companies.company_name from couriers, companies where couriers.courier_id = companies.company_id and currier_name LIKE '{}%' ORDER BY courier_id".format(something))
       results = curs.fetchall()
       return results