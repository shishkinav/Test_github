from csv_file_worker import csv_dict_writer
from parse_organization import (
    ParseMainSpravochnik,
    ListOrganizationParser,
    Organization
)


def parse_second_cat(
                    name_main_category, choice_1,
                    name_second_category, choice_2,
                    link_second_cat
                ):
    # работаем по очереди с каждым подразделом
    data = []
    relative_path_file_csv = f'data/{choice_1}_{choice_2}.csv'
    category = ListOrganizationParser(link_second_cat)
    for name_company, link_company in category.lst_organisations:
        tmp_lst = [name_main_category, name_second_category]
        company = Organization(link_company, name_company)
        company.get_param()
        tmp_lst += [
            company.name_company,
            company.url_link,
            company.adress,
            company.phone,
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


def create_readme_catalog(spravochnik):
    cat_main = {number: key for number, key in enumerate(spravochnik.dict_category.keys(), start=1)}
    fieldnames = [
        'number_main_category',
        'name_main_category',
        'number_second_category',
        'name_second_category'
    ]
    relative_path_readme_catalog = 'data/READme_catalog.csv'
    info = []
    for number, name_main_category in cat_main.items():
        for number_main_category, data in enumerate(spravochnik.dict_category.values(), start=1):
            
            if number_main_category == number:
                cat_second = {
                    number: key[0] for number, key in enumerate(data, start=1)
                }
                for number_second_category, name_second_category in cat_second.items():
                    tmp_lst = [number_main_category, name_main_category, number_second_category, name_second_category]
                    info.append(dict(zip(fieldnames, tmp_lst)))
    csv_dict_writer(
                    relative_path_readme_catalog,
                    fieldnames,
                    info
                )


def parse_all_site(spravochnik):
    cat_main = {number: key for number, key in enumerate(spravochnik.dict_category.keys(), start=1)}
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
    
    for number, name_main_category in cat_main.items():
        for number_main_category, data in enumerate(spravochnik.dict_category.values(), start=1):
            if number_main_category == number:
                cat_second = {
                    number: (key[0], key[1]) for number, key in enumerate(data, start=1)
                }
                for number_second_category, (name_second_category, link_second_category) in cat_second.items():
                    info = []
                    # print(number_second_category, (name_second_category, link_second_category))
                    relative_path_file_csv = f'data/{number_main_category}_{number_second_category}.csv'
                    category_lst = ListOrganizationParser(link_second_category)
                    for name_company, url_link_company in category_lst.lst_organisations:
                        tmp_lst = [name_main_category, name_second_category]
                        company = Organization(url_link_company, name_company)
                        company.get_param()
                        tmp_lst += [
                            company.name_company,
                            company.url_link,
                            company.adress,
                            company.phone,
                            company.boss,
                            company.site,
                            company.email,
                            company.link_logo
                        ]
                        info.append(dict(zip(fieldnames, tmp_lst)))
                    csv_dict_writer(
                        relative_path_file_csv,
                        fieldnames,
                        info
                    )
                    print(
                        f'Подкатегория {name_second_category} из раздела {name_main_category} обработана\
                            создан файл {relative_path_file_csv}'
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

choice = input('''
        Введите:
        Y - чтобы создать READme каталог
        A - чтобы запустить парсинг всего сайта целиком
        другие символы - чтобы перейти к выбору разделов / подкатегорий.
    ''')

if choice == 'Y' or choice == 'y':
    create_readme_catalog(spravochnik)
    print('READme файл сформирован')
elif choice == 'A' or choice == 'a':
    parse_all_site(spravochnik)
    print('ПОЗДРАВЛЯЕМ ПАРСИНГ ВСЕГО САЙТА ЗАВЕРШЕН')
else:
    # словарь разделов
    cat_main = {number: key for number, key in enumerate(spravochnik.dict_category.keys(), start=1)}
    for k, v in cat_main.items():
        print(f'[{k}] - {v}')
    choice_1 = int(input('\nВведите номер раздела:\n'))
    name_main_category = cat_main.get(choice_1)

    # словарь подкатегорий выбранного раздела для выбора пользователем
    for number, data in enumerate(spravochnik.dict_category.values(), start=1):
        if number == choice_1:
            cat_second = {
                number: key for number, key in enumerate(data, start=1)
            }
    for k, v in cat_second.items():
        print(f'[{k}] - {v[0]}')
    choice_2 = int(input('\nВведите номер подраздела (если хотите спарсить весь раздел введите "0"):\n'))
    if choice_2 != 0:
        # забираем данные для старта парсинга подраздела
        for k, v in cat_second.items():
            if k == choice_2:
                name_second_category, link_second_cat = v

        # три переменные образованы для парсинга
        # print(name_main_category, name_second_category, link_second_cat)
        parse_second_cat(name_main_category, choice_1, name_second_category, choice_2, link_second_cat)
    else:
        choice_2 = 1
        for name_second_category, link_second_cat in cat_second.values():
            parse_second_cat(name_main_category, choice_1, name_second_category, choice_2, link_second_cat)
            choice_2 += 1