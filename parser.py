import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

result_list = {'title': [], 'price': [], 'href': [], 'description':[]}

def get_task_description(href):
    try:
        href = f'https://freelance.habr.com{href}'
        r = requests.get(href)
        print(r.status_code)
        soup = bs(r.text, "html.parser")
        return soup.find('div', class_='task__description')
    except:
        print("Ошибка парсинга страницы вакансии")


def parse_seearch_page(soup):
    vacancies= soup.find_all('article', class_='task task_list')
    for vacancy in vacancies:
        try:
            result_list['title'].append(vacancy.div.a.text)
            result_list['href'].append(vacancy.div.a['href'])
            result_list['description'].append(get_task_description(vacancy.div.a['description']))
            #this tag span contain price only if it is fixet, otherwise the price has not established  yet
            price = vacancy.aside.find('span', class_='count')
            if price is not None:
                price=price.text
            else:
                price='Цена договорная'
            result_list['price'].append(price)
        except:
            print("Ошибка парсинга страницы поиска")


search_keyword = input('Ключевое слово для поиска:\n')
last_page = False
current_page = 1
while not last_page:
    url = f"https://freelance.habr.com/tasks?_=1651342473032&page={current_page}&q={search_keyword}"
    r = requests.get(url)
    print(r.status_code)
    soup = bs(r.text, "html.parser")
    parse_seearch_page(soup)

    next_page_link = soup.find_all('a', class_='next_page')

    current_page+=1
    #tag a with class 'next_page' will bee [] when current page is the last
    if (next_page_link == []): 
        last_page = True


FILE_NAME = "results.xlsx"  
df = pd.DataFrame(result_list)
df.to_excel(FILE_NAME)