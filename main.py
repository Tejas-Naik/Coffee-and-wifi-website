from logging import setLoggerClass
from types import MethodDescriptorType
from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(50), nullable=True)
    has_sockets = db.Column(db.Integer, nullable=True)
    has_toilet = db.Column(db.Integer, nullable=True)
    has_wifi = db.Column(db.Integer, nullable=True)
    can_take_calls = db.Column(db.Integer, nullable=True)
    seats = db.Column(db.Integer, nullable=True)
    coffee_price = db.Column(db.Float, nullable=False)
db.create_all()

@app.route('/')
def home():
    # all_movies = Cafe.query.order_by(Cafe.name).all()
    all_movies = Cafe.query.order_by(Cafe.name).all()
    return render_template('index.html', cafes=all_movies)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_cafe = Cafe(
                name=request.form['xname'],
                map_url=request.form['map_url'],
                img_url=request.form['img_url'],
                location=request.form['location'],
                has_sockets=request.form['sockets'],
                has_toilet=request.form['toilets'],
                has_wifi=request.form['wifi'],
                can_take_calls=request.form['calls'],
                seats=request.form['seats'],
                coffee_price=request.form['cost'],
            )
        db.session.add(new_cafe)
        db.session.commit()

    return render_template('add.html')

@app.route("/delete")
def delete_cafe():
    cafe_id = request.args.get("id")
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(port=5000,debug=True)