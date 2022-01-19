import json
import sqlite3
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import all_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def create_dictionary(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'role': self.role,
            'phone': self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def create_dictionary(self):  # для записи в json
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'price': self.price,
            'customer_id': self.customer_id,
            'executor_id': self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def create_dictionary(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'executor_id': self.executor_id

        }


db.drop_all()
db.create_all()

for user_data in all_data.Users:
    new_user = User(
        id=user_data['id'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        age=user_data['age'],
        email=user_data['email'],
        role=user_data['role'],
        phone=user_data['phone']
    )
    db.session.add(new_user)
    db.session.commit()

for order_data in all_data.Orders:
    new_order = Order(
        id=order_data['id'],
        name=order_data['name'],
        description=order_data['description'],
        start_date=order_data['start_date'],
        end_date=order_data['end_date'],
        address=order_data['address'],
        price=order_data['price'],
        customer_id=order_data['customer_id'],
        executor_id=order_data['executor_id']
    )
    db.session.add(new_order)
    db.session.commit()

for offer_data in all_data.Offers:
    new_offer = Offer(
        id=offer_data['id'],
        order_id=offer_data['order_id'],
        executor_id=offer_data['executor_id']
    )
    db.session.add(new_offer)
    db.session.commit()

'''вывод всех пользователей'''
@app.route('/users', methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        result = []
        for one_user in User.query.all():
            result.append(one_user.create_dictionary())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == 'POST':
        user_data = json.load(request.data)
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            age=user_data['age'],
            email=user_data['email'],
            role=user_data['role'],
            phone=user_data['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return '', 201

'''вывод пользователя по id'''
@app.route('/user/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def user_id(id: int):
    if request.method == 'GET':
        return json.dumps(User.query.get(id).create_dictionary()), 200, {
            'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == 'DELETE':
        one_user = User.query.get(id)
        db.session.delete(one_user)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        one_user = User.query.get(id)
        one_user.first_name = user_data['first_name']
        one_user.age = user_data['age']
        one_user.email = user_data['email']
        one_user.role = user_data['role']
        one_user.phone = user_data['phone']
        db.session.delete(one_user)
        db.session.commit()
        return '', 204

'''вывод всех заказов'''
@app.route('/orders', methods=['GET', 'POST'])
def all_orders():
    if request.method == 'GET':
        result = []
        for one_order in Order.query.all():
            result.append(one_order.create_dictionary())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}

'''вывод заказa по id'''
@app.route('/order/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def order_id(id: int):
    if request.method == 'GET':
        return json.dumps(Order.query.get(id).create_dictionary()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == 'DELETE':
        one_order = Order.query.get(id)
        db.session.delete(one_order)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        one_order = Order.query.get(id)
        one_order.name = order_data['name']
        one_order.description = order_data['description']
        one_order.start_date = order_data['start_date']
        one_order.end_date = order_data['end_date']
        one_order.address = order_data['address']
        one_order.price = order_data['price']
        one_order.customer_id = order_data['customer_id']
        one_order.executor_id = order_data['executor_id']
        db.session.delete(one_order)
        db.session.commit()
        return '', 204

'''вывод всех предложений'''
@app.route('/offers', methods=['GET', 'POST'])
def all_offers():
    if request.method == 'GET':
        result = []
        for one_offer in Offer.query.all():
            result.append(one_offer.create_dictionary())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}

'''вывод предложения по id'''
@app.route('/offer/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def offer_id(id: int):
    if request.method == 'GET':
        return json.dumps(Offer.query.get(id).create_dictionary()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == 'DELETE':
        one_offer = Offer.query.get(id)
        db.session.delete(one_offer)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        one_offer = Offer.query.get(id)
        one_offer.order_id = offer_data['order_id']
        one_offer.executor_id = offer_data['executor_id']
        db.session.delete(one_offer)
        db.session.commit()
        return '', 204

app.run()
