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

- #### instance.get_name(self) -> str
Возвращает имя функции.

- #### instance.get_count(self) -> int
Возвращает количество вызовов функции.

- #### instance.get_avg_time(self) -> Optional[float]
Возвращает среднее время выполнения функции (по умолчанию в секундах).

- #### instance.get_avg_executions_per_unit_time(self) -> Optional[float]
Возвращает среднее количество выполнений функции в единицу времени (дефолт: в секунду)

- #### instance.get_all_metrics(self) -> Union[Tuple[str, int, Optional[float], Optional[float]], str, dict]
Возвращает кортеж, содержащий следующие параметры:
1) Имя функции;
2) Кол-во вызовов функции;
3) Среднее время работы функции;
4) Среднее кол-во выполнений функции в единицу времени (дефолт: в секундах).

- #### *classmethod* Statistic.get_all_instances_metrics(cls) -> Optional[Tuple]
Возвращает данные в выбранном пользователем формате (по умолчанию - tuple),
содержащий значения get_all_metrics для всех экземпляров класса (декорированных функций).

- #### *classmethod* Statistic.get_average_instances_metrics(cls) -> Union[Tuple[int, int, Optional[float], Optional[float]], str, dict]:
Возвращает среднюю статистику по всем функциям, а именно:
1) Общее количество вызванных уникальных функций;
2) Общее количество вызовов функций;
3) Среднее время работы всех функций;
4) Среднее время кол-во выполнений всех функций в единицу времени (дефолт: в секунду).
