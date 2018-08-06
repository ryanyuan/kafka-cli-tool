from setuptools import setup
from kafkacli import util

setup(
    name = 'kafkacli',
    version = util.VERSION,
    description = 'Apache Kafka CLI utility tool.',
    author = 'Ryan Yuan',
    url = 'https://github.com/ryanyuan/kafkacli',
    packages = ['kafkacli'],
    entry_points = {
        'console_scripts': [
            'kafkacli = kafkacli.__main__:main'
        ]
    }
)