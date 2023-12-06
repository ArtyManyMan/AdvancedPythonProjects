VENV_DIR := venv
PYTHON := python3
CC := gcc
CFLAGS := -Wall -fPIC $(shell $(PYTHON)-config --includes)
LDFLAGS := $(shell $(PYTHON)-config --ldflags)
OBJECTS := cjson.o

.PHONY: all create-venv install test clean

all: create-venv install test

create-venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip setuptools wheel

install: cjson.so
	$(VENV_DIR)/bin/pip install .

cjson.o: cjson.c
	$(CC) $(CFLAGS) -c -o cjson.o cjson.c

cjson.so: cjson.o
	$(CC) -shared -o cjson.so cjson.o $(LDFLAGS)

test:
	@echo
	@if $(VENV_DIR)/bin/python -m unittest discover -s . -p 'test_cjson.py'; \
	then \
		echo "Tests passed!"; \
	else \
		echo "Tests failed!"; \
	fi

clean:
	rm -rf $(VENV_DIR) cjson.so $(OBJECTS)
