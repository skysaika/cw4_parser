class Vacancy:
    def __init__(self, title, salary, description, url):
        self.title = title  #  Название вакансии
        self.salary = salary  #  Информация о зарплате в виде словаря. Может содержать ключи 'from', 'to' и 'currency'.
        self.description = description  # Описание вакансии
        self.url = url  # Ссылка на вакансию

    def __str__(self):
        """
            Возвращает строковое представление вакансии в формате:
            "название='...', зарплата='...', описание='...', ссылка='...'"
        """
        return f"title='{self.title}', salary='{self.salary}', " \
               f"description='{self.description}', url='{self.url}'"


class HHVacancy(Vacancy):
    """Класс вакансий HH для создания списка экземпляров """
    __slots__ = (
        'title', 'salary_min', 'salary_max', 'currency',
        'employer', 'link',
    )

    def __init__(self, salary, description, url, title='', salary_min=None, salary_max=None, currency="rub",
                 employer='', link=''):
        super().__init__(title, salary, description, url)
        self.title = title
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.employer = employer
        self.link = link


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



class SJVacancy(Vacancy):
    """Класс вакансий SJ для создания списка экземпляров"""
    __slots__ = (
        'profession', 'payment_from', 'payment_to',
        'currency', 'title', 'link',
    )

    def __init__(self, salary, description, url, profession='', payment_from=None, payment_to=None, currency="rub",
                 title='', link=''):
        super().__init__(title, salary, description, url)
        self.profession = profession
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.currency = currency
        self.title = title
        self.link = link


    def __str__(self):
        """Строковое представление класса SJVacancy"""
        payment_from = f'От {self.payment_from}' if self.payment_from else ''
        payment_to = f'До {self.payment_to}' if self.payment_to else ''
        currency = self.currency if self.currency else ''
        if self.payment_from is None and self.payment_to is None:
            payment_from = "Не указана"
        return f"{self.title}: {self.profession} \n{payment_from} {payment_to} \n{currency} \n{self.link}"

    def __repr__(self):
        """Возвращает полное представление для отладки класса SJVacancy"""
        return f"SJVacancy(" \
               f"profession='{self.profession}', " \
               f"payment_from='{self.payment_from}', " \
               f"payment_to='{self.payment_to}', " \
               f"currency='{self.currency}', " \
               f"title='{self.title}', " \
               f"link='{self.link}')"

