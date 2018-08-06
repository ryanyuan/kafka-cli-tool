VERSION = '0.0.6'
DESCRIPTION = """kafkacli - Apache Kafka utility tool
https://github.com/ryanyuan/kafkacli
Copyright (c) 2018-2018, Ryan Yuan
Version {}""".format(VERSION)

def print_dashed_line():
    print("--------------------------------------")

def show_version():
    """Show the version string."""
    print('kafkacli version {}'.format (VERSION))