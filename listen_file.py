# coding: utf8
import os
import pyinotify
import config
import time
import smtplib
from email.mime.text import MIMEText


def send_email(log):
    msg = MIMEText('你好！服务器出现错误, 错误日志为：%s，请及时处理！'% log, )
    send_email_account = config.email_config['send_email_account']
    send_email_password = config.email_config['send_email_password']
    smtp_server = 'smtp.qq.com'
    receive_email_account = config.email_config['receive_email_account']
    msg['From'] = send_email_account
    msg['To'] = receive_email_account
    msg['Subject'] = 'Server Alert Mail!'
    server = smtplib.SMTP_SSL(smtp_server, 465)
    # server = smtplib.SMTP(smtp_server, 25)
    server.login(send_email_account, send_email_password)
    server.sendmail(send_email_account, [receive_email_account], msg.as_string())
    server.quit()
    print('email send success!')


pos = 0


def print_log():
    global pos
    log = ''
    try:
        fd = open(config.log_config['log_path'])
        if pos != 0:
            fd.seek(pos, 0)
        while True:
            line = fd.readline()
            if line.strip():
                log = line.strip()
                print(log)
            pos = pos + len(line)
            if not line.strip():
                break
        fd.close()
    except Exception:
        print('exception1')
    return log


class MyEventHandler(pyinotify.ProcessEvent):
    # 当文件被修改时调用函数
    def process_IN_MODIFY(self, event):
        try:
            print_log()
        except Exception:
            print('exception2')

    # 文件自动被删除  # 文件被删除 或者切割
    def process_IN_MOVE_SELF(self, event):
        global notifier
        try:
            notifier.stop()
        except Exception:
            print('exception3')


notifier = None


def main():
    global notifier, pos
    path = config.log_config['log_path']

    while True:
        if os.path.isfile(path):
            pos = 0
            # 输出前面的log
            log = print_log()
            if log: send_email(log)
            # watch manager
            wm = pyinotify.WatchManager()
            eh = MyEventHandler()
            notifier = pyinotify.Notifier(wm, eh)
            wm.add_watch(config.log_config['log_path'], pyinotify.ALL_EVENTS, rec=True)
            try:
                notifier.loop()
            except Exception:
                print('exception3')
        else:
            time.sleep(60)


if __name__ == '__main__':
    main()
