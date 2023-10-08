from time import time
from typing import Union, Tuple, Optional, Any
from functools import wraps
from additional import StatisticItem, Log

"""Данная библиотека содержит декоратор, предназначеннный для получения статистики работы декорированной функции"""


class Statistic:

    _instances = []
    _time_units = {"microsecond": 1_000_000, "second": 1, "minute": (1/60), "hour": (1/3600)}
    _active_time_unit = "second"
    _output_formats = {"tuple": tuple, "str": str, "dict": dict, "Log": Log}
    _active_output_format = tuple
    _KEYS = {"single_instance": ["Name", "Count", "Min_time", "Max_time", "Last_time", "Avg_time", "Avg_exec_times_per_{unit_format}"],
             "instances": ['Unique_count', 'Count', 'Avg_time', 'Avg_exec_times_per_{unit_format}']}

    @classmethod
    def _get_keys_from_KEYS(cls, key_option: str) -> Tuple:
        """Возвращает кортеж с отформатированной последней строкой из _KEYS"""

        keys = cls._KEYS.get(key_option).copy()
        keys[-1] = keys[-1].format(unit_format=cls.get_time_unit_format())
        return tuple(keys)

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
    def set_output_format(cls, output_format: str = "tuple") -> None:
        """Позволяет пользователю установить формат вывода статистических данных.
        Имеет 1 параметр, в который записывается класс необходимых данных.
        Возможные значения: tuple or str or dict"""

        cls._active_output_format = cls._output_formats.get(output_format)

    @classmethod
    def get_output_format(cls) -> Any:
        """Позволяет пользователю получить формат вывода статистических данных (_active_output_format).
        По умолчанию этот параметр - tuple"""

        return cls._active_output_format

    @classmethod
    def _convert_instances_to_output_format(cls, *instances, keys_for_values: Optional[Tuple] = None,
                                            sep="\n", output_format=None) -> Union[Tuple, str, dict]:
        """Возвращает статистические метрики в выбранном пользователе формате.
        Вывод определяет переменная _active_output_format (по умолчанию принимает значение tuple)"""

        if output_format is None:
            output_format = cls.get_output_format()

        if output_format is tuple:
            output = instances
        elif output_format is str:
            output = f"{sep}".join(str(value) for value in instances)
        elif output_format is dict:
            if not keys_for_values:
                keys_for_values = tuple(instance.__name__ for instance in instances)

            output = {keys_for_values[indx]: instance for indx, instance in enumerate(instances)}
        elif output_format is Log:
            if not keys_for_values:
                keys_for_values = cls._get_keys_from_KEYS("instances")

            dct = cls._convert_instances_to_output_format(*instances, output_format=dict,
                                                          keys_for_values=keys_for_values)
            output = Log.dict_to_log(dct=dct)
        else:
            types = cls._output_formats.keys()
            raise TypeError(f"Неподдерживаемый тип данных. Доступные типы {', '.join(types)}")
        return output

    @classmethod
    def _get_in_output_format(cls, *values, sep="; ", keys_for_values) -> Union[Tuple, str, dict]:
        """Возвращает статистические метрики в выбранном пользователе формате.
        Вывод определяет переменная _active_output_format (по умолчанию принимает значение tuple)"""

        output_format = cls.get_output_format()

        if output_format is tuple:
            output = values
        elif output_format is str:
            output = f"{sep}".join(str(value) for value in values)
        else:
            output = {keys_for_values[indx]: value for indx, value in enumerate(values)}

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
        self.count = self.max_time = self.avg_time = self.total_time = 0
        self.work_start = time()
        self.work_finish = self.min_time = self.last_time = None

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.count += 1

            work_start = time()
            func_res = func(*args, **kwargs)
            self.work_finish = time()

            self.last_time = self.work_finish - work_start
            self.total_time += self.last_time
            self._set_min_time(self.last_time)
            self._set_max_time(self.last_time)

            self.avg_time = self.total_time / self.count
            return func_res

        return wrapper

    def _set_min_time(self, work_time: float) -> None:
        """Если переданное значение work_time меньше, чем self.min_time, то тогда изменяется значение self.min_time"""

        try:
            if work_time < self.min_time:
                self.min_time = work_time
        except TypeError:
            self.min_time = work_time

    def _set_max_time(self, work_time: float) -> None:
        """Если переданное значение work_time больше, чем max_time, то тогда изменяется значение self.max_time"""

        if work_time > self.max_time:
            self.max_time = work_time

    def _get_last_time(self) -> float:
        """Возвращает последнее время, за которое выполнилась функция"""

        return self.last_time

    def _get_name(self) -> str:
        """Возвращает имя функции"""

        return self.func.__name__

    def _get_count(self) -> int:
        """Возвращает кол-во вызовов функции"""

        return self.count

    def _get_min_time(self) -> float:
        """Возвращает минимальное время работы функции"""

        return self.min_time

    def _get_max_time(self) -> float:
        """Возвращает максимальное время работы функции"""

        return self.max_time

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
        2) Минимальное время работы функции,
        3) Максимальное время работы функции,
        4) Послденее время работы функции,
        2) Среднее время работы функции,
        3) Среднее кол-во выполнений функции в единицу времени (дефолт: в секундах)"""

        output = self._get_in_output_format(self._get_name(),
                                            self._get_count(),
                                            self._get_min_time(),
                                            self._get_max_time(),
                                            self._get_last_time(),
                                            self._get_avg_time(),
                                            self._get_avg_executions_per_unit_time(),
                                            keys_for_values=self._get_keys_from_KEYS("single_instance"))

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
        keys_for_values = tuple(instance._get_name() for instance in instances)

        output = cls._convert_instances_to_output_format(*all_instances_metrics, keys_for_values=keys_for_values,
                                                         sep="\n") if all_instances_metrics else None

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

        output = cls._get_in_output_format(func_amount,
                                           count_sum,
                                           avg_time_all_instances,
                                           round(avg_time_per_minute__all_instances, 1),
                                           keys_for_values=cls._get_keys_from_KEYS("instances"))

        output = cls._convert_instances_to_output_format(output, keys_for_values=("General inforamtion",))

        return output
