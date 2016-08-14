# -*- coding:gb2312 -*-

"""
A simple args parser and a color wrapper.
"""
import sys
import random
import warnings
warnings.filterwarnings("ignore")
import requests
from requests.exceptions import ConnectionError, Timeout
from colorama import init, Fore, Back, Style
init(autoreset=True)

__all__ = ['args', 'colored', 'requests_get', 'exit_after_echo']

def exit_after_echo(msg, color='red'):
    if color == 'red':
        print(colored.red(msg))
    else:
        print(msg)
    sys.exit(1)


def requests_get(url, **kwargs):
    USER_AGENTS = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
        ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
         'Chrome/19.0.1084.46 Safari/536.5'),
        ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
         'Safari/536.5')
    )
    try:
        r = requests.get(
            url,
            timeout=12,
            headers={'User-Agent': random.choice(USER_AGENTS)}, **kwargs
        )
    except ConnectionError:
        exit_after_echo('Network connection failed.')
    except Timeout:
        exit_after_echo('timeout.')
    return r

class Args(object):

    """A simple customed args parser for `iquery`."""

    def __init__(self, args=None):
        self._args = sys.argv[1:]
        self._argc = len(self)

    def __repr__(self):
        return '<args {}>'.format(repr(self._args))

    def __len__(self):
        return len(self._args)

    @property
    def all(self):
        return self._args

    def get(self, idx):
        try:
            return self.all[idx]
        except IndexError:
            return None

    @property
    def is_null(self):
        return self._argc == 0

    @property
    def options(self):   # ��ȡ��Ʊ��ѯѡ��  ex: iquary -dgktz �Ϻ�  ����   ����dgktz
        """Train tickets query options."""
        arg = self.get(0)   #  -dgktz
        if arg.startswith('-') and not self.is_asking_for_help:
            return arg[1:]   # dgktz
        return ''.join(x for x in arg if x in 'dgktz')

    @property
    def is_asking_for_help(self):
        arg = self.get(0)
        if arg in ('-h', '--help'):
            return True
        return False

    @property
    def is_querying_train(self):
        if self._argc not in (3, 4):
            return False
        if self._argc == 4:
            arg = self.get(0)
            if not arg.startswith('-'):
                return False
            if arg[1] not in 'dgktz':
                return False
        return True

    @property
    def as_train_query_params(self):  # ��ѯ����
        opts = self.options
        if opts:
            # apped valid options to end of list
            return self._args[1:] + [opts]
        return self._args


#  ʹ�ÿ�ƽ̨��colorama�������ն�����ַ�����ɫ,���ֱ����ԭʼ��
# ת���ַ����д�ӡ��ɫ������windows�´��ڼ�������,�еİ汾�޷���
# ʾ
class Colored(object):

    #  ǰ��ɫ:��ɫ  ����ɫ:Ĭ��
    def red(self, s):
        return Fore.RED + s + Fore.RESET

    #  ǰ��ɫ:��ɫ  ����ɫ:Ĭ��
    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    #  ǰ��ɫ:��ɫ  ����ɫ:Ĭ��
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET

    #  ǰ��ɫ:��ɫ  ����ɫ:Ĭ��
    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET

    #  ǰ��ɫ:���ɫ  ����ɫ:Ĭ��
    def magenta(self, s):
        return Fore.MAGENTA + s + Fore.RESET

    #  ǰ��ɫ:��ɫ  ����ɫ:Ĭ��
    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET

    #  ǰ��ɫ:��ɫ  ����ɫ:Ĭ��
    def white(self, s):
        return Fore.WHITE + s + Fore.RESET

    #  ǰ��ɫ:��ɫ  ����ɫ:Ĭ��
    def black(self, s):
        return Fore.BLACK

    #  ǰ��ɫ:��ɫ  ����ɫ:��ɫ
    def white_green(self, s):
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET


args = Args()
colored = Colored()


