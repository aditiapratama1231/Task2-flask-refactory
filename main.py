from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db_user_flask.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.Text)
    phone = db.Column(db.String(13))

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users = users)

@app.route("/user/create", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    else:
        name = request.form["name"]
        address = request.form["address"]
        phone = request.form["phone"]

        user = User(name = name, address = address, phone = phone)

        db.session.add(user)
        db.session.commit()

        return redirect("/")

@app.route("/user/update/<id>", methods=["GET", "POST"])
def update_user(id):
    if request.method == "GET":
        user = User.query.filter_by(id = id).first()
        return render_template("update_user.html", user = user)
    else:
        name = request.form["name"]
        address = request.form["address"]
        phone = request.form["phone"]

        user = db.session.query(User)
        user = user.filter_by(id = id)
        req = user.one()
        req.name = name
        req.address = address
        req.phone = phone
        db.session.flush()
        db.session.commit()

        return redirect("/")

@app.route("/user/delete/<id>")
def delete_user(id):
    User.query.filter_by(id = id).delete()
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
