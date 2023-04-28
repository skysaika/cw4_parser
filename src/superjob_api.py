import datetime
import json
from pprint import pprint

import requests

from data.token_sj import token_sj
from src.abstracts_classes import AbstractApi, ApiError


class SuperJobAPI(AbstractApi):
    """Класс SuperJobAPI, наследуется от абстрактного AbstractApi"""
    __url_sj = "https://api.superjob.ru/2.0/vacancies/?"

    def __init__(self):
        """Инициализатор SuperJobAPI"""
        self.__vacancies_list = []

    def get_request(self, vacancy_for_search: str, page: int):
        """Переопределенный метод для запроса к SuperJob.ru"""
        headers = {'X-Api-App-Id': token_sj}

        params = {
            "keyword": vacancy_for_search,
            "page": page,
            'count': 100,
            'c': 1,
            "per_page": 100,
        }
        response = requests.get(self.__url_sj, headers=headers, params=params)
        if response.status_code != 200:
            raise ApiError("server answer with status_code" + "response.status_code")
        if "objects" not in response.json():
            raise ApiError("objects key not found in " + response.json()[:140])
        return response.json()["objects"]

    def get_vacancies_sj(self, vacancy_for_search, page=10):
        """Метод получения общих данных по вакансиям SuperJobAPI"""
        pages = 1
        current_page = 0
        now = datetime.datetime.now()
        current_time = now.strftime(f"%d.%m.%Y Время: %X")

        for page in range(pages):
            current_page += 1
            print(f"Парсинг страницы c SJ.ru: {page + 1}", end=": ")
            values = self.get_request(vacancy_for_search, page)
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies_list.extend(values)
            print(f"Парсинг окончен, собрано {len(self.__vacancies_list)} вакансий с {current_page} страниц\n"
                  f"Информация собрана {current_time}\n")
        return self.__vacancies_list

    def get_vacancies_list(self):
        """Метод для вывода общих собранных данных"""
        return self.__vacancies_list


class SJVacancy:
    """Класс вакансий SJ для создания списка экземпляров"""
    __slots__ = (
        'profession', 'payment_from', 'payment_to',
        'currency', 'title', 'link',
        'payment_sort_from', 'payment_sort_to')

    def __init__(self, profession='', payment_from=None, payment_to=None, currency="rub", title='', link=''):
        self.profession = profession
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.currency = currency
        self.title = title
        self.link = link

        self.payment_sort_from = payment_from
        self.payment_sort_to = payment_to
        if currency and currency == 'USD':
            self.payment_sort_from = self.payment_sort_from * 83 if self.payment_sort_from else None
            self.payment_sort_to = self.payment_sort_to * 83 if self.payment_sort_to else None

    def __str__(self):
        """Строковое представление класса SJVacancy"""
        payment_from = f'От {self.payment_from}' if self.payment_from else ''
        payment_to = f'До {self.payment_to}' if self.payment_to else ''
        currency = self.currency if self.currency else ''
        if self.payment_from is None and self.payment_to is None:
            payment_from = "Не указана"
        return f"{self.title}: {self.profession} \n{payment_from} {payment_to} \n{currency} \n{self.link}"

    def __repr__(self):
        """Возвращает полное представление для отладки класса SJVacancy"""
        return f"SJVacancy(" \
               f"profession='{self.profession}', " \
               f"payment_from='{self.payment_from}', " \
               f"payment_to='{self.payment_to}', " \
               f"currency='{self.currency}', " \
               f"title='{self.title}', " \
               f"link='{self.link}')"

    def __gt__(self, other):
        """Метод сравнения min зарплат SJ"""
        if not other.payment_sort_from:
            return True
        if not self.payment_sort_from:
            return False
        return self.payment_sort_from >= other.payment_sort_from


class JSONSaverSJ:
    """Класс для сохранения данных c SJ в файл json"""

    def __init__(self, vacancy_for_search):
        self.__filename = f'{vacancy_for_search.title()}.json'

    @property
    def filename_sj(self):
        """Геттер возвращает имя файла"""
        return self.__filename

    def add_vacancies_sj(self, data):
        """Функция для добавления вакансий SJ"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select_sj(self):
        """Функция выбора данных для записи в json"""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Создадим список вакансий SJ
        vacancies = []
        for row in data:
            payment_from, payment_to, currency = row['payment_from'], row['payment_to'], row['currency']
            vacancies.append(SJVacancy(
                row['profession'],
                payment_from,
                payment_to,
                currency,
                row['client'],
                row['link']
            ))
        with open('JSON_SJ_test.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    # @staticmethod
    # def instantiate_vacancy(vac_data):
    #     """Принимает данные одной вакансии с SJ и возвращает экземпляр класса Vacancy"""
    #     vacancy = SJVacancy(
    #         title=vac_data['profession'],
    #         salary_min=vac_data['payment_from'],
    #         salary_max=vac_data['payment_to'],
    #         currency=vac_data['currency'],
    #         employer=vac_data['title'],
    #         link=vac_data['link']
    #     )
    #     return vacancy

