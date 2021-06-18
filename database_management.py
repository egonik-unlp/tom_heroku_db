# from typing import OrderedDict
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import backref
from datetime import datetime
from datetime import date as _date
from app import db



class Token(db.Model):
	__tablename__="token"
	token_id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String)
	offers=db.relationship("Offer", backref="token")
	token_values_usd=db.relationship("Token_Value_Usd", backref="token")
	def __init__(self,name):
		self.name=name
class Offer(db.Model):
	__tablename__="offer"
	offer_id=db.Column(db.Integer, nullable=False, primary_key=True )
	price=db.Column(db.Float, nullable=False)
	date=db.Column(db.DateTime, nullable=False)
	datetime=db.Column(db.DateTime, nullable=False)
	token_id=db.Column(db.Integer, db.ForeignKey("token.token_id"), nullable=False)
	user_name=db.Column(db.String, nullable=False)
	user_id=db.Column(db.String, nullable=False)
	finish_rate=db.Column(db.Float, nullable=False)
	order_count=db.Column(db.Integer, nullable=False)
	methods=db.Column(db.String(256), nullable=False)
	max_single_trans_amount=db.Column(db.Float, nullable=False)
	min_single_trans_amount=db.Column(db.Float, nullable=False)
	available=db.Column(db.Float, nullable=False)

	def __init__(self, price, token_id,user_name,
	 		max_single_trans_amount, min_single_trans_amount, user_id, methods,
			 finish_rate, order_count, available):
		self.price=price
		self.date=_date.today()
		self.datetime=datetime.now()
		self.token_id=token_id
		self.user_name=user_name
		self.user_id=user_id
		self.max_single_trans_amount=max_single_trans_amount
		self.min_single_trans_amount=min_single_trans_amount
		self.order_count=order_count
		self.methods=methods
		self.finish_rate=finish_rate
		self.available=available


class Token_Value_Usd(db.Model):
	__tablename__="token_value_usd"
	value_id=db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
	date=db.Column(db.DateTime, nullable=False)
	value_usd=db.Column(db.Float, nullable=True)
	token_id=db.Column(db.Integer, db.ForeignKey("token.token_id"), nullable=False)
	def __init__(self, value_usd, token_id):
		self.date=datetime.now()
		self.value_usd=value_usd
		self.token_id=token_id




db.create_all()