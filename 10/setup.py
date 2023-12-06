from setuptools import setup, Extension

cjson_module = Extension('cjson',
                         sources=['cjson.c'])

setup(name='cjson',
      version='1.0',
      description='CJSON module',
      ext_modules=[cjson_module])
