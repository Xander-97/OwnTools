#!usr/bin python3
# coding:utf-8

import psutil
import time
import tkinter as tk
from threading import Timer

FONT = '"B612 Mono" 13'
WIDTH = 230
HEIGHT = 120

root = tk.Tk()
root.title('网速悬浮窗')
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.grid(column=0, row=0)


class NetworkSpeedGui():
    def __init__(self, _canvas, _width, _height) -> None:
        self.canvas = _canvas
        self.width = _width
        self.height = _height
        self.canvas.create_text(self.width / 2, self.height / 4, font=FONT, text='', tags='date')
        self.canvas.create_text(self.width / 2, self.height / 3 + 10, font=FONT, text='', tag='up')
        self.canvas.create_text(self.width / 2, self.height / 2 + 20, font=FONT, text='', tag='down')
        self.sent_before, self.recv_before = 0, 0

        # timer
        self.timer = Timer(0.01, self.get_net_speed)
        self.timer.start()

    def get_net_speed(self):
        self.sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        self.recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        self.timer.cancel()
        self.timer = Timer(1, self.update)
        self.timer.start()
        print('- - ' * 16)
        print('get_net_speed:', self.sent_before, self.recv_before)

    def update(self):
        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        sent = (sent_now - self.sent_before) / 1024  # 算出1秒后的差值
        recv = (recv_now - self.recv_before) / 1024
        print('update:', sent_now, recv_now)
        data = [
            time.strftime(" %Y-%m-%d %H:%M:%S ",
                          time.localtime()), "\n上传: {}b/s".format("%.2f" % sent + 'K' if sent // 1000 == 0 else "%.2f" % (sent / 1000) + 'M'),
            "\n下载: {}b/s".format("%.2f" % recv + 'K' if recv // 1000 == 0 else "%.2f" % (recv / 1000) + 'M')
        ]

        self.canvas.itemconfigure('date', text=data[0])
        self.canvas.itemconfigure('up', text=data[1])
        self.canvas.itemconfigure('down', text=data[2])
        self.timer.cancel()
        self.timer = Timer(1, self.get_net_speed)
        self.timer.start()


if __name__ == "__main__":
    NetworkSpeedGui(canvas, WIDTH, HEIGHT)
    root.mainloop()
