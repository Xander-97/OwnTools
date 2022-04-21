#!/usr/bin/env python3
# coding:utf-8

# import sys
import psutil
import time


def get_net_speed():
    out = ""
    sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
    recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
    time.sleep(1)
    sent_now = psutil.net_io_counters().bytes_sent
    recv_now = psutil.net_io_counters().bytes_recv
    sent = (sent_now - sent_before) / 1024  # 算出1秒后的差值
    recv = (recv_now - recv_before) / 1024

    out += time.strftime(" [%Y-%m-%d %H:%M:%S] ", time.localtime())
    out += "上传: {}b/s".format("%.2fK" % sent if sent // 1000 == 0 else "%.2fM" % (sent/1000))
    out += "\t下载: {}b/s".format("%.2fK" % recv if recv // 1000 == 0 else "%.2fM" % (recv/1000))

    return out


if __name__ == "__main__":
    # command = 'cls' if sys.platform.lower() == 'win32' else 'clear'
    print()
    while 1:
        # os.system(command)
        print('\r{0} {1} {2}'.format('-' * 16, get_net_speed(), '-' * 16), end='')
