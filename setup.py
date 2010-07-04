import os
from setuptools import setup, find_packages

from cab import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='cab',
    version=".".join(map(str, VERSION)),
    description='The code that powers djangosnippets.org',
    long_description=readme,
    author='James Bennett',
    url='http://github.com/coleifer/cab/tree/master',
    packages=find_packages(),
    package_data = {
        'cab': [
            'templates/*.html',
            'templates/*/*.html',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
