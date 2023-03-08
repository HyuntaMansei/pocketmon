import sqlalchemy
import pymysql
import configparser
import os, sys
import IPython

# 디버깅 모드 설정. 쥬피터 노트에서 실행중인지 확인.
if 'IPKernelApp' in IPython.Application.instance().__class__.__name__:
    debug_mode = True
else:
    debug_mode = False

debug_mode = True

debugging_flags = [1]
def debug(msg, flag_id:int =1):
    if flag_id in debugging_flags and debug_mode:
        print(msg)

def show_config(cur_conf):
    for k, v in cur_conf.items():
        print(k)
        for k2, v2 in v.items():
            print(k2, v2)

#mysql db와 연결하여 data를 처리하는 클래스
config = configparser.ConfigParser()
# conf_path = os.getcwd() + os.sep + 'ignore' + os.sep + 'config.ini'
# conf_path = r'C:\Users\jchoi\Coding\python\stockmanager\ignore\config.ini'
# conf_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'ignore' + os.sep + 'config.ini'
# conf_path = os.path.dirname('..\ignore\config.ini')
# conf_path = '..\ignore\config.ini'

#부모디렉토리는 dirname을 한번 더 사용하면 된다. 파일일 경우 디렉토리를, 디렉토리일 경우 상위 디렉토리를 리턴한다.
dir_path = os.path.dirname(os.path.abspath(__file__))
conf_path = os.path.dirname(dir_path) + r'\ignore\config.ini'

debug(conf_path, 0)

config.read(conf_path, encoding='utf-8')
# config의 내용을 확인해주는 함수
# show_config(config)
db_conf = dict(config['DB_CONFIG'])
db_conf['port'] = int(db_conf['port'])

class DbManager:
    def __init__(self):
        self.connect()
    def __del__(self):
        self.close()
    def connect(self):
        try:
            self.conn = pymysql.connect(**db_conf)
            self.cur = self.conn.cursor()
            print("Connected")
        except pymysql.Error as e:
            print("error!", e)
    def close(self):
        self.conn.close()
    def test(self):
        print("DbManger testing")
    def execute(self, sql, data=()):
        self.cur.execute(sql, data)
        self.conn.commit()
    def print_fetched(self):
        for f in self.cur.fetchall():
            print(f)