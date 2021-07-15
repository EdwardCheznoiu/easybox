from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from conn import conn
import sys
from barcode import Code128
from barcode.writer import ImageWriter
import string
import random
import func
import os
sys.path.append('D:\Facultate\PythonApps\EasyBox\obj')
from users import Users
from products import Products
from pack import Packs
from packages import Packages
from couriers import Couriers
from employees import Employees
from orders import Orders
app = Flask(__name__)

curs = conn.cursor()
@app.route('/')
def site_index():
    return render_template('site_index.html')

user = Users()
a = user.getUsers()
lenUsers = len(a) + 2

prod = Products()
b= prod.getProds()  
lenProd = len(b) + 2

@app.route('/client')
def user_insert():
    a = user.getUsers()
    lenUsers = len(a[0])
    return render_template('site_clienti.html', users = a, leng = lenUsers)


@app.route('/client', methods=['POST'])
def user_insert_form():
    warning = True
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    address = request.form['address']
    phone_nr = request.form['phone_nr']
    if not fname and not lname and not email and not address and not phone_nr:
        return render_template('site_clienti.html', users = a, leng = lenUsers, ht = "Nu ai completat nici un camp", error = warning)
    if not fname:
        return render_template('site_clienti.html', users = a, leng = lenUsers, ht = "Nu ai completat campul 'Prenume'", error = warning)
    if not lname:
        return render_template('site_clienti.html', users = a, leng = lenUsers, ht = "Nu ai completat campul 'Nume'", error = warning)
    if not email:
        return render_template('site_clienti.html', users = a, leng = lenUsers, ht = "Nu ai completat campul 'Email'", error = warning)
    if not address:
        return render_template('site_clienti.html', users = a, leng = lenUsers, ht = "Nu ai completat campul 'Adresa'", error = warning)
    if not phone_nr:
        return render_template('site_clienti.html', users = a, leng = lenUsers, ht = "Nu ai completat campul 'Numar telefon'", error = warning)
    
    # curs.execute("""INSERT INTO users(fname, lname, email, address, phone_nr) VALUES (%s, %s, %s, %s, %s)""", (fname, lname, email, address, phone_nr))
    # conn.commit()
    user = Users(fname, lname, email, address, phone_nr)
    user.insertUser()
    warning = False
    ab = user.getUsers()
    leng = len(ab[0])
    return render_template('site_clienti.html', users = ab, leng = leng, ht = "Ai adaugat un client nou!", error = warning)


@app.route('/edit/<int:id>')
def edit_client(id):
    return render_template('edit_client.html', user_id = id)

@app.route('/editf/<int:id>', methods = ['GET', 'POST'])
def edit_client_form(id):
    if request.method == 'POST':
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        address = request.form.get("address")
        phone_nr = request.form.get("phone_nr")
        user = Users(fname, lname, email, address, phone_nr)
        user.updateUser(id)
        flash("Ai editat datele cu succes!")
        return redirect(url_for('user_insert',  users = a, leng = lenUsers, error = False))
    return render_template('edit_client.html')
    
@app.route('/delete/<int:id>')
def delete_client(id):
    user.delUser(id)
    ab = user.getUsers()
    leng = len(ab) + 2
    flash("Intrarea a fost stearsa cu succes!")
    return redirect(url_for('user_insert', user = ab, leng = leng))


@app.route('/produs')
def produces_insert():
    b = prod.getProds()
    leng = len(b)
    return render_template('site_produse.html', products = b, leng = leng)

@app.route('/produs', methods=['POST'])
def produces_insert_form():
    warning = True
    name = request.form['prodname']
    price = request.form['prodprice']
    weight = request.form['prodweight']
    desc = request.form['proddesc']
    if not name and not price and not weight and not desc:
        return render_template('site_produse.html', products = b, leng = lenProd, ht = "Nu ai completat nici un camp", error = warning)
    if not name:
         return render_template('site_produse.html', products = b, leng = lenProd, ht = "Nu ai completat campul 'Nume produs'", error = warning)
    if not price:
         return render_template('site_produse.html', products = b, leng = lenProd, ht = "Nu ai completat campul 'Pret'", error = warning)
    if not weight:
         return render_template('site_produse.html', products = b, leng = lenProd, ht = "Nu ai completat campul 'Greutate'", error = warning)
    if not desc:
         return render_template('site_produse.html', products = b, leng = lenProd, ht = "Nu ai completat campul 'Descriere'", error = warning)
    prod = Products(name, price, weight, desc)
    prod.insertProd()
    warning = False
    bb = prod.getProds()
    lenProd2 = len(bb)
    return render_template('site_produse.html', products = bb, leng = lenProd2, ht = "Ai inregistrat un nou produs!", error = warning)


@app.route('/delete_prod/<int:id>')
def delete_pod(id):
    prod.delProd(id)
    a = prod.getProds()
    leng = len(a)
    flash("Intrarea a fost stearsa cu succes!")
    return redirect(url_for('produces_insert', prod = a, leng = leng))


@app.route('/comenzi')
def order_insert():
    courier = Couriers()
    employee = Employees()
    c = courier.getCouriers()
    e = employee.getEmployees()
    a = user.getUsers()
    leng = len(a[0]) 
    curs.execute("select * from easybox")
    easybox = curs.fetchall()
    return render_template('site_comenzi.html', users = a, products = b, leng = leng, couriers = c, employees = e, easybox = easybox)

@app.route('/comenzi', methods=['POST'])
def order_insert_form():
   
    courier = Couriers()
    employee = Employees()
    c = courier.getCouriers()
    e = employee.getEmployees()
    a = user.getUsers()
    leng = len(a[0]) 
    curs.execute("select * from easybox")
    easybox = curs.fetchall()
    warning = True
    if request.method == 'POST':
        listOfUsers = request.form.get('userlist')
        listOfProds = request.form.getlist('prodlist') 
        listOfCouriers = request.form.get('courierlist')
        listOfEmployees = request.form.get('employee')
        listOfEasybox = request.form.get('easyboxlist')
        curs.execute("select max(order_id) from orders")
        order_id = curs.fetchone()
        if not listOfUsers and not listOfEasybox and not listOfProds:
            flash("Trebuie sa selectezi un client, un easybox si cel putin un produs!")
            return render_template('site_comenzi.html', users = a, products = b, leng = leng, couriers = c, employees = e, easybox = easybox, error = True)
        if not listOfUsers:
            flash("Trebuie sa selectezi un client!")
            return render_template('site_comenzi.html', users = a, products = b, leng = leng, couriers = c, employees = e, easybox = easybox, error = True)
        if not listOfEasybox:
            flash("Trebuie sa selectezi un easybox!")
            return render_template('site_comenzi.html', users = a, products = b, leng = leng, couriers = c, employees = e, easybox = easybox, error = True)
        if not listOfProds:
            flash("Trebuie sa selectezi cel putin un produs!")
            return render_template('site_comenzi.html', users = a, products = b, leng = leng, couriers = c, employees = e, easybox = easybox, error = True)
        if order_id[0] == None:
            order_id = 1
            curs.execute("insert into orders (order_id) values(1)")
            conn.commit()
        else:
            order_id, = order_id
            order_id += 1
            order_id = (order_id,)
            curs.execute("insert into orders (order_id) values(%s)", (order_id))
            conn.commit()
        order_id, = order_id
        order_id = str(order_id)
        for prod in listOfProds:
              curs.execute("INSERT INTO finalorders(order_id, user_id, prod_id, employee_id, ebox_id) VALUES (%s, %s, %s, %s, %s)", (order_id, listOfUsers, prod, listOfEmployees, listOfEasybox))
              conn.commit()
        order = Orders()
        o = order.getOrders()
        courier = Couriers()
        employee = Employees()
        c = courier.getCouriers()
        e = employee.getEmployees()
        curs.execute("select * from easybox")
        easybox = curs.fetchall()
        flash("Ai adaugat o comanda noua!")
        return render_template('site_comenzi.html', users = a, products = b, error = False, couriers = c, employees = e, easybox = easybox)
    return render_template('site_comenzi.html', users = a, products = b, leng = leng, couriers = c, employees = e, easybox = easybox)

@app.route('/colete', methods=['POST', 'GET'])
def packages():
    courier = Couriers()
    employee = Employees()
    order = Orders()
    c = courier.getCouriers()
    e = employee.getEmployees()
    o = order.getOrders()
  
    if request.method == 'POST':
        orders = request.form.getlist('orderlist')
        courier = request.form.getlist('courierlist')
        drawer = request.form.getlist('drawerlist')
        uid = request.form.get('hiddenuser')
        usd = request.form.getlist('hiddenusdid');
        warning = True
        for i in range(0, len(usd)):
            usd[i] = int(usd[i])
        if uid:
            uid = int(uid)
        if len(orders) == 0: 
            flash("Nu ai selectat nici o comanda!")
            return render_template('site_colete.html', couriers = c, employees = e, orders = o, error = warning)
        if len(courier) == 0:
            flash("Nu ai selectat nici un curier!")
            return render_template('site_colete.html', couriers = c, employees = e, orders = o, error = warning)
        if len(drawer) == 0:
            flash("Nu ai selectat nici un sertar!")
        if len(drawer) != 1:
            flash("Nu poti selecta mai multe sertare pentru un singur colet!")
            return render_template('site_colete.html', couriers = c, employees = e, orders = o, error = warning)
        if len(courier) > 1:
           flash("Nu poti selecta mai multi curieri pentru un singur colet!")
           return render_template('site_colete.html', couriers = c, employees = e, orders = o, error = warning)
        for i in range(1, len(orders)):
           if(orders[i] != orders[i-1]):
               flash("Nu poti selecta comenzi cu id diferit")
               o = order.getOrders()
               return render_template('site_colete.html', couriers = c, employees = e, orders = o, error = warning) 
        for orde in orders:
            curs.execute("insert into deposit (drawer_id, order_id, prod_id, courier_id) values (%s, %s, %s, %s)", (drawer[0], orde, usd[uid], courier[0]))
            conn.commit()
            curs.execute("update finalorders set status = 'curier' where order_id = %s and prod_id = %s ", (orde, usd[uid]))
            conn.commit()
            curs.execute("update drawer set status_drawer = true where drawer_id = %s ", (drawer[0], ))
            conn.commit()
        isImage = os.path.isfile('D:/Facultate/PythonApps/EasyBox/'+str(orders[0]) +".png")
        code = string.ascii_uppercase + string.digits
        code = ''.join(random.sample(code*6, 6))
        if not isImage:
            generated_code = Code128(code, writer=ImageWriter())
            generated_code.save(str(orders[0]))
        curs.execute("select distinct code_gen from codes where order_id = %s", (orders[0],))
        codedupl = curs.fetchall()
        curs.execute("select finalord_id from finalorders where order_id = %s and prod_id = %s", (orders[0], usd[uid]))
        finalord_id = curs.fetchone()
        if codedupl:
             curs.execute("insert into codes (order_id, drawer_id, finalord_id, code_gen) values (%s, %s, %s, %s)", (orders[0], drawer[0], finalord_id, codedupl[0]))
             conn.commit()
        else:
             curs.execute("insert into codes (order_id, drawer_id, finalord_id, code_gen) values (%s, %s, %s, %s)", (orders[0], drawer[0], finalord_id, str(code)))
             conn.commit()
    
    
        
        warning = False
        flash("Ai trimis produsele catre curier!")
        o = order.getOrders()
        return render_template('site_colete.html', couriers = c, employees = e, orders = o, error = warning)
        
   
    return render_template('site_colete.html', couriers = c, employees = e, orders = o)


@app.route('/usearch', methods=['POST', 'GET'])
def order_user_search():
    searchBox = request.form.get("dataPassed")
    uSearch = user.userSearch(searchBox)
    return jsonify(uSearch)


@app.route('/psearch', methods=['POST', 'GET'])
def order_prods_search():
    searchBox = request.form.get("pdataPassed")
    pSearch = prod.prodSearch(searchBox)
    return jsonify(pSearch)

@app.route('/csearch', methods = ['POST', 'GET'])
def order_courier_search():
    searchBox = request.form.get("cdataPassed")
    courier = Couriers()
    cSearch = courier.courierSearch(searchBox)
    return jsonify(cSearch)


@app.route('/drawer_select', methods=['POST', 'GET'])
def drawer_select():
    if request.method == 'POST':
        try:
            order_id = request.form.get("drawerdataPassed")
            curs.execute("select distinct finalorders.ebox_id from orders, finalorders where orders.order_id = finalorders.order_id and orders.order_id = %s ", (order_id, ))
            ebox_id = curs.fetchone()
            curs.execute("select drawer.drawer_id, drawer.volume, easybox.town, easybox.address from drawer, easybox where drawer.ebox_id = easybox.ebox_id and drawer.ebox_id = %s and drawer.status_drawer = false order by drawer_id", (ebox_id))
            drawers = curs.fetchall()
            return jsonify(drawers)
        except:
            return "undefined" 
    
if __name__ == "__main__":
    app.secret_key = "Cheie secreta"
    app.run(debug=True, host = "0.0.0.0", port = 9566)