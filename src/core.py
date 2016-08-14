# -*- coding:gb2312 -*-

"""
The program entrance.
"""
import requests
from utils import args, exit_after_echo

def show_usage():
    """Usage:
    ttk [-dgktz] <from> <to> <date>

Go to `ttk -h` or `ttk --help`for more details.
"""
    pass


def cli():
    """train tickets query via command line.

Usage:
    ttk -h
    ttk --help
    ttk [-dgktz] <from> <to> <date>

Arguments:
    from             ����վ
    to               ����վ
    date             ��ѯ����

Options:
    -h, --help       ��ʾ�ð����˵�.

    -dgktz           ����,����,����,�ؿ�,ֱ��
Note:
    ���������ڲ�����ʱ��ע���������,��������2016111���ᱻ
    ������2016-11-01,������2016-01-11.Ҫ����2016-1-11����
    ��20160111,ע�������������2016-1-11,�����������ƴ���.

"""

    if args.is_asking_for_help:
        exit_after_echo(cli.__doc__, color=None)

    elif args.is_querying_train:
        from train import query
        result = query(args.as_train_query_params)
        result.pretty_print()
    else:
        exit_after_echo(show_usage.__doc__, color=None)

