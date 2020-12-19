import os
import json
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(headers, link):
    data = {"long_url": link}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=data)
    response.raise_for_status()

    short_link = response.json()
    return short_link["link"]


def get_count_clicks(headers, full_bitlink):
    bitlink = f"{urlparse(full_bitlink).netloc}{urlparse(full_bitlink).path}"
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}\
        /clicks/summary',
        headers=headers)
    response.raise_for_status()
    clicks_count = response.json()
    return clicks_count["total_clicks"]


def main():
    link = input("Ссылка : ")

    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        counted_clicks = (get_count_clicks(headers, link))
        print(f"Количество кликов : {counted_clicks}")
    except json.decoder.JSONDecodeError:
        bitlink = shorten_link(headers, link)
        print(f'Битлинк : {bitlink}')
    except requests.exceptions.HTTPError as error:
        print(f"Ошибка на сервере : \n{error}")


if __name__ == '__main__':
    main()
