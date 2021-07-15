import sys
sys.path.append('D:\Facultate\PythonApps\EasyBox')
from conn import conn
curs = conn.cursor()

class Orders():
    
    def __init__(self, order_id = None, user_id = None, prod_id = None, courier_id = None, employee_id = None):
        self.order_id = order_id
        self.user_id = user_id
        self.prod_id = prod_id
        self.courier_id = courier_id
        self.emoployee_id = employee_id 
    
    def insertIntoOrders(self):
        try:
            curs.execute("INSERT INTO finalorders(order_id, user_id, prod_id, courier_id, employee_id) VALUES (%s, %s, %s, %s, %s)", (self.order_id, self.user_id, self.prod_id, self.courier_id, self.employee_id))
            conn.commit()
        except:
            print("Ceva nu a mers bine in Orders")
        
    def getOrders(self):
        curs.execute("select orders.order_id, products.prod_id, users.fname, users.lname, products.prod_name, employees.employee_name from orders, users, products, employees, finalorders where orders.order_id = finalorders.order_id and products.prod_id = finalorders.prod_id and users.user_id = finalorders.user_id and employees.employee_id = finalorders.employee_id and finalorders.status = 'depozit' order by orders.order_id")
        results = curs.fetchall()
        return results