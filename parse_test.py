from bs4 import BeautifulSoup
import requests


# base_url = 'https://mysbor.ru/spravochnik/'

# r = requests.get(base_url)
# soup = BeautifulSoup(r.content, 'html.parser')
# with open('data/test.html', 'w') as html_doc:
#     for line in soup.prettify():
#         html_doc.write(line)

base_html = 'data/test.html'
with open(base_html) as html_doc:
    soup = BeautifulSoup(html_doc, 'html.parser')
    # movie_link = soup.find('div', {'class': "title active"})
    # print(movie_link)

content = soup.find('div', {'class': 'content-container'}).div.div.div.div.div
category_m = content.find_all('div', {'class': 'title'}) # распарсили места с названиями разделов
for cat in category_m:
    print(cat.text) # получили на выходе только названия главных категорий
category_s = content.find_all('div', {'class': 'block'}) # распарсили места с названиями разделов
print(len(category_m))
print(len(category_s))
print(
    len(
        [cat.find('span') for cat in category_s]
    )
)
# for cat in category_s:
#     print(cat.a.get('href') + ' - ' + cat.a.get('title')) # ссылку на подкатегорию и название подкатегории
    # print(cat.a)
