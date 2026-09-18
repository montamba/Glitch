from flask import Flask, render_template,request, session, redirect,url_for
from flask_mysqldb import MySQL
import os

import qr

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "final"
app.secret_key = "secret"



sql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html", password = "")

@app.route("/authen", methods=["POST"])
def auth():
    cur = sql.connection.cursor()
    
    name = request.form.get("name")
    password = request.form.get('pass')
    if "signin" in request.form:
        cpassword = request.form.get("cpass")
        
        if cpassword != password:
            return render_template("index.html", password = "password not match")
        
        pt = qr.generate(name, name + "hatdog.png")
        cur.execute(f"INSERT INTO users (name, password,qr) VALUES ('{name}', '{password}', '{pt}')")
        sql.connection.commit()
        return render_template("index.html", password = "sign up success")
    
    if "login" in request.form:
        cur.execute(f"SELECT * FROM users WHERE name = '{name}' AND password = '{password}'")
        data = cur.fetchone()
        try:
            if data[1] == name and data[2] == password:
                session["user"] = name
                session["id"] = data[0]
                
                return redirect(url_for("home"))
            
            else:
                return render_template("index.html", password = "User not found")
        except IndexError:
            return render_template("index.html", password = "User not found")
        
@app.route("/postvid", methods=["POST"])     
def postvid():
    cur = sql.connection.cursor()
    
    imagepath = "static/img/movie_pic/"
    vidpath = "static/vid/"
    
    user = session.get("user")
    image = request.files.get("imagesrc")
    videow = request.files.get("move")
    title = request.form.get("title")
    des = request.form.get("des")
    genre = request.form.get("gen")
    cur = sql.connection.cursor()
        
        
    cur.execute(f"SELECT * FROM users WHERE id = '{session['id']}'")
    
    
    if image.filename == '' and videow.filename == '':
        
        return render_template("post.html",data=cur.fetchone(), hmmm = "Please upload a video and image")
    
    imageup = os.path.join(imagepath, image.filename)
    videoup = os.path.join(vidpath, videow.filename)
    
    image.save(imageup)
    videow.save(videoup)
    cur.execute(f"INSERT INTO movies(image, video, title, description, genre, postedby) VALUES ('{imageup}', '{videoup}', '{title}', '{des}','{genre}','{user}')")
    sql.connection.commit()
    cur = sql.connection.cursor()
        
        
    cur.execute(f"SELECT * FROM users WHERE id = '{session['id']}'")
        
    
    return render_template('post.html',data=cur.fetchone(), hmmm="upload finish")
    
    
        
@app.route("/home")
def home():
    cur = sql.connection.cursor()
    if "user" in session:
        cur.execute(f"SELECT * FROM users WHERE id = '{session['id']}'")
        data = cur.fetchone()
        return render_template("home.html", data = data)
    return render_template("error.html")
    
        

@app.route("/watch" , methods=["POST"])
def watch():
    data = request.form.get("mid")
    id = int(data)
    cur = sql.connection.cursor()
    cur.execute(f"SELECT * FROM movies WHERE id = '{id}'")
    data2 = cur.fetchone()
    
    cur.execute(f"SELECT * FROM movies")
    d = cur.fetchall()
    
    if data2 == None:
            return render_template("error.html")

    return render_template("video.html", mv=data2, dd=d) if len(data2) > 0 else render_template("error.html")
    
@app.route("/movies")
def movies():
    cur = sql.connection.cursor()
    
    if "user" in session:
        cur.execute(f"SELECT * FROM users WHERE id = '{session['id']}'")
        profile = cur.fetchone()
        cur.execute("SELECT * FROM movies")
        return render_template("movies.html", data = cur.fetchall(), profile = profile)
    return render_template("error.html")
    
        

@app.route("/post")  
def post():
    
    if "user" in session:
        cur = sql.connection.cursor()
        
        
        cur.execute(f"SELECT * FROM users WHERE id = '{session['id']}'")
        
        return render_template("post.html",data=cur.fetchone(), hmmm="")
    return render_template("error.html")
    
    

@app.route("/profile")
def profile():
    if "user" in session:
        cur = sql.connection.cursor()
        cur.execute(f"SELECT * FROM users WHERE id = '{session['id']}'")
        return render_template("profile.html", profile = cur.fetchone())
    return render_template("error.html")
    

@app.route("/updateprofile", methods=["POST"])
def update():
    cur = sql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE id ='{session["id"]}'")
    data = cur.fetchone()
    if "user" in session:
        name = request.form.get("name")
        password = request.form.get("pass")
        profilepic = request.files.get("profile")
        
        propath = "static/img/profile/"
        
        if name != data[1]:
            nigga = qr.generate(name, name+"woohoo.png")
        else: nigga = data[4]
        
        try: 
            pathy = os.path.join(propath, profilepic.filename)
            profilepic.save(pathy)
        except:
            pathy = data[3]
        
        cur.execute(f"UPDATE users SET name='{name}',password='{password}',profilepic='{pathy}',qr='{nigga}' WHERE id='{session["id"]}'")
        sql.connection.commit()
        return redirect(url_for("profile"))
    return render_template("error.html")
    
        
    
@app.route("/about")
def about():
    if "user" in session:
        cur = sql.connection.cursor()
        cur.execute(f"SELECT * FROM users WHERE id = '{session['id']}'")
        return render_template("about.html", profile=cur.fetchone())
    return render_template("error.html")
    
    
@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template("index.html")


    
    
if __name__ == "__main__":
    app.run(debug=True)
    
