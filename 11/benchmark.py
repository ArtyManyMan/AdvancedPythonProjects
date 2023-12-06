import cjson
import json
import time

def loads_one_cjson(json_str):
    cjson.loads(json_str)

def loads_one_json(json_str):
    json.loads(json_str)

def dumps_one_cjson(py_dict):
    cjson.dumps(py_dict)

def dumps_one_json(py_dict):
    json.dumps(py_dict)

def loads_a_lot_cjson(list_json_str):
    for i in list_json_str:
        cjson.loads(i)

def loads_a_lot_json(list_json_str):
    for i in list_json_str:
        json.loads(i)

def dumps_a_lot_cjson(list_py_dict):
    for i in list_py_dict:
        cjson.dumps(i)

def dumps_a_lot_json(list_py_dict):
    for i in list_py_dict:
        json.dumps(i)

if __name__ == '__main__':
    py_dict = {f'key{i}': f'value{i}' for i in range(10_000_000)}
    json_str = json.dumps(py_dict)

    start = time.time()
    loads_one_cjson(json_str)
    end = time.time()
    print(end - start, 'секунд. Время работы cjson.loads')

    start = time.time()
    loads_one_json(json_str)
    end = time.time()
    print(end - start, 'секунд. Время работы json.loads')

    py_dict = {f'key{i}': f'value{i}' for i in range(7_000_000)}

    start = time.time()
    dumps_one_cjson(py_dict)
    end = time.time()
    print(end - start, 'секунд. Время работы cjson.dumps')

    start = time.time()
    dumps_one_json(py_dict)
    end = time.time()
    print(end - start, 'секунд. Время работы json.dumps')

    list_of_dicts = ({f'key{i}': f'value{i}' for i in range(10_000)} for i in range(1000))
    list_of_json_str = (json.dumps(i) for i in list_of_dicts)

    start = time.time()
    loads_a_lot_cjson(list_of_json_str)
    end = time.time()
    print(end - start, 'секунд. Время работы cjson.loads со списком строк json!')

    list_of_dicts = ({f'key{i}': f'value{i}' for i in range(10_000)} for i in range(1000))
    list_of_json_str = (json.dumps(i) for i in list_of_dicts)

    start = time.time()
    loads_a_lot_json(list_of_json_str)
    end = time.time()
    print(end - start, 'секунд. Время работы json.loads со списком строк json!')

    list_of_dicts = ({f'key{i}': f'value{i}' for i in range(5_000)} for i in range(1000))

    start = time.time()
    dumps_a_lot_cjson(list_of_dicts)
    end = time.time()
    print(end - start, 'секунд. Время работы cjson.dumps со списком словарей!')

    list_of_dicts = ({f'key{i}': f'value{i}' for i in range(5_000)} for i in range(1000))

    start = time.time()
    dumps_a_lot_json(list_of_dicts)
    end = time.time()
    print(end - start, 'секунд. Время работы json.dumps со списком словарей!')
