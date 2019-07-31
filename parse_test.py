from bs4 import BeautifulSoup
import requests
import re, string

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
# pattern=r'[\n\s]+(.+)[/n/s]+'
pattern='\w+'
lst_main_category = []
for cat in category_m:
    tmp = re.findall(pattern, cat.text)
    lst = ' '
    lst_main_category.append(lst.join(tmp))
# получили на выходе только названия главных категорий
category_s = content.find_all('div', {'class': 'block'}) # распарсили места с названиями разделов

cat_s = {}
count = 1
tmp_lst = []
# проходим по каждой из двадцати главных категорий и в словарь сохраняем по каждой список href + название подкатегории
for cat in category_s:
    for _ in cat.find_all('a'):
        tmp_lst.append([_.get('href'), _.get('title')])
    cat_s.update({count: tmp_lst})
    tmp_lst = []
    count += 1
    # print([[i.get('href'), i.get('title')] for i in cat.find_all('a')]) # ссылку на подкатегорию и название подкатегории
for key, value in cat_s.items():
    print(key, value)
final_dict = {}
for _ in lst_main_category:
    final_dict.update({_: cat_s[lst_main_category.index(_) + 1]})
# for key, value in final_dict.items():
#     print(key, value)
