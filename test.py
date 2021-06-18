from dotenv import load_dotenv
import os

load_dotenv()
def main():
	data1= os.getenv('CHAT_ID')
	data2= os.getenv('API_KEY')
	return 'chat->{} api->{}'.format(data1, data2)