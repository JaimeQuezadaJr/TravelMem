from fileinput import filename
from re import T
from flask_app import ALLOWED_EXTENSIONS, app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import memory, user
import json
import os
import requests
from datetime import datetime
from datetime import timedelta
import time
from werkzeug.utils import secure_filename

@app.route('/memory/new')
def new_memory():
    return render_template('create_memory.html')

@app.route('/memory/edit/<int:id>')
def edit_memory_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            "id":id,
    }
    return render_template('edit_memory.html', this_memory = memory.Memory.get_memory_by_id(data))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update_memory/<int:id>', methods = ['POST'])
def edit_memory(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not memory.Memory.validate_memory(request.form):
        return redirect(f'/memory/edit/{id}')
    if 'img_name' not in request.files:
        flash('No file part in form.', 'memory')
        return redirect(f"/memory/edit/{id}")
    file = request.files['img_name']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No file uploaded.', 'memory')
        return redirect(f"/memory/edit/{id}")
    # If invalid file type
    if not allowed_file(file.filename):
        flash("File type is incorrect. Only .png, .jpg, .jpeg, .gif files allowed", 'memory')
        return redirect(f"/memory/edit/{id}")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(os.path.join(app.root_path,'static','images', filename))
        # Save the file itself in the /static/images folder
        file.save(os.path.join(app.root_path,'static','images', filename))
    data = {
            "id":id,
            "location": request.form['location'],
            "country": request.form['country'],
            "date": request.form['date'],
            "description" : request.form['description'],
            "img_name" : filename,
            "user_id" : session['user_id']
    }
    memory.Memory.edit_memory(data)
    return redirect('/dashboard')



@app.route('/create_memory', methods = ['POST'])
def save_memory():
    if 'user_id' not in session:
        return redirect('/logout')
    if not memory.Memory.validate_memory(request.form):
        return redirect('/memory/new')
    if 'img_name' not in request.files:
        flash('No file part in form.', 'memory')
        return redirect("/memory/new")
    file = request.files['img_name']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No file uploaded.', 'memory')
        return redirect("/memory/new")
    # If invalid file type
    if not allowed_file(file.filename):
        flash("File type is incorrect.", 'memory')
        return redirect("/memory/new")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(os.path.join(app.root_path,'static','images', filename))
        # Save the file itself in the /static/images folder
        file.save(os.path.join(app.root_path,'static','images', filename))
        data = {
            "location": request.form['location'],
            "country": request.form['country'],
            "date": request.form['date'],
            "description" : request.form['description'],
            "img_name" : filename,
            "user_id" : session['user_id']
        } 
        memory.Memory.save_memory(data)
    
            
    return redirect('/dashboard')


 
@app.route('/delete/<int:id>')
def delete_memory(id):
    data = {
        'id':id
    }
    memory.Memory.delete_memory(data)
    return redirect('/dashboard')

@app.route('/weather/<place>')
def grab_weather(place):
    user_data = {
        'id': session['user_id']
    }
    print(place)
    location = place
    api_key = os.environ.get("WEATHER_API_KEY")
    # print(f"http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={api_key}")
    raw_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={api_key}")
    print(raw_data.json())
    data = raw_data.json()
    print(data['weather'])

    weather_data = data['weather']
    main_data = data['main']
    wind_data = data['wind']
    time_zone = data['timezone']

    climate = weather_data[0]['description']
    temp = round((9/5) * ((main_data['temp']) -273) + 32)
    feels_like = round((9/5) * ((main_data['feels_like']) - 273) + 32)
    min_temp = round((9/5) * ((main_data['temp_min']) - 273) + 32)
    max_temp = round((9/5) * ((main_data['temp_max']) - 273) + 32)
    humidity = main_data['humidity']
    wind = round((wind_data['speed']) * 2.236936)

    time = ((datetime.utcnow() + timedelta(seconds=time_zone)).strftime(" %I:%M%p\n %A\n %B %d"))



    return render_template( "weather.html", location=location, user_data=user_data, climate=climate, temp=temp, feels_like=feels_like, min_temp=min_temp, max_temp=max_temp, humidity=humidity, wind=wind, time=time )
     

@app.route('/memory/<int:id>')
def memory_info(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':id,
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('view_memory.html', this_memory = memory.Memory.get_memory_by_user(data), user = user.User.get_user_by_id(user_data), all_memories = user.User.grab_one_user_with_all_memories(data))

