"""Модуль предоставляет класс Fake для генерации тестовых данных через библиотеку Faker.

Класс инкапсулирует экземпляр Faker и даёт удобные обёртки над популярными методами генерации.
"""
from faker import Faker

class Fake:
    """Класс-обёртка над Faker для удобной генерации тестовых данных.

    Позволяет централизовать настройки и предоставлять согласованный набор
    методов для создания фейковых значений (текст, UUID, email, имена и т.д.).
    """

    def __init__(self, faker: Faker):
        """Инициализирует экземпляр Fake с заданным объектом Faker.

        :param faker: Экземпляр :class:`faker.Faker`, используемый для генерации данных.
        :type faker: faker.Faker
        """
        self.faker = faker

    def text(self) -> str:
        """Генерирует случайный абзац текста.

        :return: Случайный текст.
        :rtype: str
        """
        return self.faker.text()

    def uuid(self) -> str:
        """Генерирует случайный UUID версии 4.

        :return: Строковое представление UUID4.
        :rtype: str
        """
        return self.faker.uuid4()

    def email(self, domain: str | None = None) -> str:
        """
        Генерирует случайный email.

        :param domain: Домен электронной почты (например, "example.com").
        Если не указан, будет использован случайный домен.
        :return: Случайный email.
        """
        return self.faker.email(domain=domain)

    def sentence(self) -> str:
        """Генерирует одно случайное предложение.

        :return: Случайное предложение.
        :rtype: str
        """
        return self.faker.sentence()

    def password(self) -> str:
        """Генерирует случайный пароль.

        :return: Сгенерированный пароль.
        :rtype: str
        """
        return self.faker.password()

    def last_name(self) -> str:
        """Генерирует случайную фамилию.

        :return: Случайная фамилия.
        :rtype: str
        """
        return self.faker.last_name()

    def first_name(self) -> str:
        """Генерирует случайное имя.

        :return: Случайное имя.
        :rtype: str
        """
        return self.faker.first_name()

    def middle_name(self) -> str:
        """Генерирует случайное среднее имя/отчество.

        .. note::
            Для корректной работы с отчествами рекомендуется инициализировать
            :class:`faker.Faker` с локалью ``'ru_RU'``, т.к. в других локалях
            среднее имя может отсутствовать или формироваться иначе.

        :return: Случайное среднее имя/отчество.
        :rtype: str
        """
        return self.faker.last_name()

    def estimate_time(self) -> str:
        """Формирует строку с оценкой времени в неделях.

        Генерирует случайное число от 1 до 10 и добавляет суффикс ``" weeks"``.

        :return: Строка вида ``"<число> weeks"``, например ``"3 weeks"``.
        :rtype: str
        """
        return f"{self.integer(1, 10)} weeks"

    def integer(self, start: int = 10, stop: int = 100) -> int:
        """Генерирует случайное целое число в заданном диапазоне.

        :param start: Нижняя граница диапазона (включительно).
        :type start: int
        :param stop: Верхняя граница диапазона (включительно).
        :type stop: int
        :return: Случайное целое число между start и stop.
        :rtype: int
        """
        return self.faker.random_int(start, stop)

    def max_score(self) -> int:
        """Генерирует случайный максимальный балл в диапазоне [50, 100].

        :return: Случайный балл от 50 до 100.
        :rtype: int
        """
        return self.integer(50, 100)

    def min_score(self) -> int:
        """Генерирует случайный минимальный балл в диапазоне [1, 30].

        :return: Случайный балл от 1 до 30.
        :rtype: int
        """
        return self.integer(1, 30)


fake = Fake(faker=Faker())
