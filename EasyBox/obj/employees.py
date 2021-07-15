import sys
sys.path.append('D:\Facultate\PythonApps\EasyBox')
from conn import conn
curs = conn.cursor()

class Employees():
    
    def __init__(self, employee_name = None):
        self.employee_name = employee_name
    
    def getEmployees(self):
        try:
            curs.execute("SELECT * FROM employees ORDER BY employee_id")
            results = curs.fetchall()
            return results
        except:
            print("ceva nu a mers bine")