from flask import Flask, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import hashlib
import os
import mysql.connector
conn = mysql.connector.connect(host='localhost',user='root',password='',database='dfw_python')
my_cursor = conn.cursor()
app = Flask(__name__)
app.config['UPLOAD_FOLDER']='C:\\Users\\bhanu\\Desktop\\dfw_portal\\static\\uploads'
app.secret_key = 'super-secret-key'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
now = datetime.now()
# class Observations(db.Model):
#     ids = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(255),nullable=True)
#     priority = db.Column(db.String(255),nullable=True)
#     # description = db.Column(db.Text,nullable=True)
    # user_id = db.Column(db.Integer,nullable=True)
    # department_id = db.Column(db.Integer,nullable=True)
    # created_by = db.Column(db.Integer,nullable=True)
    # updated_by = db.Column(db.Integer,nullable=True)
    # image = db.Column(db.String(255),nullable=True)
    # image_after = db.Column(db.String(255),nullable=True)
    # audit_date = db.Column(db.String(255),nullable=True)
    # target_date = db.Column(db.String(255),nullable=True)
    # close_date   = db.Column(db.String(255),nullable=True)
    # shift   = db.Column(db.String(255),nullable=True)
    # status   = db.Column(db.String(255),nullable=True)
    # # notification   = db.Column(db.Integer,nullable=True)
    # created_at   = db.Column(db.DateTime,nullable=True)
    # updated_at   = db.Column(db.DateTime,nullable=True)
    # location   = db.Column(db.String(255),nullable=True)

    
@app.route("/")
def login():
    session.clear()
    return render_template('login.html')
@app.route("/register")
def register():
    return render_template('register.html')    
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    my_cursor.execute("select * from departments") 
    departments =my_cursor.fetchall()

    if ('user' in session):
        return render_template('observation/add.html',departments = departments)
           
    if request.method == 'POST':
        username = request.form.get('username')
        upass = request.form.get('password')
        upass =hashlib.md5(upass.encode())
        upass =upass.hexdigest()
        query = "SELECT * FROM users where username=%s"    
        my_cursor.execute(query,(username,))        
        record = my_cursor.fetchone()
        if (upass == record[4] and username ==record[8]):
            session['user'] = username
            session['user_id'] = record[0]
            return render_template('observation/add.html',departments = departments)       
     
    return render_template('login.html',error = 'Invalid username and password!')    
@app.route("/observation")
def observation():
    if ('user' in session):
        return render_template('observation/list.html')

    return render_template('login.html') 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS          
@app.route("/addObservation",methods=['GET', 'POST'])
def addObservation():
     if (request.method =='POST'):
        category = request.form.get('category')
        priority = request.form.get('priority')
        target_date = request.form.get('target_date')
        location = request.form.get('location')
        department_id = request.form.get('department_id')
        user_id = request.form.get('responsibility')
        status = request.form.get('status')
        shift = request.form.get('shift')
        description = request.form.get('description')
        f= request.files['file']
        image=str(now.strftime("%Y%m%d_%H-%M-%S"))
        filename = secure_filename(f.filename)
        image = image+filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
        query ="INSERT INTO observations (category, priority, target_date, location, department_id, user_id, status, image, shift, description, created_by) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (category, priority, target_date, location, department_id, user_id, status, image, shift, description, session['user_id'])
        my_cursor.execute(query,val)
        conn.commit()        
        return render_template('observation/add.html', success = 'Observation added successfuly!')
     else:
        if('user' in session):
            return render_template('observation/add.html')
        return render_template('login.html')    


@app.route("/editObservation")
def editObservation():
    if ('user' in session):
        return render_template('observation/edit.html')
    return render_template('login.html') 
@app.route("/users")
def users():
    if ('user' in session):
        return render_template('users/list.html')
    return render_template('login.html') 
@app.route("/addUser")
def addUser():
    if ('user' in session):
        return render_template('users/add.html')
    return render_template('login.html') 
@app.route("/editUser")
def editUser():
    if ('user' in session):
        return render_template('users/edit.html')   
    return render_template('login.html')
@app.route("/departments")
def departments():
    if ('user' in session):
        return render_template('department/list.html')
   
    return render_template('login.html')
@app.route("/addDepartment")
def addDepartment():
    if ('user' in session):
        return render_template('department/add.html')
   
    return render_template('login.html')
@app.route("/editDepartment")
def editDepartment():
    if ('user' in session):
        return render_template('department/edit.html')
   
    return render_template('login.html')
@app.route("/departmentDetail")  
def departmentDetail():
    if ('user' in session):
        return render_template('department/detail.html')
   
    return render_template('login.html')
@app.route("/report")
def report():
    if ('user' in session):
        return render_template('report/list.html')
   
    return render_template('login.html')      
@app.route("/profile")
def profile():
    if ('user' in session):
        return render_template('profile.html')
   
    return render_template('login.html')                             
@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html',success = 'Logout successfuly!')
app.run(debug=True)
