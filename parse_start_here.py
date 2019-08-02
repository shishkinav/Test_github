from csv_file_worker import csv_dict_writer
from parse_organization import (
    ParseMainSpravochnik,
    ListOrganizationParser,
    Organization
)



fieldnames = [
    'main_category',
    'second_category',
    'name_company',
    'url_link',
    'adress',
    'phone',
    'boss',
    'site',
    'email',
    'link_logo'
]

# приступаем к массовому парсингу ресурса
spravochnik = ParseMainSpravochnik()
# словарь разделов
cat_main = {number: key for number, key in enumerate(spravochnik.dict_category.keys(), start=1)}
for k, v in cat_main.items():
    print(f'[{k}] - {v}')
choice_1 = int(input('\nВведите номер раздела:\n'))
name_main_category = cat_main.get(choice_1)

# словарь подкатегорий выбранного раздела для выбора пользователем
for number, data in enumerate(spravochnik.dict_category.values()):
    if number == choice_1:
        cat_second = {
            number: key for number, key in enumerate(data, start=1)
        }
for k, v in cat_second.items():
    print(f'[{k}] - {v[0]}')
choice_2 = int(input('\nВведите номер подраздела:\n'))
# забираем данные для старта парсинга подраздела
for k, v in cat_second.items():
    if k == choice_2:
        name_second_category, link_second_cat = v

# три переменные образованы для парсинга
print(name_main_category, name_second_category, link_second_cat)

# работаем по очереди с каждым подразделом
data = []
relative_path_file_csv = f'data/20190802_{choice_1}_{choice_2}_organizations.csv'
category = ListOrganizationParser(link_second_cat)
for name_company, link_company in category.lst_organisations:
    tmp_lst = [name_main_category, name_second_category]
    company = Organization(link_company, name_company)
    company.get_param()
    tmp_lst += [
        company.name_company,
        company.url_link,
        company.adress,
        company.adress,
        company.boss,
        company.site,
        company.email,
        company.link_logo
    ]
    data.append(dict(zip(fieldnames, tmp_lst)))
    print(f'Данные {company.name_company} получены.')
# записываем данные в csv файл
csv_dict_writer(
    relative_path_file_csv,
    fieldnames,
    data
)
print(f'Файл {relative_path_file_csv} сохранён.')
