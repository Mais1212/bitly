from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
import os


def shorten_link(headers, link):
    data = {"long_url": link}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=data)

    short_link = response.json()
    print(short_link)
    return short_link["link"]


def count_clicks(headers, long_link):
    url_urlparse = urlparse(long_link).path
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url_urlparse}\
        /clicks/summary',
        headers=headers)
    print(url_urlparse)
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
        try:
            counted_clicks = (count_clicks(headers, link))
            print("Количество кликов : " + str(counted_clicks))
        except KeyError:
            bitlink = shorten_link(headers, link)
            print('Битлинк : ' + bitlink)
    except:
        print("Введите ссылку повторно!")
        main()


if __name__ == '__main__':
    main()
