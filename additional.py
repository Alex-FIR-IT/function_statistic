import datetime


class StatisticItem:

    def __set_name__(self, owner, name):
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.__name)

    def __set__(self, instance, value):
        setattr(instance, self.__name, value)


class Log:

    def __new__(cls, *args, **kwargs):
        raise AttributeError(f"Класс {cls.__name__} не поддерживает создание экземпляров")

    @staticmethod
    def dict_to_log(dct: dict, instance_class_name: str = "Statistic", sep: str = "; ", end: str = "\n") -> str:
        """Возвращает строку в формате Log"""

        instances = ["\t" + f"{sep}".join([f"{key}: {value}"
                     for key, value in func_info.items()])
                     for func_info in dct.values()]

        if not instances:
            instances.append('\tNone')

        start = f"[{datetime.datetime.now()}] {instance_class_name} INFO:"
        instances.insert(0, start)
        output = f"{end}".join(instances)

        return output
