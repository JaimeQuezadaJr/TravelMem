from fileinput import filename
from flask_app import ALLOWED_EXTENSIONS, app
from flask import render_template, redirect, request, session, flash
from flask_app.controllers.memories import allowed_file
from flask_app.models import user, memory
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/user/edit/<int:id>')
def edit_user_page(id):
    data = {
            "id":id,
    }
    return render_template('edit_profile.html', user = user.User.get_user_by_id(data))

@app.route('/register_page')
def register_page():
    return render_template('register.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/register', methods = ['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/register_page')
    if 'profile_pic' not in request.files:
        flash('No file part in form', 'register')
        return redirect("/register_page")
    file = request.files['profile_pic']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No file uploaded', 'register')
        return redirect("/register_page")
    # If invalid file type
    if not allowed_file(file.filename):
        flash("File type is incorrect. Only .png, .jpg, .jpeg, .gif files allowed", 'register')
        return redirect("/register_page")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(os.path.join(app.root_path,'static','images', filename))
        # Save the file itself in the /static/images folder
        file.save(os.path.join(app.root_path,'static','images', filename)) 
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "city": request.form['city'],
            "state": request.form['state'],
            "email": request.form['email'],
            "password": pw_hash,
            "profile_pic": filename
        }
        user_id = user.User.save_user(data)
        session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/update_profile/<int:id>', methods = ['POST'])
def update_profile(id):
    if not user.User.validate_edit_user(request.form):
        return redirect(f'/user/edit/{id}')
    if 'profile_pic' not in request.files:
        flash('No file part in form.', 'update')
        return redirect(f"/user/edit/{id}")
    file = request.files['profile_pic']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No file uploaded.', 'update')
        return redirect(f"/user/edit/{id}")
    # If invalid file type
    if not allowed_file(file.filename):
        flash("File type is incorrect.", 'update')
        return redirect(f"/user/edit/{id}")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(os.path.join(app.root_path,'static','images', filename))
        # Save the file itself in the /static/images folder
        file.save(os.path.join(app.root_path,'static','images', filename)) 
    data = {
            "id": id,
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "city": request.form['city'],
            "state": request.form['state'],
            "profile_pic": filename
        }
    user.User.edit_user(data)
    return redirect("/dashboard")

@app.route('/login', methods = ['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect('/login_page')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/login_page')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard(): 
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        return render_template('dashboard.html', user = user.User.get_user_by_id(data), memories = memory.Memory.get_all_memories_with_users(), all_users = user.User.get_all_users())
    else:
        flash("Must login!", "login")
        return redirect('/')

@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        return render_template('profile.html', user = user.User.get_user_by_id(data), memories = memory.Memory.get_all_memories_with_users(), all_users = user.User.get_all_users())
    else:
        flash("Must login!", "login")
        return redirect('/')

@app.route('/delete/user/<int:id>')
def delete_user(id):
    data = {
        'id':id
    }
    user.User.delete_user(data)
    return redirect('/logout')