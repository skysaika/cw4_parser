import datetime


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
            "per_page": 10,
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
