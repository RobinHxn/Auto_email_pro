#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Python version: V3.6

Author: Robin&HXN

File version: V1.0

File name: easy_mailer.py

Created on: 20160902

Resume: 便捷发送邮件

"""

from mailthon import postman, email
import datetime as dt
import json
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def send_mail_easy(content="", subject="[自动报表]", attachment=None, receivers=None, error_receivers=None, cc=None):
    """

    :param content: 输入邮件正文
    :param subject: 输入邮件主题
    :param attachment: 输入邮件附件
    :param receivers: 输入收件人
    :param error_receivers: 输入报错邮件收件人
    :param cc: 输入抄送人
    :return: None
    """

    if receivers is None:
        receivers = ["黄兴耐<huangxingnai@zhixuezhen.com>"]
    if error_receivers is None:
        error_receivers = ["黄兴耐<huangxingnai@zhixuezhen.com>"]
    if cc is None:
        cc = ["黄兴耐<huangxingnai@zhixuezhen.com>"]
    password_json = json.load(open(u'/Users/huangxingnai/PycharmProjects/my_password.json', 'r'))
    mail_auth = password_json["mail_auth"]
    user = mail_auth["user"]
    password = mail_auth["passwd"]
    mail_sender = u"自动报表 <%s>" % user
    p = postman(host='smtp.exmail.qq.com', auth=(user, password))

    try:
        if attachment is not None:
            p.send(email(
                content=content,
                subject=subject,
                sender=mail_sender,
                attachments=attachment,
                receivers=receivers,
                cc=cc
            ))
        else:
            p.send(email(
                content=content,
                subject=subject,
                sender=mail_sender,
                receivers=receivers,
                cc=cc
            ))

    except Exception as e:
        logging.error(e)
        local_time = time.localtime()
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

        p.send(email(
            content="邮件发送出错啦：%s\n出错时间：%s" % (e, time_str),
            subject="邮件发送出错",
            sender=mail_sender,
            receivers=error_receivers,
        ))


if __name__ == '__main__':
    send_mail_easy()
    print(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    exit(0)
