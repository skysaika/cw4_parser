from src.headhunter_api import HeadHunterAPI
from src.jsonsaver import JSONSaverHH, JSONSaverSJ
from src.superjob_api import SuperJobAPI

if __name__ == "__main__":
    print('Данная программа предназначена для парсинга вакансий на площадке Super Job и HeadHunter\n')

# vacancy_for_search = 'python'
user_input = str(input('Введите вакансии для поиска: '))

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()

# Получение вакансий с разных платформ
hh_vacancies = hh_api.get_vacancies_hh(user_input)
sj_vacancies = superjob_api.get_vacancies_sj(user_input)

# Сохранение информации о вакансиях c HH в файл:
json_saver_hh = JSONSaverHH()
json_saver_hh.add_vacancies_hh(hh_vacancies)
data_hh = json_saver_hh.select_hh()

# Сохранение информации о вакансиях c SJ в файл:
json_saver_sj = JSONSaverSJ()
json_saver_sj.add_vacancies_sj(sj_vacancies)
data_sj = json_saver_sj.select_sj()

# # Сортируем по min зарплате:
# data = sort_by_salary_min(data)
#
# # Сортируем по max зарплате:
# data = sort_by_salary_max(data)
#
# for row in data:
#     print(row, end=f"\n\n{'=' * 200}\n\n")


# json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
# json_saver.delete_vacancy(vacancy)

# # Создание экземпляра класса для работы с вакансиями
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")
#
#
# # Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HeadHunter", "SuperJob"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
#
#     if not filtered_vacancies:
#         print("Нет вакансий, соответствующих заданным критериям.")
#         return
#
#     sorted_vacancies = sort_vacancies(filtered_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)
