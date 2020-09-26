from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
import os

def shorten_link(headers, url):
	response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=url)
	shorten_link = response.json()
	return shorten_link["link"]

def count_clicks(headers, url):
	url_urlparse = urlparse(url).path

	response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/bit.ly{}/clicks/summary'.format(url_urlparse),
	 headers=headers)
	clicks_count = response.json()
	return clicks_count["total_clicks"]

if __name__ == '__main__':
	url = input("Ссылка : ")

	load_dotenv()
	token = os.getenv("TOKEN")
	headers = {
	    'Authorization': 'Bearer ' + str(token)
	}
	data = { "long_url": url}


	if url.startswith("bit.ly", 8, 14):
		try:
			count_clicks = count_clicks(headers,url)
			print("Количество кликов : " + str(count_clicks))
		except LookupError:
			print("Ошибка, введите ссылку повторно")
	else :		
		try:
			bitlink = shorten_link(headers,data)
			print('Битлинк : ' + bitlink)
		except LookupError:
			print("Ошибка, введите ссылку повторно")