from bs4 import BeautifulSoup
import requests
import re, string


BASE_URL = 'https://mysbor.ru'


def open_data_html(url_link, file=False):
    if file:
        with open(url_link) as html_doc:
            soup = BeautifulSoup(html_doc, 'html.parser')
    else:
        r = requests.get(url_link)
        soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def clear_value(value: str):
    pattern_1 = '^[\n\s]*'
    pattern_2 = '[\n\s]*$'
    return re.sub(pattern_2, '', re.sub(pattern_1, '', value))


class ListOrganizationParser():
    '''
    по переданному частично url'у со списком организаций, либо
    по относительному пути до файла и атрибуту file=True,
    объект класса в своём свойстве lst_organisations приобретает
    список кортежей вида:
        [(name_company, her_relative_link),
        (name_company, her_relative_link),
        (name_company, her_relative_link),
        ...]
    '''
    def __init__(self, url_link, file=False):
        self.lst_organisations = self.unpack(
            url_link, file=file
        )
        
    def unpack(self, url_link, file=False):
        soup = open_data_html(
            url_link=url_link,
            file=file
        )
        
        organizations = soup.find_all('div', {'class': 'title'})
        
        lst_organizations = [
            (
                clear_value(_.a.text),
                _.a.get('href')
            )
            for _ in organizations
        ]
        return lst_organizations


class Organization():
    '''
    id - тип integerField, primary key, генерация порядкового номера автоматическая
    id_category - тип integerField, ForeignKey (связка с категорией организации)
    id_second_category - тип integerField, ForeignKey (связка с подкатегорией организации)
    name_company - тип charField (string), ограничение 250 символов
    logo_company - тип charField (link, string), ограничение 250 символов
    description - тип TextField (string), ограничение 600 сиволов, краткое описание услуг
    adress - тип charField (string), формат - “Город, улица, дом, литера, корпус, офис”, ограничение 128 символов
    boss_company - тип сharField (link, string), ограничение 128 символов
    site_company - тип сharField (link, string), ограничение 64 символа
    email_company - тип сharField (string), ограничение 64 символа
    phone - тип charField (string), формат - +7-(код)-но-ме-р, ограничение 25 символов
    fax - тип charField (string), формат - +7-(код)-но-ме-р, ограничение 25 символов
    '''
    def __init__(self,
                url_link,
                name_company,
                adress=None,
                phone=None,
                boss=None,
                site=None,
                email=None,
                file=False
                ):
        if file:
            self.url_link = url_link
        else:
            self.url_link = BASE_URL + url_link
        self.name_company = name_company
        self.adress = adress
        self.phone = phone
        self.boss = boss
        self.site = site
        self.email = email
        self.file = file

    def get_param(self):
        soup = open_data_html(
            self.url_link,
            self.file
        )
        parameters = soup.find('div', {'class': 'param'})
        items = parameters.find_all('div', {'class': 'item'})
        for item in items:
            try:
                result = re.search(
                    '[\w\-]+',
                    clear_value(item.find('div', {'class': 'col-xs-4 col-md-3'}).text)
                    ).group(0)
                param, value = self.get_item(result, item)
                self.__dict__[param] = value
            except:
                continue

    def get_item(self, text: str, item: str):
        base_dict = {
            'Адрес': ('adress', self.get_data(item)),
            'Телефон': ('phone', self.get_data(item)),
            'Руководитель': ('boss', self.get_data(item)),
            'Сайт': ('site', self.get_data(item)),
            'E-mail': ('email', self.get_data(item))
        }

        for _ in base_dict.keys():
            if _ == text:
                return base_dict.get(_)
        return f'{text} - не найдено в справочнике'

    def get_data(self, item):
        result = clear_value(item.find('div', {'class': 'col-xs-8 col-md-9'}).text)
        if result:
            return result
        else:
            return None

class ParseMainSpravochnik():
    '''
        Объект класса при инициализации парсит справочник из интернета,
        либо при атрибуте file=True, парсит html файл по его относительному
        пути, указанному в атрибуте url_link='относительный_путь_до_файла'

        Результатом, хранящимся в свойсте экземпляра dict_category, является
        справочник вида:
        {
            'название_главной_категории': [
                ['название_подкатегории', 'ссылка_на_организации_подкатегории'],
                ['название_подкатегории', 'ссылка_на_организации_подкатегории'],
                ...
            ]
            'название_главной_категории': [
                ['название_подкатегории', 'ссылка_на_организации_подкатегории'],
                ['название_подкатегории', 'ссылка_на_организации_подкатегории'],
                ...
            ]
            ...
        }
    '''
    def __init__(self, url_link='/spravochnik/', file=False):
        self.dict_category = self.unpack(
            url_link, file=file
        )
    
    def unpack(self, url_link, file=False):
        soup = open_data_html(
            url_link=url_link,
            file=file
        )
        content = soup.find('div', {'class': 'content-container'}).div.div.div.div.div
        # парсим названия главных разделов
        category_m = content.find_all('div', {'class': 'title'}) 
        lst_main_category = []
        for cat in category_m:
            lst_main_category.append(
                clear_value(cat.text)
            )
        # получили на выходе только названия главных категорий
        # парсим подразделы формируя справочник
        category_s = content.find_all('div', {'class': 'block'}) 
        cat_s = {}
        tmp_lst = []
        # проходим по каждой из двадцати главных категорий и в словарь сохраняем по каждой список href + название подкатегории
        for count, cat in enumerate(category_s):
            for _ in cat.find_all('a'):
                tmp_lst.append([_.get('title'), _.get('href')])
            cat_s.update({count + 1: tmp_lst})
            tmp_lst = []

        final_dict = {}
        for _ in lst_main_category:
            final_dict.update(
                {_: cat_s[lst_main_category.index(_) + 1]}
                )
        return final_dict


if __name__ == "__main__":

    # # проверка работы парса главной страницы
    # base_html = 'data/test.html'
    # test3 = ParseMainSpravochnik(url_link=base_html, file=True)
    # for key, value in test3.dict_category.items():
    #     print(key)
    #     for _ in value:
    #         print(_)
    #     print(' ')

    # # проверка работы парса страницы со списком организаций из файла
    # base_html = 'data/lst_org.html'
    # test = ListOrganizationParser(base_html, file=True)
    # for name_company, url_link in test.lst_organisations:
    #     print(name_company, url_link)

    # # проверка работы парса страницы со списком организаций из интернета
    # url_obsluz = '/spravochnik/dosug_otdyh_i_razvlecheniya/detskie_ozdorovitel_nye_lagerya/'
    # test2 = ListOrganizationParser(url_obsluz)
    # for name_company, url_link in test2.lst_organisations:
    #     print(name_company, url_link)
    
    # # проверка парсинга из интернета с использованием комплекса классов
    # spravochnik = ParseMainSpravochnik()
    # print('*'*10, 'ПАРСИМ ВСЕ РАЗДЕЛЫ','*'*10)
    # for main_category, lst_second_category in spravochnik.dict_category.items():
    #     print('*'*10, f'РАБОТАЕМ С РАЗДЕЛОМ {main_category}','*'*10)
    #     for name_second_category, url_link in lst_second_category:
    #         print('*'*10, f'РАБОТАЕМ С ПОДРАЗДЕЛОМ {name_second_category}','*'*10)
    #         category = ListOrganizationParser(url_link)
    #         for name_company, link_company in category.lst_organisations:
    #             print(name_company, url_link)

    # # проверка парсинга параметров организации
    # base_url = 'data/org.html'
    # company = Organization(base_url, 'Чайка', file=True)
    # company.get_param()
    # print(company.__dict__)

    # проверка парсинга параметров организации из интернета
    # base_url = '/spravochnik/1528/'
    # company = Organization(base_url, 'Парус')
    # company.get_param()
    # print(company.__dict__)
    pass