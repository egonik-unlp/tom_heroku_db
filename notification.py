from numpy import load
from dotenv import load_dotenv
import requests as req
from database_management import Offer, Token, Token_Value_Usd
from app import db
import pandas as pd
import os

load_dotenv()


def test(text="Estoy andando pedazo de tontolin"):
	token = os.getenv("API_KEY")
	urlp = f"https://api.telegram.org/bot{token}"
	params = {"chat_id": os.getenv("CHAT_ID"), 
          "text":text}
	r = req.get(urlp + "/sendMessage", params=params)
	return r.json()






def main(data):
	tablita=data
	print(tablita)
	token = os.getenv("API_KEY")
	for chat_id in (os.getenv("CHAT_ID"), os.getenv("CHAT_ID1")):
		urlp = f"https://api.telegram.org/bot{token}"
		try:
			package="\n\n".join(["\n".join([f"{x} = {str(z)}" for x,z in v.iteritems()]) for k,v in tablita.iterrows()])
		except AttributeError:
			package="\n".join([f"{x} = {str(z)}" for x,z in tablita.iteritems()])
		params = {"chat_id": os.getenv("CHAT_ID"), 
		"text":package}

		r = req.get(urlp + "/sendMessage", params=params)
	return r

def from_db(selected_offers):
	text=''
	api_key=os.getenv("API_KEY")
	
	for offer in selected_offers:
		text+='Token = {}\n'.format(Token.query.filter(Token.token_id==offer.token_id).first().name)
		text+='Price = {}\n'.format(offer.price)
		text+='User Name = {}\n'.format(offer.user_name)
		text+='\n'
	urlp = f"https://api.telegram.org/bot{api_key}"
	params = {"chat_id": os.getenv("CHAT_ID"), 
		"text":text}

	r = req.get(urlp + "/sendMessage", params=params)
	return r
