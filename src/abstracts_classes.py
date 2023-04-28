from abc import ABC, abstractmethod


class ApiError(Exception):
    """Класс для вывода ошибок сервера"""
    pass


class AbstractApi(ABC):
    """Абстрактный класс"""

    def __get_request(self, search_vacancy: str, page: int) -> list:
        """Метод возвращает запрос к сайтам вакансий"""
        pass

    # @staticmethod
    # @abstractmethod
    # def instantiate_vacancy(vac_data):
    #     """Принимает данные одной вакансии с SJ и возвращает экземпляр класса Vacancy"""
