import os
from gettext import install
from idlelib.multicall import r

import pip
import requests
import dotenv
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv
from pip._internal.resolution.resolvelib import requirements





def shorten_link(token, url):
    body = {
        "long_url": url,
    }
    parameters = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.post(
        "https://api-ssl.bitly.com/v4/bitlinks",
        headers=parameters,
        json=body
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, url):
    parameters = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary",
        headers=parameters
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, token):
    parameters = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary",
        headers=parameters
    )
    return response.ok

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='Shortens links')
    parser.add_argument('--url', help='Введите ссылку')
    args = parser.parse_args()
    url = args.url
    token = os.environ["SECRET_BITLY_TOKEN"]
    parsed_url = urlparse(url)
    url_without_scheme = f"{parsed_url.netloc}{parsed_url.path}"
    if is_bitlink(url_without_scheme, token):
        try:
            print("amount of clicks:", count_clicks(token, url_without_scheme))
        except requests.exceptions.HTTPError:
            print("click counting error")
    else:
        try:
            print("your shortend link:", shorten_link(token, url))
        except requests.exceptions.HTTPError:
            print("link shortening error")
