import getter , notification
import pandas as pd
import numpy as np
import requests as req
from sqlalchemy import desc, asc
from app import db
from database_management import Token_Value_Usd, Offer, Token
from getter import store_query_in_db

# data=getter.main()

def filter_db(params):
	selected_offers=[]
	new_entries=store_query_in_db()
	for param in params:
		_token_id=Token.query.filter_by(name=param["token"]).first().token_id
		if param['token']=='USDT':
			usdt_token=_token_id
			usdt_offers = new_entries.filter(Offer.token_id ==_token_id).\
					filter(Offer.price < param["price"]).\
					filter(Offer.max_single_trans_amount >= param['target']).\
					filter(Offer.min_single_trans_amount <= param['target']).\
					filter(Offer.finish_rate >= param['finish_rate']).\
					filter(Offer.order_count >= param["order_count"]).\
					order_by(desc(Offer.price)).all()
			selected_offers += usdt_offers 
				
			print('Ofertas para usdt {} '.format(usdt_offers))
		else:
			
			other_offers = new_entries.filter(Offer.token_id==_token_id).filter(
					Offer.price < param["price"]).filter(
					Offer.max_single_trans_amount >= param['target']).filter(
					Offer.min_single_trans_amount <= param['target']).filter(
					Offer.finish_rate <= param['finish_rate']).filter(
					Offer.order_count >= param["order_count"]
			).order_by(desc(Offer.price)).all()
			selected_offers += other_offers


		
		print(selected_offers)
	
	if usdt_offers:
		best_usdt_offer=usdt_offers[-1]
		for offer in new_entries.filter(Offer.token_id != usdt_token).all():
			current_price_in_usd=Token_Value_Usd.query.order_by(desc(Token_Value_Usd.date)).filter_by(token_id=offer.token_id).first().value_usd
			token_name=Token.query.filter(Token.token_id==offer.token_id).first().name
			if offer.price/current_price_in_usd < best_usdt_offer.price:
				print("Precio en dolares cociente falopa {} para {}, precio usdt {}".format(offer.price/current_price_in_usd, token_name,best_usdt_offer.price))
				selected_offers.append(offer)

	else:
		pass
	if selected_offers:
		r=notification.from_db(selected_offers)
		print('message sent')
	else:
		print('no message sent')
	
	# return selected_offers


			
			


		

	


def get_params():
	params=[
				{
					'token':'USDT',
					'price':161,
					'target':40000,
					'finish_rate':.80,
					'order_count':20
				},
		
			]

	return params


	
if __name__=='__main__':
	# main()
	a=filter_db(params=get_params())