from csv_file_worker import csv_dict_writer
from parse_organization import (
    ParseMainSpravochnik,
    ListOrganizationParser,
    Organization
)

relative_path_file_csv = 'data/20190801_organizations.csv'

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
data = []
# приступаем к массовому парсингу ресурса
spravochnik = ParseMainSpravochnik()
for main_category, lst_second_category in spravochnik.dict_category.items():
    # работаем по очереди с каждым разделом
    for name_second_category, url_link in lst_second_category:
        # работаем по очереди с каждым подразделом
        category = ListOrganizationParser(url_link)
        for name_company, link_company in category.lst_organisations:
            tmp_lst = [main_category, name_second_category]
            company = Organization(url_link, name_company)
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

# записываем данные в csv файл
csv_dict_writer(
    relative_path_file_csv,
    fieldnames,
    data
)