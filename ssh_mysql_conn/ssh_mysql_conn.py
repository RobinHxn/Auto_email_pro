#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Python version: V3.6

Author: Robin&HXN

File version: V1.0

File name: ssh_mysql_conn.py

Created on: 20180828

Resume: SSH to connect mysql DB

"""
import datetime as dt
import pymysql as pyms
import pandas as pd
from sshtunnel import SSHTunnelForwarder


def ssh_to_mysql(conn_jump=None, conn_mysql=None, exec_mysql=None, tempfile=None):
    """

    :param conn_jump: 跳板机配置
    :param conn_mysql: MYSQL配置
    :param exec_mysql: 需执行SQL
    :param tempfile: 输出文件名称
    :return: 输出文件
    """

    with SSHTunnelForwarder(
            (conn_jump["host"], int(conn_jump["port"])),
            ssh_username=conn_jump["user"],
            ssh_password=conn_jump["passwd"],
            remote_bind_address=(conn_mysql["host"], int(conn_mysql["port"]))) as sever:
        conn = pyms.connect(host='127.0.0.1',
                            port=sever.local_bind_port,
                            user=conn_mysql["user"],
                            password=conn_mysql["passwd"])
        return_df = pd.read_sql(exec_mysql, con=conn)
        conn.close()

    return_excel = pd.ExcelWriter(tempfile)
    return_df.to_excel(return_excel, "test")
    return_excel.save()


if __name__ == '__main__':
    ssh_to_mysql()
    print(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    exit(0)
