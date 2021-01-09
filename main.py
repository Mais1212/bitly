import os
import json
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "link",
        type=str,
        help="Введите ссылку или битлинк",
    )
    return parser


# def check_bitlink(bitlink, headers):
#     bitlink = f"{urlparse(bitlink).netloc}{urlparse(bitlink).path}"

#     response = requests.get(
#         f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}", headers=headers)
#     response.raise_for_status()
#     print(response.text)


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
    parser = create_parser()
    args = parser.parse_args()

    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # try:
    #     bitlink_info = check_bitlink(args.link, headers)
    #     print(bitlink_info)
    # except requests.exceptions.HTTPError:
    #     try:
    #         bitlink = shorten_link(headers, args.link)
    #         print(f'Битлинк : {bitlink}')
    #     except requests.exceptions.HTTPError:
    #         print("Ссылка какая-то 'Странная', попробуйте ввести другую")

    try:
        counted_clicks = get_count_clicks(headers, args.link)
        print(f"Количество кликов : {counted_clicks}")
    except requests.exceptions.HTTPError:
        try:
            bitlink = shorten_link(headers, args.link)
            print(f'Битлинк : {bitlink}')
        except requests.exceptions.HTTPError as error:
            print(args.link)
            print(f"Ошибка на сервере : \n{error}")


if __name__ == '__main__':
    main()
