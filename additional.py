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
    def dict_to_log(dct: dict, all_instances: bool = True, instance_class_name: str = "Statistic", sep = "; ", end = "\n"):
        date_time = datetime.datetime.now()
        start = f"[{date_time}] {instance_class_name} INFO:"
        # instances = [f"\t[{key}: {value}]"
        #              for func_info in dct.values()
        #              for key, value in func_info.items()]

        if len(dct) == 1:
            dct = {1: dct}

        instances = ["\t" + "; ".join([f"{key}: {value}"
                     for key, value in func_info.items()])
                     for func_info in dct.values()]


        instances.insert(0, start)
        output = f"{end}".join(instances)

        return output