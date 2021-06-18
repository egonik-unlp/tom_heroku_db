from database_management import  Offer, Token_Value_Usd, Token
from app import db
import requests as req
import dotenv
import os


dotenv.load_dotenv()


def get_rates(token):
	url = 'https://rest.coinapi.io/v1/exchangerate/{}/USD'.format(token)
	headers = {'X-CoinAPI-Key' : os.getenv('COINAPI_KEY')}
	return req.get(url, headers=headers)


def main():
	list=[]
	for id, token in Token.query.with_entities(Token.token_id, Token.name).all():
		rate=get_rates(token).json()['rate']
		token_value=Token_Value_Usd(value_usd=rate, token_id=id)
		db.session.add(token_value)
	db.session.commit()
	


if __name__=="__main__":
	main()