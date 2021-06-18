from datetime import datetime, timedelta
from datetime import date as _date

import requests as req
from sqlalchemy import extract
import pandas as pd
from database_management import Token, Offer
from app import db


def main()->dict:
	url= "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

	tokens=["USDT","BTC","BUSD","BNB","ETH","DAI"]
	data_tokens={}
	for token in tokens:
		data=[]
		for n in range(1,2):
			response = req.post(url=url, json={"page":n,"rows":10,"payTypes":[],"asset":token,"tradeType":"BUY","fiat":"ARS","publisherType":None,"merchantCheck":False,"transAmount":""})
			for node in response.json()["data"]:
				seller_params=node["advertiser"]
				token_params=node["adv"]
				methods=[]
				for transaction_method in token_params["tradeMethods"]:
					methods.append(transaction_method["identifier"])
				data.append({
					"user_name":seller_params["nickName"],
					"user_id":seller_params["userNo"],
					"finish_rate":seller_params["monthFinishRate"],
					"order_count":seller_params["monthOrderCount"],
					"methods": ", ".join(methods),
					"max_single_trans_amount":float(token_params["dynamicMaxSingleTransAmount"]),
					"min_single_trans_amount":float(token_params["minSingleTransAmount"]),
					"available":float(token_params["dynamicMaxSingleTransAmount"]),
					"price":float(token_params["price"]),
			
				})
		data_tokens[token]=data
	return data_tokens

def store_query_in_db():
	try:
		first_database_id= Offer.query.order_by(Offer.offer_id.desc()).first().offer_id
	except AttributeError:
		first_database_id=0
	print(first_database_id)
	new_values=[]
	data=main()
	for keys, values in data.items():
		db_id=Token.query.filter_by(name=keys).with_entities(Token.token_id).first()[0]
		for value in values:
			matching_values_in_db=Offer.query.filter(Offer.price == value["price"],
								Offer.user_name==value["user_name"],
								Offer.min_single_trans_amount == value["min_single_trans_amount"]
								)
			if matching_values_in_db.count():
				offers_from_today=matching_values_in_db.filter(
                			extract('year', Offer.date) == _date.today().year,
                			extract('month', Offer.date) == _date.today().month,
               				 extract('day', Offer.date) == _date.today().day)
				if offers_from_today.count() == 0:
					offer=Offer(**value, token_id=db_id)
					db.session.add(offer)
					new_values.append(offer)
					print("wrote an offer, {}, alternative path".format(offer.user_name))
				else:
					for updated_offer in offers_from_today.all():
						updated_offer.datetime=datetime.now()
						db.session.add(updated_offer)
						print("Updated values for offer by = {}".format(updated_offer.user_name))
			else:
				offer= Offer(**value,token_id= db_id)
				db.session.add(offer)
				new_values.append(offer)
				print('wrote an offer, {} of token {} '.format(offer.user_name, Token.query.with_entities(Token.name).filter_by(token_id=offer.token_id).first()[0]))
		db.session.commit()
	try:
		last_database_id= offer.offer_id
	except UnboundLocalError:
		print('No escribí datos nuevos')
		last_database_id=first_database_id
	print(last_database_id)

	return Offer.query.filter(Offer.offer_id > first_database_id).filter(Offer.offer_id <= last_database_id)




def consulta():
  data=main()
  lista=[]
  for k,v in data.items():
    nodo = v[v.price==v.price.min()].copy()
    nodo["token"]=k
    lista.append(nodo)
  return pd.concat(lista, axis=0)



if __name__=="__main__":
	q=store_query_in_db()