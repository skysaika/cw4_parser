from pprint import pprint


from src.superjob_api import SuperJobAPI, SJVacancy

superjob_api = SuperJobAPI()
sj_vacancies = superjob_api.get_vacancies_sj("Python")
pprint(sj_vacancies)


# пример для repr:
vacancy = SJVacancy(profession="Python Developer", payment_from='100 000', payment_to='150 000', currency="rub", title='SkyPro', link='URL: https://superjob.ru/vacancy/123456')
# print(repr(vacancy))
