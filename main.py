import bs4, requests, smtplib, json, time
from config import *

urlDict = {'https://thepihut.com/products/raspberry-pi-4-model-b': {'4B (1Gb)': '41005997392067',
                                                                    '4B (2Gb)': '20064052674622',
                                                                    '4B (4Gb)': '20064052740158',
                                                                    '4B (8Gb)': '31994565689406'},
           'https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-3-model-a-plus': {'3B': '13584708763710'},
           'https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-3-model-b-plus': {'3A': '18157318733886'},
           'https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-pico': {'Pico': '37979757412547'}}

# savedDict = {'4B (1Gb)': 'Sold out', '4B (2Gb)': 'Sold out', '4B (4Gb)': 'Sold out', '4B (8Gb)': 'Sold out', '3B': 'Sold out', '3A': 'Sold out', 'Pico': 'In stock, ready to be shipped'}
savedDict = {}
statusDict = {}
x = 0

selector = '#shopify-section-product-template > section > div.container.container--flush > div.product-block-list.product-block-list--medium > div > div.product-block-list__item.product-block-list__item--info > div > script'

def getSaved():
    for url in urlDict:

        inventories = getInventories(url)
        for item in urlDict[url]:
            num = urlDict[url][item]
            msg = inventories[num]['inventory_message']
            savedDict[item] = msg

    return savedDict


def getInventories(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select(selector)
    jsondata = json.loads(elems[0].text)
    inventories = (jsondata['inventories'])
    return inventories


def sendEmail(item, status, url):
    conn = smtplib.SMTP(host, port, timeout=120)
    conn.ehlo()
    conn.starttls()
    conn.login(sender_email, sender_pass)

    conn.sendmail(sender_email, receiver_email,
                  f'Subject: PiHut Stock Change\n\nThe stock status of the Raspberry Pi {item} has changed to \'{status}\' at this link:\n\n{url}')

    conn.quit()


def main():
    global savedDict, x
    for url in urlDict:
        inventories = getInventories(url)

        for item in urlDict[url]:
            num = urlDict[url][item]
            msg = inventories[num]['inventory_message']
            statusDict[item] = msg

            if statusDict[item] != savedDict[item]:
                email = f'{item}: {statusDict[item]}: {url}'
                print(email)
                sendEmail(item, statusDict[item], url)
                savedDict = statusDict
            else:
                pass

    x += 1
    print(f'Status checked {x} times')
    time.sleep(300)
    main()

if __name__ == '__main__':
    savedDict = getSaved()
    main()

# TODO: update to fit PEP
# TODO: add functionality to track from Farnell and other websites



