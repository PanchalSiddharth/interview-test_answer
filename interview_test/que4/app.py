from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 


app = Flask(__name__) 
  
  
app.secret_key = 'sid'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'user'
  
mysql = MySQL(app) 

@app.route('/')
@app.route('/login/', methods=["GET","POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            messages='login succesfully'
            return redirect('addAddress')
        else:
            msg = 'Incorrect username/password!'
    
 
    return render_template('login.html', msg=msg)

@app.route('/register', methods =['GET', 'POST']) 
def saveUser(): 
    msg = '' 
    if request.method == 'POST': 
        username = request.form.get('username')
        password = request.form.get('pwd') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute("SELECT * FROM user WHERE `username` = '%s';"%(username)) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not username or not password : 
            msg = 'Please fill out the form !'
        else: 
            try:
                cursor.execute("INSERT INTO user(username,password) VALUES ('%s', '%s');"%(username, password)) 
                mysql.connection.commit() 
                msg = 'You have successfully registered !'
                return redirect('login',msg)
            except MySQLdb._exceptions.IntegrityError as err:
                msg ='user is already registered'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
   
    return render_template('save_user.html', msg = msg)


@app.route('/viewAddress',methods =['GET', 'POST'])
def viewAddress():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute("SELECT address.* FROM address RIGHT JOIN user ON user.id = address.user_id where user.username = '%s';"%(session['username']))
    addlist=[]
    for row in cursor.fetchall():
        addlist.append(row)

    cursor.close()
    return render_template('viewaddress.html',addlist=addlist)


@app.route('/addAddress', methods =['GET', 'POST']) 
def addAddress():
    if request.method == 'POST': 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
     
        street = request.form.get('street')
        state = request.form.get('state') 
        country = request.form.get('country') 
        pincode = request.form.get('pincode') 
        phoneno = request.form.get('phoneno') 
        cursor.execute("INSERT INTO address(street,state,country,pincode,phoneno,user_id) VALUES ('%s', '%s','%s','%s','%s','%s');"%(street,state,country,pincode,phoneno,session['id'])) 
        mysql.connection.commit()
        cursor.close()
        return redirect('viewAddress')
    return render_template('address.html')



@app.route('/editaddress', methods =['GET', 'POST']) 
def editAddress():
    if request.method=='GET':
        address_id = request.args.get('addressId')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute("SELECT * FROM address RIGHT JOIN user ON user.id = address.user_id where user.username = '%s' and address.id = '%s';"%( session['username'],address_id )) 
        for row in cursor.fetchall():
            cursor.close()
            return render_template('editAddress.html',row=row,address_id=address_id)
        return redirect('viewAddress')

    if request.method=='POST':
        address_id=request.form.get('address_id')

        street = request.form.get('street')
        state = request.form.get('state') 
        country = request.form.get('country') 
        pincode = request.form.get('pincode') 
        phoneno = request.form.get('phoneno') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute("SELECT * FROM address RIGHT JOIN user ON user.id = address.user_id where user.username = '%s' and address.id = '%s';"%( session['username'],address_id ))
        if len(cursor.fetchall()) == 0:
            return redirect('viewAddress')
        cursor.execute("UPDATE address SET street='%s',state='%s',country='%s',pincode='%s',phoneno='%s' WHERE `id` = '%s';"%(street,state,country,pincode,phoneno,address_id )) 
        mysql.connection.commit()

        cursor.close()
        return redirect('viewAddress')
        
app.run(debug=True)