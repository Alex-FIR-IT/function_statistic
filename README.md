# Библиотека для получения статистики по декорированным функциям/методам классов

## Общие положения

Данная библиотека содержит класс-декоратор (Statistic), предназначеннный для 
получения статистики работы декорированной функции. Данный класс содержит методы,
позволяющие получить общую информацию: 

- Общее количество вызванных уникальных функций;
- Общее количество вызовов функций;
- Среднее время работы всех функций;
- Среднее время кол-во выполнений всех функций в единицу времени (дефолт: в секунду).

А также локальную информацию по каждой функции:

- Имя функции;
- Количество ее вызовов;
- Минимальное время работы функции;
- Максимальное время работы функции;
- Последнее время работы функции;
- Среднее время работы функции (формат по дефолту: секунды);
- Среднее время выполнения функции в единицу времени (формат по дефолту: секунды).

Библиотека совместима с версией Python 3.8 и выше.

## Документация


### Быстрый старт

> Ваша программа:

    from function_statistic import Statistic
    
    
    @Statistic()         # Декоратор 
    def some_func(a, b): # Ваша функция
        res = 0
        for i in range(a + b):
            res += i
    
        return res
    
    
    class SomeClass:
    
        def __init__(self, info):
            self.info = info
    
        @Statistic()                 # Декоратор
        def some_class_method(self): # Ваш метод класса
            return f"{self.info}"
    
    
    for i in range(50):
        some_func(i, i)
    
    test = SomeClass("some information")
    for i in range(3):
        test.some_class_method()
    
> Получение статистики:

    Statistic.set_output_format("Log") # Доступные форматы: ("tuple", "str", "dict", "Log")
    Statistic.set_time_unit_format("second") # Доступные временные форматы: ("microsecond", "second", "minute", "hour")


    # Получить метрики для всех декорированных инстансов
    Statistic.get_instances_metrics()
    
    # Получить метрики для указанных декорированных инстансов
    Statistic.get_instances_metrics(("some_class_method",))
    
    # Получить обобщенную статистику по всем инстансам
    Statistic.get_average_instances_metrics()

> Вывод:

    [2023-10-08 16:22:42.765913] Statistic INFO:
        Name: some_func; Count: 50; Min_time: 4.76837158203125e-07; Max_time: 4.5299530029296875e-06; Last_time: 4.5299530029296875e-06; Avg_time: 2.231597900391e-06; Avg_exec_times_per_second: 190823.7
        Name: some_class_method; Count: 3; Min_time: 2.384185791015625e-07; Max_time: 4.76837158203125e-07; Last_time: 2.384185791015625e-07; Avg_time: 3.17891438802e-07; Avg_exec_times_per_second: 11683.3
    
    [2023-10-08 16:22:42.765973] Statistic INFO:
        Name: some_class_method; Count: 3; Min_time: 2.384185791015625e-07; Max_time: 4.76837158203125e-07; Last_time: 2.384185791015625e-07; Avg_time: 3.17891438802e-07; Avg_exec_times_per_second: 11683.3
    
    [2023-10-08 16:22:42.766008] Statistic INFO:
        Unique_count: 2; Count: 53; Avg_time: 1.2747446695965e-06; Avg_exec_times_per_second: 101253.5

### Доступные форматы для вывода

Декоратор Statistic имеет методы, позволяющие получить статистику по функциям в следующих форматах:

- tuple;
- str;
- dict;
- Log.
 
### Доступные временные форматы:

- microsecond (коэфициент - 10^6);
- second (коэфициент - 1);
- minute (коэфициент 1/60);
- hour (коэфициент 1/3600).

### Методы 

- #### *classmethod* Statistic.set_time_unit_format(cls, time_unit: str = 'second') -> None 
Позволяет установить временную единицу, которая используется при выводе 
статистических метрик.

Доступные временные форматы: 'microsecond', 'second', 'minute', 'hour'

Пример использования:

    Statistic.set_time_unit_format("second")
    Statistic.set_time_unit_format(time_unit="second")

- #### *classmethod* Statistic.get_time_unit_format(cls) -> str
Позволяет получить временною единицу, в которою переводятся все статистические метрики
(геттор метода set_time_unit_format). По умолчанию параметр принимает значение 'second'.

Пример использования:

    Statistic.get_time_unit_format()
    # Output: second

- #### *classmethod* Statistic.set_output_format(cls, output_format: str = 'tuple') -> None
Позволяет пользователю установить формат вывода статистических данных.
Имеет 1 параметр - output_format принимающий строку соответствующую доступному типу данных.

Доступные форматы: 'tuple', 'str', 'dict', 'Log'.

Пример использования:

    Statistic.set_output_format('tuple')
    Statistic.set_output_format(output_format='tuple')    

- #### *classmethod* Statistic.get_output_format(cls) -> str
Позволяет пользователю получить формат вывода статистических данных (геттор метода set_output_format).
По умолчанию, если не вызывался метод set_output_format, принимает значение 'tuple'.

Пример использования:

    Statistic.get_output_format()
    # Output: tuple

- #### *classmethod* Statistic.get_instances_metrics(cls, instances_names: tuple = ()) -> Optional[Tuple]
По умолчанию возвращает статистическую информацию по всем отдельным инстансам. 
Метод имеет 1 параметр instances_names (по умолчанию пустой кортеж), принимающий имена инстансов. 
Если в instances_names передан непустой кортеж, то возвращает статистическую информацию по переданым инстансам. 
Если в instances_names передан непустой кортеж, где все его значения принимают значения несущетсвующих инстансов, то
возвращает ложное с точки зрения Python выражение (кроме тех случаев, когда формат вывода принимает значение - 'Log')

Пример использования:
    
    Statistic.set_output_format(output_format='dict')
    Statistic.get_instances_metrics()
    # Output: {'some_func': {'Name': 'some_func', 'Count': 50, 'Min_time': 4.76837158203125e-07, 'Max_time': 6.198883056640625e-06, 'Last_time': 5.0067901611328125e-06, 'Avg_time': 2.865791320801e-06, 'Avg_exec_times_per_second': 152409.3}, 
    #          'some_class_method': {'Name': 'some_class_method', 'Count': 3, 'Min_time': 2.384185791015625e-07, 'Max_time': 4.76837158203125e-07, 'Last_time': 2.384185791015625e-07, 'Avg_time': 3.17891438802e-07, 'Avg_exec_times_per_second': 9327.6}}

    Statistic.get_instances_metrics(("some_func",))
    # Output: {'some_func': {'Name': 'some_func', 'Count': 50, 'Min_time': 4.76837158203125e-07, 'Max_time': 4.76837158203125e-06, 'Last_time': 4.76837158203125e-06, 'Avg_time': 2.460479736328e-06, 'Avg_exec_times_per_second': 168445.9}}

    Statistic.get_instances_metrics(("does_not_exist",))
    # Output: {}

- #### *classmethod* Statistic.get_average_instances_metrics(cls) -> Union[Tuple[int, int, Optional[float], Optional[float]], str, dict]:
Возвращает обобщенную статистику по всем инстансам.

Пример использования:

    Statistic.set_output_format(output_format='dict')
    Statistic.get_average_instances_metrics()
    # Output: {'General inforamtion': {'Unique_count': 2, 'Count': 53, 'Avg_time': 1.348654429118e-06, 'Avg_exec_times_per_second': 94493.6}}
