from functools import update_wrapper


"""Данная библиотека содержит декораторы, предназначеннные для получения статистки работы функции"""


class StatisticItem:

    def __set_name__(self, owner, name):
        self.__name = f"_{owner.__name__}__{name}"

    def __set__(self, instance, value):
        setattr(instance, self.__name, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.__name)


class Statistic:

    count = StatisticItem()
    func = StatisticItem()

    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

    def get_name(self):
        return self.func.__name__

    def get_count(self):
        return self.count

    def get_statistic(self):
        """Возвращает кортеж, содержащий: Имя функции, Кол-во выполнений,
        Среднее время работы, а также Среднее кол-во выполнений функции в минуту"""

        return self.get_name(), self.get_count()

