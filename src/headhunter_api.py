import datetime
import json
from pprint import pprint

import requests

from src.abstracts_classes import AbstractApi, ApiError
from src.vacancy import Vacancy


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
