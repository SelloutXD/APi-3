import os
import argparse
from urllib.parse import urlparse

from dotenv import load_dotenv
import requests


def shorten_link(headers, url):
    body = {
        "long_url": url,
    }
    response = requests.post(
        "https://api-ssl.bitly.com/v4/bitlinks",
        headers=headers,
        json=body
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(headers, url):
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary",
        headers=headers
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, headers):
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary",
        headers=headers
    )
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='Shortens links')
    parser.add_argument('--url', help='Введите ссылку')
    args = parser.parse_args()
    url = args.url
    token = os.environ["SECRET_BITLY_TOKEN"]
    headers = {
        "Authorization": f"Bearer {token}",
    }
    parsed_url = urlparse(url)
    url_without_scheme = f"{parsed_url.netloc}{parsed_url.path}"
    if is_bitlink(url_without_scheme, headers):
        try:
            print("amount of clicks:", count_clicks(headers, url_without_scheme))
        except requests.exceptions.HTTPError:
            print("click counting error")
    else:
        try:
            print("your shortend link:", shorten_link(headers, url))
        except requests.exceptions.HTTPError:
            print("link shortening error")
