import bs4
import requests
import smtplib
import json
import time
from config import *

URL_DICT = {
    'https://thepihut.com/products/raspberry-pi-4-model-b': {'4B (1Gb)': '41005997392067',
                                                             '4B (2Gb)': '20064052674622',
                                                             '4B (4Gb)': '20064052740158',
                                                             '4B (8Gb)': '31994565689406'},
    'https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-3-model-a-plus': {'3B': '13584708763710'},
    'https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-3-model-b-plus': {'3A': '18157318733886'},
    'https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-pico': {'Pico': '37979757412547'}}

SELECTOR = '''#shopify-section-product-template > section > div.container.container--flush > 
              div.product-block-list.product-block-list--medium > div > 
              div.product-block-list__item.product-block-list__item--info > div > script'''

saved_dict = {}
status_dict = {}
x = 0


def get_saved():
    for url in URL_DICT:

        inventories = get_inventories(url)
        for item in URL_DICT[url]:
            num = URL_DICT[url][item]
            msg = inventories[num]['inventory_message']
            saved_dict[item] = msg

    return saved_dict


def get_inventories(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    element = soup.select(SELECTOR)
    data = json.loads(element[0].text)
    inventories = (data['inventories'])
    return inventories


def send_email(item, status, url):
    conn = smtplib.SMTP(host, port, timeout=120)
    conn.ehlo()
    conn.starttls()
    conn.login(sender_email, sender_pass)

    conn.sendmail(sender_email, receiver_email,
                  f'Subject: PiHut Stock Change\n\n'
                  f'The stock status of the Raspberry Pi {item} has changed to \'{status}\' at this link:'
                  f'\n\n{url}')

    conn.quit()


def main():
    global saved_dict, x
    for url in URL_DICT:
        inventories = get_inventories(url)

        for item in URL_DICT[url]:
            num = URL_DICT[url][item]
            msg = inventories[num]['inventory_message']
            status_dict[item] = msg

            if status_dict[item] != saved_dict[item]:
                email = f'{item}: {status_dict[item]}: {url}'
                print(email)
                send_email(item, status_dict[item], url)
                saved_dict = status_dict
            else:
                pass

    x += 1
    print(f'Status checked {x} times')
    time.sleep(300)
    main()


if __name__ == '__main__':
    saved_dict = get_saved()
    main()

# TODO: add functionality to track from Farnell and other websites
