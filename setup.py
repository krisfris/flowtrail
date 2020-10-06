import numpy
from setuptools import setup, find_packages, Extension


setup(
    name='flowtrail',
    version='0.1.0',
    packages=find_packages(),
    ext_modules=[
        Extension(
            'flowtrail._transformations', ['flowtrail/transformations.c'],
            include_dirs=[numpy.get_include()]
        )
    ]
)
