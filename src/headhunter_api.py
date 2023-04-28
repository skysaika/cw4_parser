import datetime
import json
from pprint import pprint

import requests

from src.abstracts_classes import AbstractApi, ApiError


class HeadHunterAPI(AbstractApi):
    """Класс HeadHunterAPI, наследуется от абстрактного AbstractApi"""
    __url_hh = "https://api.hh.ru/vacancies?only_with_salary=true"

    def __init__(self):
        """Инициализатор HeadHunterAPI"""
        self.__vacancies_list = []

    def get_request(self, vacancy_for_search: str, page: int):
        """Переопределенный метод для запроса к HeadHunter.ru"""
        params = {
            "text": vacancy_for_search,
            "page": page,
            'area': 113,
            "per_page": 100,
        }

        response = requests.get(self.__url_hh, params=params)
        if response.status_code != 200:
            raise ApiError("server answer with status_code" + "response.status_code")
        if "items" not in response.json():
            raise ApiError("objects key not found in " + response.json()[:140])
        return response.json()["items"]

    def get_vacancies_hh(self, vacancy_for_search):
        """Метод получения общих данных по вакансиям HeadHunterApi"""
        pages = 1
        current_page = 0
        now = datetime.datetime.now()
        current_time = now.strftime(f"%d.%m.%Y Время: %X")

        for page in range(pages):
            current_page += 1
            print(f"Парсинг страницы c HH.ru: {page + 1}", end=": ")
            values = self.get_request(vacancy_for_search, page)
            print(f"Найдено {len(values)} вакансий.")
            self.__vacancies_list.extend(values)
            print(f"Парсинг окончен, собрано {len(self.__vacancies_list)} вакансий с {current_page} страниц\n"
                  f"Информация собрана {current_time}\n")
        return self.__vacancies_list

    @property
    def get_vacancies_list(self):
        """Метод для вывода общих собранных данных"""
        return self.__vacancies_list


class HHVacancy:
    """Класс вакансий HH для создания списка экземпляров """
    __slots__ = (
        'title', 'salary_min', 'salary_max', 'currency',
        'employer', 'link', 'salary_sort_min', 'salary_sort_max',
    )

    def __init__(self, title='', salary_min=None, salary_max=None, currency="rub", employer='', link=''):
        self.title = title
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.employer = employer
        self.link = link

        self.salary_sort_min = salary_min
        self.salary_sort_max = salary_max
        if currency and currency == 'USD':
            self.salary_sort_min = self.salary_sort_min * 83 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 83 if self.salary_sort_max else None

    def __str__(self):
        """Строковое представление класса HHVacancy"""
        # определим, если нет salary_min, salary_max или не указана salary, currency
        salary_min = f'От {self.salary_min}' if self.salary_min else ''
        salary_max = f'До {self.salary_max}' if self.salary_max else ''
        currency = self.currency if self.currency else ''
        if self.salary_min is None and self.salary_max is None:
            salary_min = "Не указана"
        return f"{self.employer}: {self.title} \n{salary_min} {salary_max} {currency} \nURL: {self.link}"

    def __repr__(self):
        """Возвращает полное представление для отладки класса HHVacancy"""
        return f"HHVacancy(" \
               f"title='{self.title}', " \
               f"salary_min='{self.salary_min}', " \
               f"salary_max='{self.salary_max}', " \
               f"currency='{self.currency}', " \
               f"employer='{self.employer}', " \
               f"link='{self.link}')"

    def __gt__(self, other):
        """Метод сравнения min зарплат НН"""
        if not other.salary_sort_min:
            return True
        if not self.salary_sort_min:
            return False
        return self.salary_sort_min >= other.salary_sort_min


class JSONSaverHH:
    """Класс для сохранения данных c HH в файл json"""

    def __init__(self, vacancy_for_search):
        self.__filename = f'{vacancy_for_search.title()}.json'

    @property
    def filename_hh(self):
        """Геттер возвращает имя файла"""
        return self.__filename

    def add_vacancies_hh(self, data):
        """Функция для добавления вакансий HH"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select_hh(self):
        """Функция выбора данных для записи в json"""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Создадим список вакансий HH
        vacancies = []
        for row in data:
            salary_min, salary_max, currency = None, None, None
            if row['salary']:
                salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary']['currency']
            vacancies.append(HHVacancy(
                row['name'],
                salary_min,
                salary_max,
                currency,
                row['employer']['name'],
                row['employer']['alternate_url']
            ))
        with open('JSON_HH_test.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)


    # @staticmethod
    # def instantiate_vacancy(vac_data):
    #     """Принимает данные одной вакансии с HH и возвращает экземпляр класса Vacancy"""
    #     vacancy = HHVacancy(
    #         title=vac_data['name'],
    #         salary_min=vac_data['salary']['from'],
    #         salary_max=vac_data['salary']['to'],
    #         currency=vac_data['salary']['currency'],
    #         employer=vac_data['employer']['name'],
    #         link=vac_data['alternate_url']
    #     )
    #     return vacancy

