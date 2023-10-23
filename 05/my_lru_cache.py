class LRUCache():

    def __init__(self, limit=42):
        self.__cache_table = {}
        self.__limit = self.check(limit)
        self.__current_size = 0

    @staticmethod
    def check(limit):
        if not isinstance(limit, int):
            raise ValueError("Limit should be int")
        if limit < 1:
            raise ValueError("Limit should be positive")
        return limit

    def get(self, key):
        val = self.__cache_table.get(key)
        if val is None:
            return None
        self.set(key, val)
        return val

    def set(self, key, value):

        if value is None:
            raise ValueError("Value can't be None")

        exist_val = self.__cache_table.get(key)

        if exist_val is None and self.__current_size < self.__limit:
            self.__cache_table[key] = value
            self.__current_size += 1
        elif exist_val is not None and self.__current_size < self.__limit:
            self.__cache_table.pop(key)
            self.__cache_table[key] = value
        elif exist_val is not None:
            self.__cache_table.pop(key)
            self.__cache_table[key] = value
        else:
            self.__del()
            self.__cache_table[key] = value
            self.__current_size += 1

    def __del(self):
        key = iter(self.__cache_table).__next__()
        self.__cache_table.pop(key)
        self.__current_size -= 1
