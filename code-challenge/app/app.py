from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Power, Hero, HeroPower

def create_app():
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app = create_app()
migrate = Migrate(app, db)

@app.route('/')
def home():
    return ''

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
    return jsonify(hero_data)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)

if hero is None:
    return jsonify({"error": "Hero not found"}), 404

hero_powers = HeroPower.query.filter_by(hero_id=hero.id).all()

powers = [
    {
        "id": hero_power.id,
        "strength": hero_power.strength,
        "name": hero_power.power.name,
        "description": hero_power.power.description
    }
    for hero_power in hero_powers
]

hero_data = {
    "id": hero.id,
    "name": hero.name,
    "super_name": hero.super_name,
    "powers": powers
}

return jsonify(hero_data)
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(power_data)

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)

if power is None:
    return jsonify({"error": "Power not found"}), 404

power_data = {
    "id": power.id,
    "name": power.name,
    "description": power.description
}

return jsonify(power_data)
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)

if power is None:
    return jsonify({"error": "Power not found"}), 404

try:
    data = request.get_json()
    power.description = data.get('description', power.description)


    db.session.commit()

    updated_power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }

    return jsonify(updated_power_data)

except Exception as e:
    db.session.rollback()
    return jsonify({"errors": [str(e)]}), 400
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.json
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

    # check if the fields are present
    if not strength or not power_id or not hero_id:
        raise ValueError('Missing required fields')

   
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        raise ValueError('Hero or Power not found')

    # Create a new HeroPower
    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    db.session.add(hero_power)
    db.session.commit()

    # Fetch the hero data 
    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [
            {"id": p.id, "name": p.name, "description": p.description}
            for p in hero.powers
        ],
    }

    return jsonify(hero_data), 201  

except ValueError as e:
    return jsonify({"errors": [str(e)]}), 400 
if name == 'main':
    app.run(port=5555)