import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

base_url = 'https://books.toscrape.com'

data = {
    'category': [],
    'title': [],
    'price': []
}

def clear_string(string):
    return string.replace('\n', '').strip()

def get_soup(url):
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup

soup = get_soup(f'{base_url}')

# categories = soup.select('div.side_categories ul.nav-list li ul a')
categories = soup.find('div', class_='side_categories').find('ul', class_='nav-list').find('li').find('ul').find_all('a')

for category in categories:
    category_name = clear_string(category.get_text())
    # print(category_name)

    category_link = category['href']
    # print(category['href'])

    soup = get_soup(f'{base_url}/{category_link}')

    results = clear_string(soup.find('form', class_='form-horizontal').find('strong').get_text())
    # print(results)

    num_pages = math.ceil(int(results) / 20)
    # print(num_pages)

    for num_page in range(1, num_pages + 1):
        print(f'scraping page {num_page} of {num_pages} of the {category_name} category')

        category_url = category_link.split('/')[3]
        partial_url = f'{base_url}/catalogue/category/books/{category_url}'

        if num_page == 1:
            url = f'{partial_url}/index.html'
        else:
            url = f'{partial_url}/page-{num_page}.html'

        # print(url)

        soup = get_soup(url)

        products = soup.find_all('article', class_='product_pod')

        for product in products:
            product_title = clear_string(product.find('a', {'title': True}).get_text())
            # print(product_title)

            product_price = clear_string(product.find('p', class_='price_color').get_text())
            # print(product_price)

            # print(product_title, '-', product_price)

            data['category'].append(category_name)
            data['title'].append(product_title)
            data['price'].append(product_price)

df_data = pd.DataFrame(data)
df_data.to_csv('data.csv', sep=';', encoding='utf-8', index=False)