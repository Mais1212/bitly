from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
import os


def shorten_link(headers, link):
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=link)

    short_link = response.json()
    return short_link["link"]


def count_clicks(headers, long_link):
    url_urlparse = urlparse(long_link).path

    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/bit.ly{}/clicks/summary'.format(
            url_urlparse),
        headers=headers)
    clicks_count = response.json()
    return clicks_count["total_clicks"]


if __name__ == '__main__':
    link = input("Ссылка : ")

    load_dotenv()
    token = os.getenv("TOKEN")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    long_link = {"long_url": link}

    if link.startswith("bit.ly", 8, 14):
        try:
            count_clicks = count_clicks(headers, link)
            print("Количество кликов : " + str(count_clicks))
        except LookupError:
            print("Ошибка, введите ссылку повторно")
    else:
        try:
            bitlink = shorten_link(headers, long_link)
            print('Битлинк : ' + bitlink)
        except LookupError:
            print("Ошибка, введите ссылку повторно")
