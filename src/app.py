from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user 
from flask_mysqldb import MySQL
from models.modelUsers import ModelUsers
from models.entities.users import User
from config import config
app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

@app.route('/')
def root():
    return redirect("login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['username'], request.form['password'], 0)
        logged_user = ModelUsers.login(db, user)
        print("Logged User:", logged_user)  # Debug print
        if logged_user is not None:
            login_user(logged_user)
            return redirect(url_for("home"))
        else:
            flash('Acceso rechazado.', 'danger')
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")
    
@app.route('/home')
def home():
    return render_template("home.html")
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()