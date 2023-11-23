import logging
import argparse


class LRUCache():

    def __init__(self, limit=42):
        self.__cache_table = {}
        self.__limit = self.check(limit)
        self.logger = logging.getLogger('LRUCache')

    def check(self, limit):
        if not isinstance(limit, int):
            self.logger.warning(f'Значение limit не является int')
            raise ValueError("Limit should be int")
        if limit < 1:
            self.logger.warning(f'Значение limit меньше 1')
            raise ValueError("Limit should be positive")
        return limit

    def get(self, key):
        val = self.__cache_table.get(key)
        if val is not None:
            self.set(key, val)
            self.logger.debug(f'get существующего ключа: {key}')
        else:
            self.logger.debug(f'get отсутствующего ключа: {key}')
        return val

    def set(self, key, value):

        if value is None:
            self.logger.warning("Value can't be None")
            raise ValueError("Value can't be None")

        exist_val = self.__cache_table.get(key)

        if exist_val is None and len(self.__cache_table) < self.__limit:
            self.__cache_table[key] = value
            self.logger.debug(f'set отсутствующего ключа: {key}')
        elif exist_val is not None:
            self.__cache_table.pop(key)
            self.__cache_table[key] = value
            self.logger.debug(f'set существующего ключа: {key}')
        else:
            self.__del()
            self.__cache_table[key] = value
            self.logger.debug(f'set отсутствующего ключа, когда достигнута ёмкость: {key}')

        self.logger.info(f'Установлено значение: {key} = {value}')

    def __del(self):
        if len(self.__cache_table) == 0:
            self.logger.warning('Кэш пуст, удаление невозможно')
        else:
            key = next(iter(self.__cache_table))
            self.__cache_table.pop(key)
            self.logger.debug('Выполнено удаление из кэша')
            self.logger.warning(f'Удалено значение из-за превышения лимита кэша')

def configure_logging(log_to_stdout, apply_custom_filter):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('cache.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logging.getLogger('').addHandler(file_handler)

    if log_to_stdout:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logging.getLogger('').addHandler(console_handler)

    if apply_custom_filter:
        logging.getLogger('').addFilter(custom_filter)

def custom_filter(record):
    message = record.getMessage()
    words = message.split()
    return len(words) % 2 != 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Логирование операций с кэшем')
    parser.add_argument('-s', action='store_true', help='Логировать в stdout')
    parser.add_argument('-f', action='store_true', help='Применить кастомный фильтр')

    args = parser.parse_args()

    configure_logging(args.s, args.f)

    cache = LRUCache()

    cache.get('key1')
    cache.get('key2')
    cache.set('key3', 'value3')
    cache.set('key1', 'new_value1')
    cache.set('key4', 'value4')
