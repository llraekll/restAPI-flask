from crypt import methods
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def welcome_page():
    return "Hello human"


@app.route('/cars')
def get_data():
    cars = Cars.query.all()

    output = []
    for car in cars:
        car_data = {'name': car.name, 'description': car.description}

        output.append(car_data)
   # return ('rakshiths data')
    return {'data': output}


@app.route('/cars/<id>')
def get_cars(id):
    car = Cars.query.get_or_404(id)
    return jsonify({"name": car.name, "description": car.description})


@app.route('/cars', methods=['POST'])
def add_car():
    cars = Cars(name=request.json['name'],
                description=request.json['description'])
    db.session.add(cars)
    db.session.commit()
    return {'id': cars.id}

@app.route('/cars/<id>', methods=['DELETE'])
def delete_car(id):
    car=Cars.query.get(id)
    if car is None:
        return{"error": "not found"}

    db.session.delete(car)
    db.session.commit()
    return {"message": "deleted car successfully"}


