from time import time
from collections import deque

"""Данная библиотека содержит декоратор, предназначеннный для получения статистики работы декорированной функции"""


class StatisticItem:

    def __set_name__(self, owner, name):
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.__name)

    def __set__(self, instance, value):
        setattr(instance, self.__name, value)


class Statistic:

    count = StatisticItem()
    func = StatisticItem()
    avg_time = StatisticItem()
    work_start = StatisticItem()
    work_finish = StatisticItem()
    is_on = StatisticItem()

    def __init__(self, func):
        self.func = func
        self.count = 0
        self.avg_time = deque()
        self.work_start = time()
        self.work_finish = None
        self.is_on = False

    def __call__(self, *args, **kwargs):
        if self.is_on:
            return self.__is_on_call(args, kwargs)

        return self.func

    def __is_on_call(self, *args, **kwargs):
        self.count += 1

        work_start = time()
        func_result = self.func(*args, **kwargs)
        self.work_finish = time()

        self.avg_time.append(self.work_finish - work_start)

        return func_result


    def get_name(self) -> str:
        """Возвращает имя функции"""

        return self.func.__name__

    def get_count(self) -> int:
        """Возвращает кол-во вызовов функции"""

        return self.count

    def get_avg_time(self) -> float:
        """Возвращает среднее время выполнения функции (в секундах)"""

        count = self.get_count()

        if count:
            return sum(self.avg_time) / count

        raise ZeroDivisionError("Невозможно вычислить среднее время работы функции, т.к она ни разу не вызывалась")

    def get_avg_time_per_minute(self) -> float:
        """Возвращает среднее количество выполнений функции в минуту"""

        work_finish = self.work_finish

        if work_finish:
            return round(60 * self.count / (self.work_finish - self.work_start), 4)

        raise ArithmeticError("Невозможно вычислить среднее время работы функции в минуту, "
                              "т.к она ни разу не вызывалась")

    def get_all_metrics(self) -> tuple:
        """Возвращает кортеж, содержащий: Имя функции, Кол-во вызовов функции,
        Среднее время работы функции, а также Среднее кол-во выполнений функции в минуту"""

        return self.get_name(), self.get_count(), self.get_avg_time(), self.get_avg_time_per_minute()
