import time
from collections import deque

"""Данная библиотека содержит декоратор, предназначеннный для получения статистки работы функции"""


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
    avg_time = StatisticItem()

    def __init__(self, func):
        self.func = func
        self.count = 0
        self.avg_time = deque()
        self.work_start = time.time()
        self.work_finish = None

    def __call__(self, *args, **kwargs):
        self.count += 1

        work_start = time.time()
        func_result = self.func(*args, **kwargs)
        self.work_finish = time.time()

        self.avg_time.append(self.work_finish - work_start)

        return func_result

    def get_name(self):
        return self.func.__name__

    def get_count(self):
        return self.count

    def get_avg_time(self):
        return sum(self.avg_time) / len(self.avg_time)

    def get_avg_time_per_minute(self):
        return self.get_count() / (self.work_finish - self.work_start)

    def get_statistic(self):
        """Возвращает кортеж, содержащий: Имя функции, Кол-во выполнений,
        Среднее время работы, а также Среднее кол-во выполнений функции в минуту"""

        return self.get_name(), self.get_count(), self.get_avg_time(), self.get_avg_time_per_minute()


