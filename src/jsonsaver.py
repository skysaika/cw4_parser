import json
import os
import re


class JSONSaverSJ:
    """Класс для сохранения данных c SJ в файл json"""

    def __init__(self):
        self.__filename = f'JSON_SJ.json'

    @property
    def filename_sj(self):
        """Геттер возвращает имя файла"""
        return self.__filename

    def select_sj(self, data):
        """Функция выбора данных для записи в json"""
        # Создадим список вакансий SJ
        vacancies = []
        if data == None:
            return None
        else:
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
            return vacancies


class JSONSaverHH:
    """Класс для сохранения данных c HH в файл json"""

    def __init__(self):
        self.__filename = f'JSON_HH.json'

    @property
    def filename_hh(self):
        """Геттер возвращает имя файла"""
        return self.__filename

    def select_hh(self, data):
        """Функция выбора данных для записи в json"""
        # Создадим список вакансий HH
        vacancies = []
        if data == None:
            return None
        else:
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
            return vacancies


class JSONParser:
    """Сохраняет вакансии в финальный json, в котором будет дальнейшая сортировка"""
    def __init__(self):
        self.__filename = f'JSON_FINAL.json'

    def sort_and_save_to_JSON(self, hh = None, sj = None):
        """Функция сортировки вакансий по выбранным платформам и сохранения в единый json"""
        if hh is not None and sj is None:  ### Если выбрана только hh -> сохраняю только hh
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([row for row in hh], key=lambda v: v['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        elif sj is not None and hh is None:  ### Если выбрана только sj -> сохраняю только sj
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([row for row in sj], key=lambda v: v['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        elif hh is None and sj is None:
            print('')
        else:
            """При получении двух аргументов для каждого создаётся свой json файл и сохранение в 
                        каждый словарь с их API. В дальнейшем словари складываются,сортируются по зарплате и 
                        сохраняются в общий json, а временные файлы удаляются
                        """
            with open('JSON_HH.json', 'w', encoding='utf-8') as file:
                json.dump([row for row in hh], file, ensure_ascii=False, indent=4)
            with open('JSON_SJ.json', 'w', encoding='utf-8') as file:
                json.dump([row for row in sj], file, ensure_ascii=False, indent=4)
            # Открыть первый файл JSON и сохранить данные
            with open('JSON_HH.json', 'r', encoding='utf-8') as f:
                hh = json.load(f)
            # Открыть второй файл JSON и сохранить данные
            with open('JSON_SJ.json', 'r', encoding='utf-8') as f:
                sj = json.load(f)

            vacancies = hh + sj  ### Сложение двух словарей
            """Перед сохранением в общий json происходит сортировка по зарплате(в начале словаря самое большое значение)"""
            sorted_vacancies = sorted(vacancies, key=lambda v: v['salary']['from'], reverse=True)
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(sorted_vacancies, file, ensure_ascii=False, indent=4)

            # удаляем JSON-файлы
            os.remove("JSON_HH.json")
            os.remove("JSON_SJ.json")

    def sort_by_salary(self, user_salary: int):
        """Функция сортировки по зарплате, сначала рубли, другие валюты в конце.
        Возвращает список вакансий с заданной зарплатой.

        salary_int Зарплата в формате "100 000-150 000 руб."
        Список вакансий."""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        with open(self.__filename, 'w', encoding='utf-8') as file:
            vacancy_by_salary = []
            currency = ['руб', 'rur', 'rub', 'RUR']
            for row in data:
                try:
                    """Проверка, что зарплата отвечает заданным требованиям"""
                    if int(row['salary']['from']) >= int(user_salary):
                        vacancy_by_salary.append(row)
                    ### USD, EUR пересчитаются по условному курсу 80 руб за единицу
                    elif row['salary']['currency'] not in currency and int(row['salary']['from'])*80 > user_salary:
                        vacancy_by_salary.append(row) ### Добавление вакансии в список вакансий с требуемой зарплатой.
                except:
                    continue
            json.dump(vacancy_by_salary, file, ensure_ascii=False, indent=4)

    def search_words(self, search_words):
        """Функция поиска по ключевым словам, заданным пользователем"""
        if search_words == '':  # если не задано ничего
            with open(self.__filename, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
            return vacancies  # то вернет все вакансии из файла
        else:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)  # иначе начнет поиск по ключевым словам
            with open(self.__filename, 'w', encoding='utf-8') as file:
                search_dict = []
                words_lower = search_words.lower()  # Приведение запроса и заголовков вакансий к нижнему регистру
                split_vacancy = re.findall(r'\b\w+\b', words_lower)  # Разбиение запроса и заголовков на отдельные слова
                for row in vacancies:  # Поиск совпадений между словами запроса и описанием вакансий
                    title_lower = str(row['description']).lower()
                    split_title = re.findall(r'\b\w+\b', title_lower)
                    if set(split_vacancy) & set(split_title): # если множества пересекаются
                        search_dict.append(row)
                # Сохранение найденных слов в файл
                json.dump(search_dict, file, ensure_ascii=False, indent=4)

    def json_result(self):
        """Вывод итоговой информации по файлу json"""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            final = json.load(file)
            return final
