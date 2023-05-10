
from src.headhunter_api import HeadHunterAPI
from src.jsonsaver import JSONParser, JSONSaverHH, JSONSaverSJ
from src.superjob_api import SuperJobAPI


def user_interaction():
    """
    Функция, которая осуществляет взаимодействие с пользователем, запрашивая данные для поиска вакансий и вывода результатов
    """
    try:
        hh_api, sj_api = check_platform()  # Получение API для выбранных платформ
        hh_vacancies, sj_vacancies = get_class_by_platform(hh_api, sj_api)  # Получение вакансий для выбранных платформ
        filter_word_input = filter_words()  # Получение ключевых слов
        salary_input = salary_sort()  # Получение минимальной зарплаты
        output_results(hh_vacancies, sj_vacancies, filter_word_input, salary_input) ### Вывод результатов поиска
    except:
        print('До скорой встречи!')


def check_platform():
    print("Введите 'Выход/Exit' чтобы закрыть программу")
    while True:
        """Цикл while запускает бесконечный цикл ввода пользователем 
        платформ для поиска. Если пользователь вводит 'выход' или 'exit',
        программа закрывается."""
        platform_input = input('Введите название платформы для поиска (HeadHunter\SuperJob): ').lower().split(' ')
        if 'выход' in platform_input or 'exit' in platform_input:
            print('Выход из программы')
            raise SystemExit
        # Если пользователь ввел обе платформы (HeadHunter и SuperJob):
        elif set(platform_input) & {'headhunter', 'hh'} and set(platform_input) & {'superjob', 'sj'}:
            hh_api = HeadHunterAPI()
            sj_api = SuperJobAPI()
            print('Вы выбрали поиск в HH и SJ')
            return hh_api, sj_api
            # только HeadHunter:
        elif set(platform_input) & {'headhunter', 'hh'}:
            hh_api = HeadHunterAPI()
            print('Вы выбрали поиск в HH')
            return hh_api, None
        elif set(platform_input) & {'superjob', 'sj'}:
            # только SuperJob
            sj_api = SuperJobAPI()
            print('Вы выбрали поиск в SJ')
            return None, sj_api
            # ни одну не выбрал:
        else:
            print('Вы не ввели платформу')
            continue


def get_class_by_platform(hh_api, sj_api):
    """Функция для получения объектов классов API в
    зависимости от выбранных платформ"""

    search_query = str(input("Введите поисковый запрос: "))

    if 'выход' in search_query or 'exit' in search_query:
        print('Выход из программы')  # Проверка на выход из программы
        raise SystemExit
    if hh_api is not None and sj_api is not None:
        # Если выбраны обе платформы, то получаем объекты для каждой
        hh_vacancies = hh_api.get_vacancies_hh(search_query)
        sj_vacancies = sj_api.get_vacancies_sj(search_query)
        return hh_vacancies, sj_vacancies
    if sj_api is not None:
        # Если выбран только SuperJob
        sj_vacancies = sj_api.get_vacancies_sj(search_query)
        return None, sj_vacancies
    if hh_api is not None:
        # Если выбран только HeadHunter
        hh_vacancies = hh_api.get_vacancies_hh(search_query)
        return hh_vacancies, None


def salary_sort():
    while True:
        user_salary = input("Введите минимальную зарплату для поиска (только цифры, rub): ")
        if 'выход' in user_salary or 'exit' in user_salary:
            print('Выход из программы')
            raise SystemExit
        if not user_salary.strip():  # Проверка, что введено значение не пустое Если значение пустое, то возвращается минимальное значение 0.
            print("Вы не ввели минимальную зарплату. Минимальное значение будет равно 0")
            return '0'
        try:
            user_salary = int(user_salary)
            return user_salary
        except ValueError:
            print("Некорректное значение. Минимальное значение будет равно 0")
            return '0'


def filter_words():
    """ Функция запрашивает у пользователя ввод ключевых слов для фильтрации вакансий по
    описанию и возвращает введенные слова или пустую строку, если пользователь ничего не ввел.
    Если введено "выход" или "exit", то программа завершается."""

    words = input(
        "Введите ключевые слова для фильтрации вакансий в описании(чем больше слов тем больше найдётся соответствий):\n")
    if 'выход' in words or 'exit' in words:
        print('Выход из программы')
        raise SystemExit
    elif words == '':
        print('Вы ничего не ввели')
        return words
    else:
        return words


def output_results(hh_vacancies, sj_vacancies, filter_words, salary_input):
    """
       Функция вывода результатов поиска вакансий.
       - hh_vacancies: список вакансий с сайта HeadHunter, полученный из API;
       - sj_vacancies: список вакансий с сайта SuperJob, полученный из API;
       - filter_words: ключевые слова для фильтрации вакансий;
       - salary_input: минимальная зарплата для поиска вакансий.
       """

    hh = JSONSaverHH()
    res_hh = hh.select_hh(hh_vacancies)
    sj = JSONSaverSJ()
    res_sj = sj.select_sj(sj_vacancies)
    json_saver = JSONParser()  ### Создание объекта для сохранения результатов в JSON-файл
    json_saver.sort_and_save_to_JSON(hh=res_hh, sj=res_sj)  ### Добавление вакансий
    json_saver.search_words(filter_words)
    json_saver.sort_by_salary(salary_input)  ### Фильтрация вакансий по зарплате
    final = json_saver.json_result()  ### Получение результата в виде словаря
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    print('\n')
    if len(final) == 0:  ### Если список вакансий пуст, выводим сообщение об отсутствии результатов
        print('Вакансий по вашему запросу нет')
    else:
        for x in range(top_n):# Цикл для вывода топ N вакансий
            # print(final[x])
            try:
                text = final[x]['description'].replace('<highlighttext>', '').replace('</highlighttext>',
                                                                                      '')  # Удаление тегов из описания вакансии
                try:  ### Обработка зарплаты
                    salary_text = f"Зарплата: {final[x]['salary']['from']}-{final[x]['salary']['to']} руб"
                except:  ### Если зарплата не указана, выводим соответствующее сообщение
                    if final[x]['salary']['from'] == 0:
                        salary_text = 'Зарплата не указана'
                    else:
                        salary_text = f"Зарплата: {final[x]['salary']['from']} руб"
                # Вывод названия вакансии, зарплаты, описания вакансии и ссылки на неё
                print(f"{final[x]['profession']}\n{salary_text}\nОписание вакансии:\n{text}\nСсылка: {final[x]['link']}\n")
            except:
                # Если вакансий меньше, чем заданное количество, выводим соответствующее сообщение и завершаем цикл
                print('Больше вакансий нет')
                break
