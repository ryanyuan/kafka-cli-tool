from setuptools import setup
setup(
    name = 'kafkacli',
    version = '0.1.0',
    packages = ['kafkacli'],
    entry_points = {
        'console_scripts': [
            'kafkacli = kafkacli.__main__:main'
        ]
    })