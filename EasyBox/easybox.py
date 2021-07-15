from flask import Flask, render_template, request, flash
from conn import conn
from datetime import date, datetime
import func
import os
app = Flask(__name__)

 

curs = conn.cursor()
 


#preluam data si ora curenta 
today = date.today()
date = today.strftime("%d/%m/%Y");
now = datetime.now()
hour = now.strftime("%d/%m/%Y %H:%M:%S")

@app.route('/')
@app.route('/home')
def index_page():
    return render_template('index.html', time = hour)


@app.route('/client', methods = ['POST', 'GET'])
def client_page():
    courierCode = request.form.get('usersub')
    if request.method == 'POST':
        if len(courierCode) > 6:
            flash("Codul introdus depaseste numarul maxim de caractere!")
            return render_template('curier.html', error = True, time = hour)
        if len(courierCode) < 6:
            flash("Codul introdus nu are numarul necesar de caractere")
            return render_template('curier.html', error = True, time = hour)
    if request.method == 'POST':    
        try:
            curs.execute("select distinct order_id from codes where code_gen = %s", (courierCode, ))
            order_id = curs.fetchall()
            order_id = order_id[0][0]
            curs.execute("select code_gen from codes where order_id = %s", (str(order_id), ))
            codes = curs.fetchall()
        except:
            flash("Codul introdus nu apartine unei comenzi active!")
            return render_template('client.html', error = True, time = hour)   
    if request.method == 'POST':
 
        try:
            curs.execute("select distinct status from finalorders where order_id = %s and status = 'livrat'", (str(order_id), ))
            ord_status = curs.fetchall()
            if courierCode == codes[0][0] and not ord_status:
                curs.execute("select couriers.currier_name, companies.company_id, drawer.drawer_id, products.prod_name, users.fname, users.lname from deposit, drawer, users, products, finalorders, orders, couriers, companies where orders.order_id = finalorders.order_id and products.prod_id = finalorders.prod_id and users.user_id = finalorders.user_id and drawer.drawer_id = deposit.drawer_id and orders.order_id = deposit.order_id and couriers.courier_id = deposit.courier_id and companies.company_id = couriers.company_id and finalorders.prod_id = deposit.prod_id and finalorders.status='easybox' and orders.order_id = %s", (str(order_id), ))
                prod = curs.fetchall()
             
                curs.execute("select drawer_id from codes where code_gen = %s", (courierCode, ))
                drawer_id = curs.fetchall()
                curs.execute("select finalord_id from codes where code_gen = %s", (courierCode, ))
                finalord_id = curs.fetchall()
                for finord in finalord_id:
                    curs.execute("update finalorders set status = 'livrat' where order_id = %s", (str(order_id),))
                conn.commit()
                curs.execute("select * from finalorders where order_id = %s and status = 'curier'", (str(order_id), ))
                orders_left = curs.fetchall()
               
                func.sendMail('D:/Facultate/PythonApps/EasyBox/'+str(order_id) +".png")
                
                os.remove('D:/Facultate/PythonApps/EasyBox/'+str(order_id) +".png")
                return render_template('client_succes.html', error = False, time = hour, products = prod, another = True)
                     
            else:
                flash("Codul introdus nu apartine unei comenzi active!")
                return render_template('client.html', error = True, time = hour)
        except:
            flash("A aparut o eroare in timpul executiei")
            return render_template('client.html', error = True, time = hour)
           
             
    return render_template('client.html', time = hour)

 
 
@app.route('/curier', methods = ['POST', 'GET'])
def curier_page():
    
    courierCode = request.form.get('usersub')
    if request.method == 'POST':
        if len(courierCode) > 6:
            flash("Codul introdus depaseste numarul maxim de caractere!")
            return render_template('curier.html', error = True, time = hour)
        if len(courierCode) < 6:
            flash("Codul introdus nu are numarul necesar de caractere")
            return render_template('curier.html', error = True, time = hour)
    
   
    if request.method == 'POST':
        try:
            curs.execute("select distinct order_id from codes where code_gen = %s", (courierCode, ))
            order_id = curs.fetchall()
            order_id = order_id[0][0]
            curs.execute("select distinct status from finalorders where order_id = %s and status = 'easybox'", (str(order_id), ))
            ord_status = curs.fetchall()
            curs.execute("select code_gen from codes where order_id = %s", (str(order_id), ))
            codes = curs.fetchall()
        except:
            flash("Codul introdus nu apartine unei comenzi active!")
            return render_template('curier.html', error = True, time = hour)
        if courierCode == codes[0][0] and not ord_status:
            curs.execute("select drawer_id from codes where code_gen = %s", (courierCode, ))
            drawer_id = curs.fetchall()
            curs.execute("select finalord_id from codes where code_gen = %s", (courierCode, ))
            finalord_id = curs.fetchall()
            for finord in finalord_id:
                curs.execute("update finalorders set status = 'easybox' where order_id = %s", (str(order_id),))
            conn.commit()
            curs.execute("select * from finalorders where order_id = %s and status = 'curier'", (str(order_id), ))
            orders_left = curs.fetchall()
            curs.execute("select couriers.currier_name, companies.company_id, drawer.drawer_id, products.prod_name, users.fname, users.lname from deposit, drawer, users, products, finalorders, orders, couriers, companies where orders.order_id = finalorders.order_id and products.prod_id = finalorders.prod_id and users.user_id = finalorders.user_id and drawer.drawer_id = deposit.drawer_id and orders.order_id = deposit.order_id and couriers.courier_id = deposit.courier_id and companies.company_id = couriers.company_id and finalorders.prod_id = deposit.prod_id and finalorders.status='easybox' and orders.order_id = %s", (str(order_id), ))
            prod = curs.fetchall()
        
            func.sendMail('D:/Facultate/PythonApps/EasyBox/'+str(order_id) +".png")
            return render_template('curier_succes.html', error = False, time = hour, products = prod, another = True)
                 
        else:
            flash("Codul introdus nu apartine unei comenzi active!")
            return render_template('curier.html', error = True, time = hour)
           
 
    return render_template('curier.html', time = hour)

@app.route('/curier_succes')
def curier_succes():
   return render_template('curier_succes.html')
app.secret_key = "Cheie super secreta"
app.run(debug=True)
