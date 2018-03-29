#!/usr/bin/env python
# coding=utf-8
# author: Tang Hong
import inspect
import MySQLdb
import string
import time
import json
import os
import sys

MYSQL_USER = "ysboss"
# MYSQL_HOST = "192.168.1.250"
MYSQL_HOST = "172.30.254.151"
MYSQL_PASSWORD = "Yunshang2014"
MYSQL_PORT = 3306
MYSQL_DATABASE = "boss"

# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)


class MysqlDB(object):
    def __init__(self, user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_DATABASE):
        self.sql = None
        self._result = None
        start_time = time.time()
        print "Connect to MySQL database by {0}, it should be only call one time!!!".format(user)
        self._conn = MySQLdb.connect(host=host, user=user, passwd=password, port=port, db=db)
        self._cur = self._conn.cursor()
        end_time = time.time()
        print "Connection cost {0} seconds.".format(end_time - start_time)

    def __del__(self):
        self._conn.close()
        print "Disconnect to MySQL"

    def execute(self, sql_command):
        self.sql = sql_command.strip()
        if self.sql.startswith("select" or "SELECT"):
            self._cur.execute(self.sql)
            self._result = self._cur.fetchall()  # [tuple, tuple, ...]
            return self
        else:
            self._cur.execute(self.sql)
            self._conn.commit()
            time.sleep(1)
            print "Commit Successfully"

    def __has_alias__(self):
        # 选取sql语句中的列名
        start = string.find(self.sql, "select " or "SELECT ")
        end = string.find(self.sql, "from " or "FROM ")
        columns = self.sql[start + 6:end]
        # 判断列名是否为"*"
        if string.rfind(columns, " * ") == -1:
            cols = columns.split(", ")
        else:
            table_index = string.find(self.sql[end + 5:].strip(), " ")
            if table_index == -1:
                table_name = self.sql[end + 5:].strip()
            else:
                table_name = self.sql[end + 5:end + 5 + table_index]
            # 获取数据表的所有列名
            self._cur.execute("select COLUMN_NAME from information_schema.columns "
                              "where table_name = '{0}'".format(table_name))
            self.rows = self._cur.fetchall()
            cols = []
            for row in self.rows:
                for col in row:
                    cols.append(col)

        # 判断是否有别名
        key_list = []
        for col in cols:
            has_alias = string.rfind(col.strip(), " ")
            if has_alias == -1:
                key_list.append(col.strip())
            else:
                key_list.append(col[has_alias + 1:].strip())

        return key_list

    def to_rows(self):
        # 将每行查询结果保存为list
        return [row for row in self._result]

    def only_one(self):
        # 当查询结果只有一行一列时, 直接输出结果
        if len(self._result) == 1:
            if len(self._result[0]) == 1:
                result = self._result[0][0]
                return result
            else:
                print "result:", self._result
                raise ValueError
        else:
            print "result:", self._result
            raise ValueError

    def to_dict(self):
        # 将每行查询结果以别名为key转换为dict, 并将结果保存为list
        results = []
        key_list = self.__has_alias__()
        print key_list
        if len(key_list) != 0:
            for row in self._result:
                result = {}
                for key in range(len(row)):
                    result[key_list[key]] = row[key]
                results.append(result)
        return results

    def to_cols(self):
        # 将每列查询结果转换为一个list, 并将结果保存为list
        results = []
        if len(self._result) != 0:
            for index in range(len(self._result[0])):
                result = [row[index] for row in self._result]
                results.append(result)
        return results

    def one_by_one(self):
        # 将查询结果先按行再按列地转换为一个个string, 并将结果保存为list
        return [result for row in self._result for result in row]


def get_files_info_with_rename_key():
    sql = "select hex(file_id) AS file_id, fsize AS file_size, psize AS piece_size, ppc " \
          "from boss.ppc_tenant_files where source like '%vodtest%' limit 10"
    resp = MysqlDB().execute(sql).to_dict()
    f = open('{0}/all_files.txt'.format(parent_path), 'w')
    f.write(json.dumps(resp))
    f.close()
    return resp


if __name__ == "__main__":
    get_files_info_with_rename_key()
