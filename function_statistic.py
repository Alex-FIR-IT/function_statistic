from time import time

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
        cls._active_time_unit = cls._is_in_permitted_values(time_unit, cls._time_units)

    @classmethod
    def get_time_unit_format(cls) -> str:
        return cls._active_time_unit

    @classmethod
    def _is_in_permitted_values(cls, time_format: any, permitted_value: dict) -> any:
        if time_format not in permitted_value:
            message = f"Введенного вами формата не существует, " \
                      f"доступные форматы: {', '.join(x for x in cls._time_units.keys())}"
            raise KeyError(message)

        return time_format

    @classmethod
    def _get_time_unit_value(cls) -> int | float:
        return cls._time_units.get(cls.get_time_unit_format())

    @classmethod
    def set_output_format(cls, output_format=tuple) -> None:
        cls._active_output_format = cls._output_formats.get(output_format)

    @classmethod
    def get_output_format(cls) -> any:
        return cls._active_output_format

    @classmethod
    def _make_keys(cls, instances, keys_for_values=None):
        try:
            if instances is None:
                raise TypeError()

            keys = (x.func.__name__ for x in instances)
        except TypeError:
            if keys_for_values:
                keys = iter(keys_for_values)
            else:
                keys = iter(("Name", "Count", "Average_time", f"Average_time_per_{cls.get_time_unit_format()}"))

        return keys

    @classmethod
    def _convert_to_output_format(cls, *args, instances=None, sep=",", keys_for_values=None):
        output_format = cls.get_output_format()

        match output_format:
            case "tuple":
                output = args
            case "str":
                output = f"{sep} ".join(str(value) for value in args)
            case "dict":
                keys = cls._make_keys(instances, keys_for_values=keys_for_values)
                output = {next(keys): value for value in args}
            case _:
                types = cls._output_formats.values()
                raise TypeError(f"Неподдерживаемый тип данных. Доступные типы {', '.join(types)}")
        return output

    count = StatisticItem()
    func = StatisticItem()
    avg_time = StatisticItem()
    work_start = StatisticItem()
    work_finish = StatisticItem()

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        cls._instances.append(instance)

        return instance

    def __init__(self, func):
        self.func = func
        self.count = self.avg_time = 0
        self.work_start = time()
        self.work_finish = None

    def __call__(self, *args, **kwargs):
        self.count += 1

        work_start = time()
        func_result = self.func(*args, **kwargs)
        self.work_finish = time()

        self.avg_time = (self.avg_time + self.work_finish - work_start) / self.count

        return func_result

    def get_name(self) -> str:
        """Возвращает имя функции"""

        return self.func.__name__

    def get_count(self) -> int:
        """Возвращает кол-во вызовов функции"""

        return self.count

    def get_avg_time(self) -> float | None:
        """Возвращает среднее время выполнения функции (дефолт: в секундах)"""

        count = self.get_count()
        time_format = self._get_time_unit_value()

        if count:
            return round(self.avg_time * time_format, 18)

    def get_avg_time_per_unit_time(self) -> float | None:
        """Возвращает среднее количество выполнений функции в единицу времени (дефолт: в секунду)"""

        work_finish = self.work_finish
        time_format = self._get_time_unit_value()

        if work_finish:
            return round(self.count / ((self.work_finish - self.work_start) * time_format), 1)

    def get_all_metrics(self) -> tuple[str, int, float | None, float | None] | str | dict:
        """Возвращает кортеж, содержащий:
        Имя функции,
        Кол-во вызовов функции,
        Среднее время работы функции,
        Среднее кол-во выполнений функции в единицу времени (дефолт: в секундах)"""
        output = self._convert_to_output_format(self.get_name(),
                                                self.get_count(),
                                                self.get_avg_time(),
                                                self.get_avg_time_per_unit_time())

        return output

    @classmethod
    def get_all_instances_metrics(cls) -> tuple | None:
        """Возвращает кортеж, содержащий значения get_all_metrics для всех экземпляров класса"""

        instances = tuple(filter(cls.get_count, cls._instances))
        all_instances_metrics = tuple(instance.get_all_metrics() for instance in instances)
        output = cls._convert_to_output_format(*all_instances_metrics,
                                               instances=instances, sep=";") if all_instances_metrics else None

        return output

    @classmethod
    def get_average_instances_metrics(cls) -> tuple[int, int, float | None, float | None] | str | dict:
        """Возвращает среднюю статистику по всем функциям, а именно:
         Общее количество вызванных уникальных функций,
         Общее количество вызовов функций,
         Среднее время работы всех функций,
         Среднее время кол-во выполнений всех функций в единицу времени (дефолт: в секунду)"""

        instances = tuple(filter(cls.get_count, cls._instances))

        func_amount = len(instances)
        count_sum = sum(x.get_count() for x in instances)
        avg_time_all_instances = avg_time_per_minute__all_instances = None

        if func_amount:
            avg_time_all_instances = sum(map(cls.get_avg_time, instances)) / func_amount
            avg_time_per_minute__all_instances = sum(map(cls.get_avg_time_per_unit_time, instances)) / func_amount

        keys_for_values = ('Unique_count', 'Count', 'Average_time', f'Average_time_per_{cls.get_time_unit_format()}')
        output = cls._convert_to_output_format(func_amount,
                                               count_sum,
                                               avg_time_all_instances,
                                               round(avg_time_per_minute__all_instances, 1),
                                               keys_for_values=keys_for_values)

        return output
