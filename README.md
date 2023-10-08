# Библиотека для получения статистики по декорированным функциям

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
- Среднее время работы функции;
- Среднее время выполнения функции в единицу времени (дефолт: в секундах).

Библиотека совместима с версией Python 3.8 и выше.

## Документация


### Быстрый старт

> Ваша программа:

    from function_statistic import Statistic
    
    
    @Statistic()         # Задекорирован
    def some_func(a, b): # Какая-то функция
        res = 0
        for i in range(a + b):
            res += i
    
        return res
    
    
    class SomeClass:
    
        def __init__(self, info):
            self.info = info
    
        @Statistic()                 # Задекорирован
        def some_class_method(self): # Какой-то метод класса
            return f"{self.info}"
    
    
    for i in range(50):
        some_func(i, i)
    
    test = SomeClass("some information")
    for i in range(3):
        test.some_class_method()
    
> Получение статистики:

    Statistic.set_output_format("Log")
    Statistic.set_time_unit_format("second")


    # Получить метрики для всех декорированных инстансов
    Statistic.get_instances_metrics()
    
    # Получить метрики для указанных декорированных инстансов
    Statistic.get_instances_metrics(("some_class_method",))
    
    # Получить обобщенную статистику по всем инстансам
    Statistic.get_average_instances_metrics()

> Вывод:

    [2023-10-08 16:10:18.156704] Statistic INFO:
        Name: some_func; Count: 50; Min_time: 7.152557373046875e-07; Max_time: 4.5299530029296875e-06; Last_time: 4.5299530029296875e-06; Avg_time: 2.412796020508e-06; Avg_exec_times_per_second: 179858.7
        Name: some_class_method; Count: 3; Min_time: 0.0; Max_time: 4.76837158203125e-07; Last_time: 0.0; Avg_time: 2.38418579102e-07; Avg_exec_times_per_second: 10951.2
    [2023-10-08 16:10:18.156771] Statistic INFO:
        some_class_method: {'Name': 'some_class_method', 'Count': 3, 'Min_time': 0.0, 'Max_time': 4.76837158203125e-07, 'Last_time': 0.0, 'Avg_time': 2.38418579102e-07, 'Avg_exec_times_per_second': 10951.2}
    [2023-10-08 16:10:18.156810] Statistic INFO:
        General inforamtion: {'Unique_count': 2, 'Count': 53, 'Avg_time': 1.325607299805e-06, 'Avg_exec_times_per_second': 95405.0}

### Доступные форматы для вывода

Декоратор Statistic имеет методы, позволяющие получить статистику по функциям в следующих форматах:

- tuple;
- str;
- dict.
 
### Доступные временные единицы измерения:

- Microsecond (коэфициент - 10^6);
- Second (коэфициент - 1);
- Minute (коэфициент 1/60);
- Hour (коэфициент 1/3600).

### Методы 

- #### *classmethod* Statistic.set_time_unit_format(cls, time_unit: str = 'second') -> None 
Позволяет установить временную единицу, которая используется при выводе 
статистических метрик в таких методах, как:
1) get_avg_time
2) get_avg_executions_per_unit_time
3) get_all_metrics
4) get_all_instances_metrics
5) get_average_instances_metrics

Возможные значения: 'microsecond' or 'second' or 'minute' or 'hour'
- #### *classmethod* Statistic.get_time_unit_format(cls) -> str
Позволяет получить временною единицу, в которою переводятся все статистические метрики
(по умолчанию принимает значение - second)

- #### *classmethod* Statistic.set_output_format(cls, output_format=tuple) -> None
Позволяет пользователю установить формат вывода статистических данных.
Имеет 1 параметр, в который записывается класс необходимых данных.

Возможные значения: tuple or str or dict.

- #### *classmethod* Statistic.get_output_format(cls) -> str
Позволяет пользователю получить формат вывода статистических данных (_active_output_format).
По умолчанию этот параметр - tuple.

- #### instance._get_name(self) -> str
Возвращает имя функции.

- #### instance._get_count(self) -> int
Возвращает количество вызовов функции.

- #### instance._get_avg_time(self) -> Optional[float]
Возвращает среднее время выполнения функции (по умолчанию в секундах).

- #### instance._get_avg_executions_per_unit_time(self) -> Optional[float]
Возвращает среднее количество выполнений функции в единицу времени (дефолт: в секунду)

- #### instance._get_all_metrics(self) -> Union[Tuple[str, int, Optional[float], Optional[float]], str, dict]
Возвращает кортеж, содержащий следующие параметры:
1) Имя функции;
2) Кол-во вызовов функции;
3) Среднее время работы функции;
4) Среднее кол-во выполнений функции в единицу времени (дефолт: в секундах).

- #### *classmethod* Statistic.get_instances_metrics(cls, instances_names: tuple = ()) -> Optional[Tuple]
Принимает кортеж, состоящий из имен декорированных функций.
Возвращает для переданных декорированных функций\методов в выбранном пользователем формате (по умолчанию tuple)
слудующие данные (по умолчанию возвращает информацию по все инстансам):
1) Имя функции,
2) Кол-во вызовов функции,
3) Среднее время работы функции,
4) Среднее кол-во выполнений функции в единицу времени (дефолт: в секундах)

- #### *classmethod* Statistic.get_average_instances_metrics(cls) -> Union[Tuple[int, int, Optional[float], Optional[float]], str, dict]:
Возвращает среднюю статистику по всем функциям, а именно:
1) Общее количество вызванных уникальных функций;
2) Общее количество вызовов функций;
3) Среднее время работы всех функций;
4) Среднее время кол-во выполнений всех функций в единицу времени (дефолт: в секунду).
