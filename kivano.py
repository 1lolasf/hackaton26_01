import csv
import json

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag


URL = 'https://www.kivano.kg/'


def get_html(url: str, category: str, params: str=''):
    html = requests.get(
        url=url + 'f/' + category,
        params=params,
        verify=False
    )
    return html.text


def get_cards_from_html(html: str) -> ResultSet:
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_='item product_listbox oh')
    return cards


def parse_data_from_cards(cards: ResultSet[Tag]) -> list[dict]:
    result = []
    for card in cards:
        title = card.find('div', class_='listbox_title oh').text
        price = card.find('div', class_='listbox_price text-center').text
        img_link = Tag.find('div', class_='listbox_img pull-left').find('img').get('src')

        obj = {
                'title': title.strip(),
                'price': price.strip(),
                'img_link': img_link,
            }
        result.append(obj)
    return result


def write_to_csv(data: list, file_name: str) -> None:
    fieldnames = data[0].keys()
    with open(f'{file_name}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_last_page(html: str) -> int:
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.find('div', class_='pager-wrap').get('data-page')
    return int(last_page)


def main() -> None:
    result = []
    html = get_html(URL, 'mobilnye-telefony')
    last_page = get_last_page(html)
    for page in range(1, last_page+1):
        html = get_html(URL, 'mobilnye-telefony', params=f'page={page}')
        cards = get_cards_from_html(html)
        result_from_page = parse_data_from_cards(cards)
        result.extend(result_from_page)
    write_to_csv(result, 'smartphones')


if __name__ == '__main__':
    main()