import json


class JSONSaverSJ:
    """Класс для сохранения данных c SJ в файл json"""

    def __init__(self):
        self.__filename = f'JSON_SJ.json'

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
            try:
                if row['payment_to'] == 0:  ### Проверка на диапазон зарплаты
                    salary = {'from': row['payment_from'], 'currency': row['currency']}
                elif row['payment_from'] == 0:
                    salary = {'from': row['payment_to'], 'currency': row['currency']}
                else:
                    salary = {'from': row['payment_from'], 'to': row['payment_to'],
                              'currency': row['currency']}
            except:
                salary = {'from': 0, 'currency': 'RUR'}

            vacancy_dict = {
                'profession': row['profession'],
                'salary': salary,
                'description': row['candidat'],
                'company_name': row['firm_name'],
                'link': row['link']
            }
            vacancies.append(vacancy_dict)
        with open('JSON_SJ.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)


class JSONSaverHH:
    """Класс для сохранения данных c HH в файл json"""

    def __init__(self):
        self.__filename = f'JSON_HH.json'

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
            try:
                if row['salary']['to'] == None:  ### Проверка на диапазон зарплаты
                    salary = {'from': row['salary']['from'], 'currency': row['salary']['currency']}
                elif row['salary']['from'] == None:
                    salary = {'from': row['salary']['to'], 'currency': row['salary']['currency']}
                else:
                    salary = {'from': row['salary']['from'], 'to': row['salary']['to'],
                              'currency': row['salary']['currency']}
            except:
                salary = {'from': 0, 'currency': 'RUR'}

            vacancy_dict = {
                'profession': row['name'],
                'salary': salary,
                'description': row['snippet']['requirement'],
                'company_name': row['employer']['name'],
                'link': row['alternate_url']
            }
            vacancies.append(vacancy_dict)
        with open('JSON_HH.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)
