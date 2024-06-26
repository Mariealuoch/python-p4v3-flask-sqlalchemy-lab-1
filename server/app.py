from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Routes
@app.route('/')
def index():
    return make_response({'message': 'Flask SQLAlchemy Lab 1'}, 200)

@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        return make_response(earthquake.to_dict(), 200)
    else:
        return make_response({'message': f'Earthquake {id} not found.'}, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    # Query earthquakes with magnitude greater than or equal to the given parameter
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    if earthquakes:
        quakes_data = [quake.to_dict() for quake in earthquakes]
        response_body = {
            'count': len(quakes_data),
            'quakes': quakes_data
        }
        status = 200
    else:
        response_body = {
            'count': 0,
            'quakes': []
        }
        status = 200  # Returning 200 as per the example

    return make_response(jsonify(response_body), status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
