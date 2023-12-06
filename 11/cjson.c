#include <Python.h>
#include <string.h>
#include <ctype.h>

int is_number(const char *str) {
    while (*str) {
        if (!isdigit(*str)) {
            return 0;
        }
        str++;
    }
    return 1;
}

static PyObject *loads_cjson(PyObject *self, PyObject *args) {
    const char *input;
    if (!PyArg_ParseTuple(args, "s", &input)) {
        return NULL;
    }

    PyObject *dict = PyDict_New();
    if (!dict) {
        return NULL;
    }

    char *str = strdup(input);
    if (!str) {
        Py_DECREF(dict);
        return PyErr_NoMemory();
    }

    char *token;
	char *saveptr;
	token = strtok_r(str, ":,{}", &saveptr);
	int index = 0;
	PyObject *key = NULL;
	PyObject *value = NULL;
	int quote_removed = 0;

	while (token != NULL) {
	    size_t len = strlen(token);
	    if (len > 0 && token[0] == '\'') {
	        token++;
	        len--;
	    }
	    if (len > 0 && token[len - 1] == '\'') {
	        len--;
	    }

	    // удаляю из токена двойные кавычки
	    size_t write_index = 0;
	    int quote_removed = 0;

		for (size_t i = 0; i < len; ++i) {
		    if (token[i] != '"') {
		        token[write_index++] = token[i];
		    } else {
		        quote_removed = 1;
		    }
		}

	    token[write_index] = '\0';

	    if (token[0] == ' ') {
	    // Если первый символ токена - пробел, уменьшаем токен на пробел
	        token++;
		}

		if (is_number(token) && quote_removed == 0 && index % 2 != 0) {
		    value = PyLong_FromString(token, NULL, 10);
		    if (!value) {
		        PyErr_SetString(PyExc_TypeError, "Failed to convert string to number");
		        Py_DECREF(dict);
		        free(str);
		        return NULL;
		    }

		    PyDict_SetItem(dict, key, value);
		    Py_DECREF(value);
		    value = NULL;
		    index++;
		    token = strtok_r(NULL, ":,{}", &saveptr);
		    continue;
		}

	    if (index % 2 == 0) {
	        key = PyUnicode_FromString(token);
	    } else {
	        value = PyUnicode_FromString(token);
	        if (!key || !value) {
	            Py_XDECREF(key);
	            Py_XDECREF(value);
	            Py_DECREF(dict);
	            free(str);
	            return NULL;
	        }

	        PyDict_SetItem(dict, key, value);
	        Py_DECREF(key);
	        Py_DECREF(value);
	        key = NULL;
	        value = NULL;
	    }
	    index++;
	    token = strtok_r(NULL, ":,{}", &saveptr);
	}
	free(str);
	return dict;

}

static PyObject *dumps_cjson(PyObject *self, PyObject *args) {
    PyObject *input_dict;
    if (!PyArg_ParseTuple(args, "O", &input_dict)) {
        return NULL;
    }


    PyObject *str = PyUnicode_FromString("{");
    if (!str) {
        return NULL;
    }

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    int first_item = 1;

    while (PyDict_Next(input_dict, &pos, &key, &value)) {
        if (!first_item) {
            PyUnicode_Append(&str, PyUnicode_FromString(", "));
        } else {
            first_item = 0;
        }

        PyObject *repr_key = PyObject_Repr(key);
        if (!repr_key) {
            Py_DECREF(str);
            return NULL;
        }
        char *key_str = PyUnicode_AsUTF8(repr_key);
        for (int i = 0; key_str[i]; ++i) {
            if (key_str[i] == '\'') {
                key_str[i] = '"';
            }
        }
        Py_DECREF(repr_key);
        repr_key = PyUnicode_FromString(key_str);
        PyUnicode_Append(&str, repr_key);
        Py_DECREF(repr_key);

        PyUnicode_Append(&str, PyUnicode_FromString(": "));

        PyObject *repr_value = PyObject_Repr(value);
        if (!repr_value) {
            Py_DECREF(str);
            return NULL;
        }

        char *value_str = PyUnicode_AsUTF8(repr_value);
        size_t len = strlen(value_str);
        if (len > 1 && value_str[0] == '\'' && value_str[len - 1] == '\'') {
            value_str[len - 1] = '"';
            value_str[0] = '"';
            repr_value = PyUnicode_FromString(value_str);
        }
        PyUnicode_Append(&str, repr_value);
        Py_DECREF(repr_value);
    }

    PyUnicode_Append(&str, PyUnicode_FromString("}"));
    return str;
}

static PyMethodDef cjson_methods[] = {
    {"loads", loads_cjson, METH_VARARGS, "Load a string into a Python dictionary"},
    {"dumps", dumps_cjson, METH_VARARGS, "Dump a Python dictionary into a string"},
    {NULL, NULL, 0, NULL} // Sentinel
};

static struct PyModuleDef cjsonmodule = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    "C JSON-like functions",
    -1,
    cjson_methods
};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjsonmodule);
}
