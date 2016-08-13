# -*- coding:gb2312 -*-

"""
# The program entrance.
Train tickets query and display. The datas come
from:
    www.12306.cn
"""

import os
import re
import sys
reload(sys)
sys.setdefaultencoding('GB2312')
import datetime
from collections import OrderedDict
from prettytable import PrettyTable
from utils import colored, requests_get, exit_after_echo
from Q2B_and_B2Q import *

__all__ = ['query']

QUERY_URL = 'https://kyfw.12306.cn/otn/lcxxcx/query'    # ��Ʊ��ѯ
PRICE_QUERY_URL = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice'  # Ʊ�۲�ѯ
# ERR
FROM_STATION_NOT_FOUND = 'From station not found.'
TO_STATION_NOT_FOUND = 'To station not found.'
INVALID_DATE = 'Invalid query date.'
TRAIN_NOT_FOUND = 'No result.'
NO_RESPONSE = 'Sorry, server is not responding.'


class TrainsCollection(object):

    """A set of raw datas from a query."""

    headers = '���� ��վ ʱ�� ��ʱ ������ �ص��� һ���� ������ �߼����� ���� Ӳ�� ���� Ӳ�� ���� ����'.split()

    def __init__(self, rows, opts, date, from_station, to_station):
        self._rows = rows
        self._opts = opts
        self._date = date
        self._from_station = from_station
        self._to_station = to_station
        cnt = 0     #  ��¼���θ���
    def __repr__(self):
        return '<TrainsCollection size={}>'.format(len(self))

    def __len__(self):
        return len(self._rows)

    def _get_duration(self, row):
        duration = row.get('lishi').encode('GB2312').replace(':', 'Сʱ') + '����'
        # take 0 hour , only show minites
        if duration.startswith('00'):   #  С��һСʱ  ex: 00Сʱ23����--->23����
            return duration[4:]
        # take <10 hours, show 1 bit
        if duration.startswith('0'):  #  С��ʮСʱ  ex: 05Сʱ38����--->5Сʱ38����
            return duration[1:]
        return duration

    def _build_params(self, row):
        """Ʊ���������, ���������ֵ�,�ֵ����˳��Ͳɵ�ʱ����˳�����һ��,Ҫ��Ȼ�����ʧ��
        """
        d = OrderedDict()
        d['train_no'] = row.get('train_no')
        d['from_station_no'] = row.get('from_station_no')
        d['to_station_no'] = row.get('to_station_no')
        d['seat_types'] = row.get('seat_types')
        d['train_date'] = self._date
        return d

    #  --------------- ����Ʊ���������� -----------------
    # {"validateMessagesShowId": "_validatorMessage",
    #  "status": true,
    #  "httpstatus": 200,
    #  "data": {"3": "3105",
    #           "A1": "?180.5",
    #           "1": "1805",
    #           "A4": "?488.5",
    #           "A3": "?310.5",
    #           "4": "4885",
    #           "OT": [],
    #           "WZ": "?180.5",
    #           "train_no": "870000K35963"
    #           },
    #  "messages": [],
    #  "validateMessages": {}}
    # --------------------------------------------------

    def _get_price(self, row):       # ��ȡÿ�г���ͬϯ���Ʊ��,����һ���б�
        params = self._build_params(row)
        r = requests_get(PRICE_QUERY_URL, params=params, verify=False)
        try:
            rows = r.json()['data']  # �õ�json��ѯ���
        except KeyError:
            rows = {}
        except TypeError:
            exit_after_echo(NO_RESPONSE)
        return rows

    def replace_and_append(self, s, c='', a='Ԫ'):
        '''
         �˺������Խ������ַ����ĵ�һ���ַ��滻��c,Ȼ��
         ��ĩβ׷��һ���ַ���a.���sΪ����׷���κ��ַ���.
         Ĭ��׷�� 'Ԫ'
         �������ַ���s�еĵ�һ���ַ��滻���ַ�c.
         ����������ַ����к���gb2312�޷������
         �ַ�,������ᱨ��.�����Ҫ�����滻��gb2312
         �ܱ�����ַ�. �ڴ��滻���ڸ�����һ���ַ���.
        :param s: ���滻�ַ���
        :param c: Ŀ���ַ�
        :param a: ׷���ַ���
        :return: �����滻����ַ���
        '''

        try:
            result = ''
            if s:
                result = re.sub('^.', c, s)
                result = result + a
            return colored.yellow(result)
        except TypeError:
            pass
        except:
            pass

    @property
    def trains(self):
        """Filter rows according to `headers`"""
        for row in self._rows:  #  self._rows:�б�����,ÿ��Ԫ��Ϊһ���ֵ�,����һ������
            train_no = row.get('station_train_code')
            initial = train_no[0].lower()   # �����״�ĸ  ex:  G851--->g
            if not self._opts or initial in self._opts:   #  ���˳�������
                # '���� ��վ ʱ�� ��ʱ ������ �ص��� һ���� ������ �߼����� ���� Ӳ�� ���� Ӳ�� ���� ����'
                train = [
                    # Column: '����'
                    train_no,
                    # Column: '��վ'
                    '\n'.join([
                        colored.green(row.get('from_station_name').encode('GB2312')),
                        colored.red(row.get('to_station_name').encode('GB2312'))
                    ]),
                    # Column: 'ʱ��'
                    '\n'.join([
                        colored.green(row.get('start_time')),
                        colored.red(row.get('arrive_time')),
                    ]),
                    # Column: '��ʱ'
                    self._get_duration(row),
                    # Column: '����'
                    row.get('swz_num'),
                    # Column: '�ص�'
                    row.get('tz_num'),
                    # Column: 'һ��'
                    row.get('zy_num'),
                    # Column: '����'
                    row.get('ze_num'),
                    # Column: '�߼�����'
                    row.get('gr_num'),
                    # Column: '����'
                    row.get('rw_num'),
                    # Column: 'Ӳ��'
                    row.get('yw_num'),
                    # Column: '����'
                    row.get('rz_num'),
                    # Column: 'Ӳ��'
                    row.get('yz_num'),
                    # Column: '����'
                    row.get('wz_num'),
                    # Column: '����'
                    row.get('qt_num')
                ]
                # ---------ͨ���ɵ�õ�ϯ���Ӧ�ı�� ---------------
                #               ������: A9
                #               �ص���: P
                #               һ����: M
                #               ������: O
                #               �߼�����: A6
                #               ����: A4
                #               Ӳ��: A3
                #               ����: A2
                #               Ӳ��: A1
                #               ����: WZ
                #               ����: OT[]
                # -------------------------------------------------
                price_dict = self._get_price(row)   #  ��ȡƱ������
                try:
                    ot_str = self.replace_and_append('\n'.join(price_dict.get('OT')), '')
                except TypeError:
                    ot_str = ''
                price = [          # Ʊ���б�
                    colored.yellow('Ʊ��'),
                    '',
                    '',
                    '',
                    # ���ڴӷ�������ȡ�����ַ����е�һ���ַ���'��',����ַ�
                    # ��GB2312���������޷������,�ڴ�������лᱨ��,�����Ҫ
                    # ����һ���ַ��滻��,�ڴ��ÿ��ַ��滻,��ʾɾ����һ���ַ�,
                    # Ȼ��׷�� 'Ԫ' �ַ���,��ʾ�����
                    #  ����
                    self.replace_and_append(price_dict.get('A9', '')),
                    #  �ص�
                    self.replace_and_append(price_dict.get('P', '')),
                    #  һ��
                    self.replace_and_append(price_dict.get('M', '')),
                    # ����
                    self.replace_and_append(price_dict.get('O', '')),
                    # �߼�����
                    self.replace_and_append(price_dict.get('A6', '')),
                    # ����
                    self.replace_and_append(price_dict.get('A4', '')),
                    # Ӳ��
                    self.replace_and_append(price_dict.get('A3', '')),
                    # ����
                    self.replace_and_append(price_dict.get('A2', '')),
                    # Ӳ��
                    self.replace_and_append(price_dict.get('A1')),
                    # ����
                    self.replace_and_append(price_dict.get('WZ', '')),
                    # ����
                    ot_str
                ]
                data_list = [train, price]
                yield data_list                # ���س�Ʊ��Ϣ��Ʊ����Ϣ

    def get_table_header(self):
        '''
        ��ӡ������: ex: �ӳ�->����(2016��08��17�� ����)
        :return:�޷���ֵ
        '''
        week_dict = {
            'Mon': '��һ',
            'Tue': '�ܶ�',
            'Wed': '����',
            'Thu': '����',
            'Fri': '����',
            'Sat': '����',
            'Sun': '����'
        }
        date = datetime.datetime.strptime(self._date, '%Y-%m-%d')
        date_str = date.strftime('%Y��%m��%d�� %a')
        date_str = date_str.replace(date_str[-3:], week_dict[date_str[-3:]])
        header = self._from_station + '->' + self._to_station + '(' + date_str + ')'
        print '\n%92s' % colored.red(header)

    def note_str(self, note_str):
        temp_str = '%-139s' % note_str
        print colored.note_str(temp_str)

    def pretty_print(self):
        """Use `PrettyTable` to perform formatted outprint."""
        self.note_str('����Ŭ������������......')
        pt = PrettyTable()
        pt.encoding = 'GB2312'   # ����prettytable���뷽ʽ,Ҫ��Ȼ��windows���޷���ӡ����
        if len(self) == 0:
            pt._set_field_names(['Sorry,'])
            pt.add_row([TRAIN_NOT_FOUND])
        else:
            pt._set_field_names(self.headers)
            for train in self.trains:
                pt.add_row(train[0])
                pt.add_row(train[1])
        self.note_str('���ݼ������......')
        self.get_table_header()
        print(pt)


class TrainTicketsQuery(object):

    """Docstring for TrainTicketsCollection. """

    def __init__(self, from_station, to_station, date, opts=None):

        self.from_station = from_station
        self.to_station = to_station
        self.date = date
        self.opts = opts

    def __repr__(self):
        return 'TrainTicketsQuery from={} to={} date={}'.format(
            self.from_station, self.to_station, self.date
        )

    @property
    def stations(self):
        filepath = os.path.join(    #  ��ȡ��վ�����ļ���
            os.getcwd(),
            r'datas', r'stations.dat'
        )
        d = {}
        with open(filepath, 'r') as f:
            for line in f.readlines():
                name, telecode = line.split()
                d.setdefault(name, telecode)      # ����վ���ݼ��ص��ֵ�
        return d

    @property
    def _from_station_telecode(self):
        # import chardet
        # print chardet.detect(self.from_station)   #  ����������--������
        code = self.stations.get(self.from_station)
        if not code:
            exit_after_echo(FROM_STATION_NOT_FOUND)
        return code

    @property
    def _to_station_telecode(self):
        code = self.stations.get(self.to_station)
        if not code:
            exit_after_echo(TO_STATION_NOT_FOUND)
        return code

    @property
    def _valid_date(self):
        """Check and return a valid query date."""
        date = self._parse_date(self.date)

        if not date:
            exit_after_echo(INVALID_DATE)

        try:
            date = datetime.datetime.strptime(date, '%Y%m%d')
        except ValueError:
            exit_after_echo(INVALID_DATE)

        # A valid query date should within 50 days.
        offset = date - datetime.datetime.today()
        if offset.days not in range(-1, 50):
            exit_after_echo(INVALID_DATE)

        return date.strftime('%Y-%m-%d')
        # return datetime.date.strftime(date, '%Y-%m-%d')

    @staticmethod
    def _parse_date(date):
        """Parse from the user input `date`.

        e.g. current year 2016:
           input 6-26, 626, ... return 2016626
           input 2016-6-26, 2016/6/26, ... retrun 2016626

        This fn wouldn't check the date, it only gather the number as a string.
        """
        result = ''.join(re.findall('\d', date))
        l = len(result)

        # User only input month and day, eg 6-1, 6.26, 0626...
        if l in (2, 3, 4):
            # year = str(datetime.today().year)
            year = str(datetime.date.today().year)
            return year + result   # ת������������ʽ  ex:423--->2016423

        # User input full format date, eg 201661, 2016-6-26, 20160626...
        if l in (6, 7, 8):
            return result

        return ''

    def _build_params(self):
        """Have no idea why wrong params order can't get data.
        So, use `OrderedDict` here.
        """
        d = OrderedDict()
        d['purpose_codes'] = 'ADULT'
        d['queryDate'] = self._valid_date
        d['from_station'] = self._from_station_telecode
        d['to_station'] = self._to_station_telecode
        return d

    def query(self):

        params = self._build_params()

        r = requests_get(QUERY_URL, params=params, verify=False)

        try:
            rows = r.json()['data']['datas']   # �õ�json��ѯ���
        except KeyError:
            rows = []
        except TypeError:
            exit_after_echo(NO_RESPONSE)
        query_date = self._valid_date
        return TrainsCollection(rows, self.opts, query_date, self.from_station, self.to_station)


def query(params):
    """`params` is a list, contains `from`, `to`, `date`."""

    return TrainTicketsQuery(*params).query()
