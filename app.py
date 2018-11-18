from flask import Flask, render_template,url_for, redirect, request, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import os
from os.path import dirname, join
import json
from werkzeug.security import generate_password_hash, check_password_hash

path=os.getcwd()
filename=(path+ "/templates/db.json")
#filename=os.path.join(dirname(__file__), "../templates/db.json")
with open(filename) as f:
    db=json.load(f)
    f.close()
app = Flask(__name__)
Bootstrap(app)


# Congigure db
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)
app.config['SECRET_KEY']=os.urandom(24)



@app.route('/_index')
def _index():
    #return url_for(about)
    #this url_for will return the url of function about , which is /about
    #return redirect(url_for(about))
    fruits=['Apple', 'Mango','Orange']

    return render_template('_index.html', ht_fruits=fruits)




@app.route('/about')
def about():
    cur=mysql.connection.cursor()
    #cur.execute("INSERT INTO user(user_name) values(%s)", ['Mike'])
    #mysql.connection.commit()

    result_value=cur.execute("SELECT * FROM user ")
    if result_value >0 :
        users=cur.fetchall()
        #print(users)
        first_user= users[0][0]
        return ( first_user)
    return render_template('about.html', ht_first_user=first_user)

@app.route('/css', methods=["GET", "POST"])
def css():
    if request.method=='POST':
        #return 'Successfully registered'
        return request.form ['password']
    return render_template('css.html')


@app.route('/insert_name', methods=["GET", "POST"])
def insert_name():
    cur=mysql.connection.cursor()
    if cur.execute("INSERT INTO user(user_name) VALUES ('BEN')"):
        mysql.connection.commit()
        return 'success', 201
    return render_template('insert_name.html')



@app.route('/')
def home():
    #return url_for(about)
    #this url_for will return the url of function about , which is /about
    #return redirect(url_for(about))
    #fruits=['Apple', 'Mango','Orange']

    return render_template('index.html')

@app.route('/employee_register', methods=["GET", "POST"])
def employee_register():
    if request.method=='POST':
        try:
            form=request.form
            name=form['name']
            age=form['age']

            #hashing the name ...
            #name=generate_password_hash(name)

            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO employee(name, age) VALUES (%s, %s)", (name, age))
            mysql.connection.commit()
            flash("successfully inserted data", 'success')
        except:
            flash("Fail to insert data", 'danger')
        #return 'success'
    return render_template('employee_register.html')


@app.route('/employee_form', methods=["GET","POST"])
def employee_form():
    cur=mysql.connection.cursor()
    result_value=cur.execute("SELECT * from employee")
    if result_value>0:
        employees=cur.fetchall()
        #session['username']=employees[0]['name']
        #session['username']=check_password_hash(employees[0]['name'],'Daisy')
        return render_template('employee_form.html', ht_employees=employees)

@app.errorhandler(404)
def page_not_found(e):
    return 'This page was not found'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
