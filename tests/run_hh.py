from pprint import pprint

from src.headhunter_api import HeadHunterAPI, HHVacancy

hh_api = HeadHunterAPI()
hh_vacancies = hh_api.get_vacancies_hh("Python")
pprint(hh_vacancies)

vacancy = HHVacancy(title="Python Developer", salary_min='100 000', salary_max='150 000', currency="rub", employer='SkyPro', link='URL: https://hh.ru/vacancy/123456')
print(repr(vacancy))