#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc


from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    
    bakeries = Bakery.query.all()
    if bakeries:
        bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
        response = make_response(jsonify(bakeries_serialized), 200)
    else: 
        response = make_response(jsonify(bakeries=[]), 200)
    response.headers['Content-Type'] = 'application/json'


    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):    
    
    bakery = Bakery.query.filter_by(id = id).first()
    if bakery:
        response = make_response(jsonify(bakery.to_dict()), 200)
    else:
        response = make_response(f'Bakery {id} not found', 404)

    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():

    goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    goods_serialized = [good.to_dict() for good in goods]

    response = make_response(jsonify(goods_serialized), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    
    goods = BakedGood.query.order_by(desc(BakedGood.price)).first()
    goods_serialized = goods.to_dict() 
    response = make_response(jsonify(goods_serialized), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
