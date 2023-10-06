from time import time
from typing import Union, Tuple, Optional
from functools import wraps

"""Данная библиотека содержит декоратор, предназначеннный для получения статистики работы декорированной функции"""


class StatisticItem:

    def __set_name__(self, owner, name):
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.__name)

    def __set__(self, instance, value):
        setattr(instance, self.__name, value)


class Statistic:

    _instances = []
    _time_units = {"microsecond": 1_000_000, "second": 1, "minute":  1/60, "hour": 1/3600}
    _active_time_unit = "second"
    _output_formats = {tuple: "tuple", str: "str", dict: "dict"}
    _active_output_format = "tuple"

    @classmethod
    def set_time_unit_format(cls, time_unit: str = 'second') -> None:
        """Позволяет установить временную единицу, которая используется при выводе статистических метрик.
        Возможные значения: 'microsecond' or 'second' or 'minute' or 'hour'"""

        cls._active_time_unit = cls._is_in_permitted_values(time_unit, cls._time_units)

    @classmethod
    def get_time_unit_format(cls) -> str:
        """Позволяет получить временною единицу, в которою переводятся все статистические метрики
        (по умолчанию принимает значение - second)"""

        return cls._active_time_unit

    @classmethod
    def _is_in_permitted_values(cls, time_unit: str, permitted_value: dict) -> str:
        """Проверяет, что значение time_unit находится в permitted_value. Используется в set_time_unit_format"""

        if time_unit not in permitted_value:
            message = f"Введенного вами формата не существует, " \
                      f"доступные форматы: {', '.join(x for x in cls._time_units.keys())}"
            raise KeyError(message)

        return time_unit

    @classmethod
    def _get_time_unit_value(cls) -> Union[int, float]:
        """Позволяет получить числовой коэфициент,
        который используется при пересчете статистических метрик в определенный временной формат
        (например для перевода среднего времени выполнения функции (_get_avg_time) из секунд в минуты и т.д.)"""

        return cls._time_units.get(cls.get_time_unit_format())

    @classmethod
    def set_output_format(cls, output_format=tuple) -> None:
        """Позволяет пользователю установить формат вывода статистических данных.
        Имеет 1 параметр, в который записывается класс необходимых данных.
        Возможные значения: tuple or str or dict"""

        cls._active_output_format = cls._output_formats.get(output_format)

    @classmethod
    def get_output_format(cls) -> str:
        """Позволяет пользователю получить формат вывода статистических данных (_active_output_format).
        По умолчанию этот параметр - tuple"""

        return cls._active_output_format

    @classmethod
    def _make_keys(cls, instances, keys_for_values=None) -> iter:
        """Возвращает итератор из значений,
        которые будут являться ключами при выборе словаря как типа вывода статистических данных """

        try:
            if instances is None:
                raise TypeError()

            keys = (x.func.__name__ for x in instances)
        except TypeError:
            if keys_for_values:
                keys = iter(keys_for_values)
            else:
                keys = iter(("Name", "Count", "Average_time", f"Avg_exec_times_per_{cls.get_time_unit_format()}"))

        return keys

    @classmethod
    def _convert_to_output_format(cls, *args, instances=None, sep=",", keys_for_values=None) -> Union[Tuple, str, dict]:
        """Возвращает статистические метрики в выбранном пользователе формате.
        Вывод определяет переменная _active_output_format (по умолчанию принимает значение tuple)"""

        output_format = cls.get_output_format()

        if output_format == "tuple":
            output = args
        elif output_format == "str":
            output = f"{sep} ".join(str(value) for value in args)
        elif output_format == "dict":
            keys = cls._make_keys(instances, keys_for_values=keys_for_values)
            output = {next(keys): value for value in args}
        else:
            types = cls._output_formats.values()
            raise TypeError(f"Неподдерживаемый тип данных. Доступные типы {', '.join(types)}")
        return output

    count = StatisticItem()
    func = StatisticItem()
    avg_time = StatisticItem()
    work_start = StatisticItem()
    work_finish = StatisticItem()
    total_time = StatisticItem()

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        cls._instances.append(instance)

        return instance

    def __init__(self):
        self.count = self.avg_time = self.total_time = 0
        self.work_start = time()
        self.work_finish = None

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.count += 1

            work_start = time()
            func_res = func(*args, **kwargs)
            self.work_finish = time()
            self.total_time += self.work_finish - work_start

            self.avg_time = self.total_time / self.count
            return func_res

        return wrapper

    def _get_name(self) -> str:
        """Возвращает имя функции"""

        return self.func.__name__

    def _get_count(self) -> int:
        """Возвращает кол-во вызовов функции"""

        return self.count

    def _get_avg_time(self) -> Optional[float]:
        """Возвращает среднее время выполнения функции (дефолт: в секундах)"""

        count = self._get_count()
        time_format = self._get_time_unit_value()

        if count:
            return round(self.avg_time * time_format, 18)

    def _get_avg_executions_per_unit_time(self) -> Optional[float]:
        """Возвращает среднее количество выполнений функции в единицу времени (дефолт: в секунду)"""

        work_finish = self.work_finish
        time_format = self._get_time_unit_value()

        if work_finish:
            return round(self.count / ((self.work_finish - self.work_start) * time_format), 1)

    def _get_all_metrics(self) -> Union[Tuple[str, int, Optional[float], Optional[float]], str, dict]:
        """Возвращает кортеж, содержащий:
        0) Имя функции,
        1) Кол-во вызовов функции,
        2) Среднее время работы функции,
        3) Среднее кол-во выполнений функции в единицу времени (дефолт: в секундах)"""

        output = self._convert_to_output_format(self._get_name(),
                                                self._get_count(),
                                                self._get_avg_time(),
                                                self._get_avg_executions_per_unit_time())

        return output

    @classmethod
    def get_instances_metrics(cls, instances_names: tuple = ()) -> Optional[Tuple]:
        """Принимает кортеж, состоящий из имен декорированных функций.
        Возвращает для переданных декорированных функций\методов в выбранном пользователем формате (по умолчанию tuple)
        слудующие данные (по умолчанию возвращает информацию по все инстансам):
        0) Имя функции,
        1) Кол-во вызовов функции,
        2) Среднее время работы функции,
        3) Среднее кол-во выполнений функции в единицу времени (дефолт: в секундах)"""

        if instances_names:
            instances = tuple(instance for instance in cls._instances
                              if instance._get_name() in instances_names)
        else:
            instances = tuple(filter(cls._get_count, cls._instances))

        all_instances_metrics = tuple(instance._get_all_metrics() for instance in instances)
        output = cls._convert_to_output_format(*all_instances_metrics,
                                               instances=instances, sep=";") if all_instances_metrics else None

        return output

    @classmethod
    def get_average_instances_metrics(cls) -> Union[Tuple[int, int, Optional[float], Optional[float]], str, dict]:
        """Возвращает среднюю статистику по всем функциям, а именно:
         0) Общее количество уникальных вызовов,
         1) Общее количество вызовов функций,
         2) Среднее время работы всех функций,
         3) Среднее кол-во выполнений всех функций в единицу времени (дефолт: в секунду)"""

        instances = tuple(filter(cls._get_count, cls._instances))

        func_amount = len(instances)
        count_sum = sum(x._get_count() for x in instances)
        avg_time_all_instances = avg_time_per_minute__all_instances = None

        if func_amount:
            avg_time_all_instances = sum(map(cls._get_avg_time, instances)) / func_amount
            avg_time_per_minute__all_instances = sum(map(cls._get_avg_executions_per_unit_time, instances)) / func_amount

        keys_for_values = ('Unique_count', 'Count', 'Average_time', f'Avg_exec_times_per_{cls.get_time_unit_format()}')
        output = cls._convert_to_output_format(func_amount,
                                               count_sum,
                                               avg_time_all_instances,
                                               round(avg_time_per_minute__all_instances, 1),
                                               keys_for_values=keys_for_values)

        return output
