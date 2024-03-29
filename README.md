# Папка 01: Работа с файлами и предсказание настроения

## Задача 1: Фильтр файлов (01/file_filter.py)

### Описание
Модуль `file_filter.py` предоставляет функции для фильтрации текстовых данных из файлов и строк.

### Функции

1. **gen(f_obj, lst)**
   - Генератор, фильтрующий строки файла по списку слов.
   - Принимает файловый объект `f_obj` и список слов `lst`.
   - Возвращает строки файла, содержащие хотя бы одно слово из списка.
   - Автоматически закрывает файл после завершения.

2. **from_str_to_file_obj(st)**
   - Конвертирует строку `st` в файловый объект.

### Тестирование (test_file_filter.py)
Модуль `test_file_filter.py` содержит юнит-тесты для функции `gen` в файле `file_filter.py`.

## Задача 2: Предсказание настроения (01/predicator.py)

### Описание
Модуль `predicator.py` содержит функции для предсказания настроения сообщений.

### Классы и функции

1. **SomeModel**
   - Простая модель, предсказывающая случайное значение от 0.0 до 1.0.

2. **predict_message_mood(message, model, bad_thresholds=0.3, good_thresholds=0.8)**
   - Функция, предсказывающая настроение сообщения на основе модели.
   - Возвращает "неуд", "норм" или "отл" в зависимости от предсказания модели.

### Тестирование (test_predicator.py)
Модуль `test_predicator.py` содержит юнит-тесты для функции `predict_message_mood` в файле `predicator.py`.

# Папка 02: Парсер JSON и Декоратор для измерения времени выполнения функции

## Задача 1: Парсер JSON (02/json_parser_utils.py)

Модуль `json_parser_utils.py` предоставляет утилитарные функции для разбора JSON-данных и поиска ключевых слов в полях JSON.

### Описание
Этот модуль предназначен для обработки JSON-данных и поиска ключевых слов в определенных полях. Он предоставляет функцию `parse_json`, которая принимает JSON-строку, список обязательных полей, список ключевых слов и функцию обратного вызова для каждого найденного ключевого слова. Модуль также включает вспомогательную функцию `func`, предназначенную для обработки результатов поиска.

### Использование
```python
import json_parser_utils

# Пример использования
json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
required_fields = ["key1", "key2"]
keywords = ["word2", "word3"]

def keyword_callback(required_field, keyword):
    print(f"Keyword found in '{required_field}': {keyword}")

json_parser_utils.parse_json(json_str, required_fields, keywords, keyword_callback)
```

## Задача 2: Декоратор измерения времени выполнения (02/time_measurement_decorators.py)

Модуль `time_measurement_decorators.py` предоставляет декоратор для измерения и отчета о среднем времени выполнения декорированной функции за несколько вызовов.

### Описание
Этот модуль предназначен для измерения среднего времени выполнения функции за несколько вызовов с использованием декоратора. Он включает функцию-декоратор `average_time_deco`, принимающую параметр `k` - количество последних вызовов для расчета среднего времени. Модуль также содержит пример использования декоратора с функцией `my_function`.

### Использование
```python
import time_measurement_decorators

# Пример использования
@time_measurement_decorators.average_time_deco(5)
def my_function(arg):
    res = arg + " White! You're goddamn right"
    time.sleep(1)
    return res

# Вызов декорированной функции
result = my_function("Walter")
print(result)
```

# Папка 03: Кастомный список для поэлементного сложения, вычитания, сравнения и кастомного строкового представления.

## Задача 1: CustomList (03/metaclass_changer.py)

## Описание

Модуль 'metaclass_changer.py' определяет класс `CustomList`, являющийся пользовательским расширением встроенного класса `list` в Python. Этот класс предоставляет дополнительные возможности для поэлементного сложения, вычитания, сравнения и кастомного строкового представления.

```python
class CustomList(list):
    # Код класса
    ...
```

### Функциональность
Сложение (__add__): Реализует операцию сложения для экземпляров CustomList, позволяя складывать их друг с другом или с обычными списками. Результатом является новый кастомный список.

Сложение (справа) (__radd__): Реализует операцию сложения справа, позволяя складывать экземпляры CustomList с обычными списками.

Вычитание (__sub__): Реализует операцию вычитания для экземпляров CustomList, позволяя вычитать их друг из друга или из обычных списков. Результатом является новый кастомный список.

Вычитание (справа) (__rsub__): Реализует операцию вычитания справа, позволяя вычитать экземпляры CustomList из обычных списков.

Сравнение (__eq__, __ne__, __le__, __ge__, __gt__, __lt__): Реализуют операции сравнения, сравнивая суммы элементов экземпляров CustomList. Сравнение с обычными списками не предусмотрено.

Строковое представление (__str__): Переопределенный метод для красивого вывода элементов списка и их суммы.

Статический метод (sum_centr): Вычисляет сумму элементов двух списков.

Пример использования
```python
Copy code
custom_list1 = CustomList([5, 1, 3, 7])
custom_list2 = CustomList([1, 2, 7])

result = custom_list1 + custom_list2  # CustomList([6, 3, 10, 7])
print(result)
# Вывод: CustomList([6, 3, 10, 7]) сумма элементов = 26

custom_list3 = CustomList([1])
result2 = custom_list3 + [2, 5]  # CustomList([3, 5])
print(result2)
# Вывод: CustomList([3, 5]) сумма элементов = 8
```
### Замечание
Списки всегда считаются числовыми для проведения арифметических операций.

# Папка 04: Дескрипторы и метаклассы (03/metaclass_changer.py)

## Задача 1: Метакласс, который в начале названий всех атрибутов и методов, кроме магических, добавляет префикс "custom_"

## Описание
Модуль 'metaclass_changer.py' предоставляет метакласс CustomMeta, предназначенный для модификации имен атрибутов и методов внутри класса. Метакласс добавляет префикс "custom_" к началу всех атрибутов и методов (за исключением магических) как в самом классе, так и в его экземплярах. Метакласс также обрабатывает атрибуты, добавленные динамически после создания экземпляра класса.
Пример использования


## Задача 2: Дескрипторы с проверками типов и значений данных

## Описание
Модуль 'movie_service_descs.py' предоставляет три дескриптора для области интереса - фильмов. Дескрипторы предназначены для проверки и установки значений атрибутов класса MovieService, представляющего информацию о фильме.

Дескрипторы
1. MovieName
Дескриптор для управления именем фильма. Проверяет, что значение является строкой, содержит только английские буквы и не является пустой строкой.

2. RatingDescr
Дескриптор для управления рейтингом фильма. Проверяет, что значение является числом (целым или с плавающей запятой) и не отрицательным.

3. MoviePlotDescr
Дескриптор для управления описанием сюжета фильма. Проверяет, что значение является строкой, содержит не более 50 слов и 250 символов.

4. MovieCastDescr
Дескриптор для управления списком актеров в фильме. Проверяет, что значение является словарем и не содержит более 10 актеров.

# Папка 05: LRU-cache (avg difficulty - O1)

## my_lru_cache.py

Этот модуль представляет собой реализацию LRU кэша.

Методы LRUCache
- __init__(self, limit=42)
Создает экземпляр LRUCache с указанным лимитом (по умолчанию - 42).

- get(self, key)
Извлекает значение, связанное с заданным ключом, из кэша. Если ключ присутствует, он отмечается как недавно использованный.

- set(self, key, value)
Устанавливает пару ключ-значение в кэш. Если ключ уже присутствует, значение обновляется, и ключ отмечается как недавно использованный. Если кэш заполнен, наименее недавно использованный элемент удаляется.

- __del(self)
Приватный метод, используемый внутренне для удаления наименее недавно использованного элемента, когда лимит кэша достигнут.

### Ограничения
Значение, связанное с ключом, не может быть None.
Лимит должен быть положительным целым числом.

# Папка 06: Клиент-серверное приложение для обкачки набора урлов с ограничением нагрузки

## client.py

Этот модуль представляет собой простой TCP-клиент, способный отправлять данные на сервер и принимать ответы в многопоточной среде. Клиент использует библиотеку 'socket' для установки соединения с сервером и библиотеки 'concurrent.futures' для реализации пула потоков.

Описание
- TCPClient: Основной класс клиента, инициализирует соединение с сервером, создает потоки для чтения файла и отправки сообщений, а также ожидает ответы от сервера.

- __init__(self, ip, port, quantity_th, filename): Конструктор класса, инициализирует параметры клиента и устанавливает соединение с сервером.

- sender_msg(self, msg): Метод для отправки сообщения на сервер.

- file_reader(self): Метод для чтения данных из файла и добавления их в очередь для отправки.

- extractor(self): Метод для извлечения сообщений из очереди и отправки их на сервер.

- worker(self): Метод, запускающий пул потоков для обработки данных из очереди.

- receiver(self): Метод для приема данных от сервера и их вывода на экран.

- __main__: Блок кода, выполняемый при запуске скрипта. Создает экземпляр класса TCPClient, используя аргументы командной строки.

## server.py

Этот проект представляет собой простой TCP-сервер, способный принимать URL-адреса от клиентов, загружать содержимое веб-страниц и анализировать наиболее популярные слова на страницах с использованием нескольких рабочих потоков. Сервер использует библиотеки socket, selectors, threading, concurrent.futures, queue для организации многопоточности и requests, BeautifulSoup для взаимодействия с веб-страницами.

Описание
- TCPServer: Основной класс сервера, управляющий обработкой запросов от клиентов.

- __init__(self, n_workers, k_words): Конструктор класса, инициализирует параметры сервера и устанавливает соединение.

- master(self): Метод для обработки входящих соединений и управления обработкой запросов от клиентов.

- workers(self): Метод для запуска пула потоков для обработки URL-адресов.

- url_parser(self): Метод для загрузки веб-страницы, извлечения текста и анализа популярных слов.

- words_counter(self, text, url, client_socket): Метод для подсчета наиболее популярных слов в тексте.

- send_msg(self, client_socket, msg): Метод для отправки сообщения клиенту.

- __main__: Блок кода, выполняемый при запуске скрипта. Создает экземпляр класса TCPServer, используя аргументы командной строки.

# Папка 07: Скрипт для асинхронной обкачки урлов

## Описание

Простой скрипт для асинхронной обработки URL-адресов из текстового файла на Python, asyncio и aiohttp.

Скрипт fetcher.py предоставляет возможность асинхронной обработки URL-адресов с использованием нескольких воркеров. Каждый воркер выполняет запрос GET к URL-адресу и выводит статус ответа или информацию об ошибке.

- worker(que, pos): Функция воркера. Получает URL из очереди, вызывает функцию fetch и выводит результат обработки.

- fetch(url): Функция для выполнения асинхронного запроса GET к URL-адресу с использованием библиотеки aiohttp. Возвращает статус ответа или информацию об ошибке.

- main(workers_num): Основная функция, создающая асинхронные задачи для воркеров, читающая URL-адреса из файла и добавляющая их в асинхронную очередь.

#### Аргументы командной строки

-w, --workers: Количество асинхронных воркеров. По умолчанию 10.

#### Ограничения

Скрипт предполагает, что файл url_lib.txt существует и содержит корректные URL-адреса.
Ответы сервера выводятся на экран, но могут быть легко адаптированы для дальнейшей обработки или сохранения в файл.


# Папка 08: Память, Профилирование

## comparator.py

Скрипт предназначен для измерения производительности различных типов классов в Python и их воздействия на время создания экземпляров, чтения и записи атрибутов. В эксперименте используются три типа классов:

- Обычные атрибуты (MyClass):

   - Экземпляры создаются с использованием обычных атрибутов.

- Слоты (MySlottedClass):

   - Экземпляры создаются с использованием слотов для определения атрибутов.
  
- Атрибуты WeakRef (MyWeakRefClass):

   - Экземпляры создаются с использованием слабых ссылок на атрибуты.
  
#### Измерения времени

- Время создания экземпляров:

   - Измеряется время, затраченное на создание указанного количества экземпляров каждого типа класса.

- Время чтения атрибутов:

   - Измеряется время, затраченное на выполнение операции чтения атрибутов указанное количество раз для каждого типа класса.
  
- Время записи атрибутов:

   - Измеряется время, затраченное на выполнение операции записи атрибутов указанное количество раз для каждого типа класса.

#### Результаты

## deco_profiler.py

Результаты измерений выводятся в консоль и предоставляют информацию о том, как различные подходы к определению атрибутов классов могут влиять на производительность в различных сценариях использования.

Этот скрипт предоставляет простой механизм профилирования для функций Python с использованием модуля cProfile. Два различных метода применения профилирования включены: через класс Profiler и с использованием декоратора profile_deco.

### Инструкции по использованию

Profiler класс:

Инстанцируйте класс Profiler и передайте в него функцию, которую вы хотите профилировать.
Вызовите этот экземпляр как функцию с аргументами, переданными в оригинальную функцию.
Для просмотра статистики вызовите метод print_stat() у экземпляра Profiler.

profile_deco декоратор:

Просто добавьте @profile_deco перед определением функции, которую вы хотите профилировать.
Декорированная функция будет автоматически профилироваться при каждом вызове.
Для просмотра статистики вызовите метод print_stat() у декорированной функции.

# Папка 09: Логирование для LRUCache

Логирование включает в себя три уровня, такие как DEBUG, INFO, и WARNING. Дополнительно, логирование может быть настроено для вывода в стандартный поток вывода (stdout) и применения кастомного фильтра.

Конфигурация логирования:

Скрипт запускается с параметрами -s для логирования в stdout и -f для применения кастомного фильтра.

### Операции с кэшем:

- Создайте экземпляр LRUCache.
- Выполняйте операции get и set для управления содержимым кэша.
- Результаты операций будут залогированы согласно уровням логирования.

### Результаты
Логи операций будут записаны в файл cache.log. Стандартный вывод также будет использован, если указан параметр -s. Кастомный фильтр (-f) будет применен к логам.

# Папка 10: Библиотека для парсинга и сериализации json (C-extension)

## Описание

Этот модуль предоставляет две функции для преобразования данных между строковым форматом и объектами Python: loads и dumps. Реализация подобна формату JSON, но с определенными отличиями. Модуль написан на языке C и доступен для использования в Python.

Функции
loads
python
Copy code
cjson.loads(string: str) -> dict

Принимает строку в формате CJSON и возвращает эквивалентный словарь Python.
```python
dumps
python
Copy code
cjson.dumps(data: dict) -> str
```

Принимает словарь Python и возвращает его строковое представление в формате CJSON.


```python
import cjson

# Преобразование строки в словарь
data = cjson.loads("{'key': 'value', 'num': 42}")

# Преобразование словаря в строку
string_data = cjson.dumps({'key': 'value', 'num': 42})
```
