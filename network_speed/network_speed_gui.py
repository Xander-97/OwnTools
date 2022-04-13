#!usr/bin python3
# coding:utf-8

import psutil
import time
import tkinter as tk

FONT = '"B612 Mono" 13'


class Timer:
    def __init__(self, wnd, ms, call):
        self.__wnd = wnd
        self.__ms = ms
        self.__call = call
        self.__running = False

    def start(self):
        if not self.__running:
            self.__wnd.after(0, self.__on_timer)
            self.__running = True

    def stop(self):
        if self.__running:
            self.__running = False

    def is_running(self):
        return self.__running

    def __on_timer(self):
        if self.__running:
            self.__call()
            self.__wnd.after(self.__ms, self.__on_timer)


class NetworkSpeedGui():
    def __init__(self, canvas, width, height) -> None:
        # self.root = tk.Tk()
        self.canvas = canvas
        self.width = width
        self.height = height
        self.canvas.create_text(self.width / 2, self.height / 4, font=FONT, text='', tag='date')
        self.canvas.create_text(self.width / 2, self.height / 3 + 10, font=FONT, text='', tag='up')
        self.canvas.create_text(self.width / 2, self.height / 2 + 20, font=FONT, text='', tag='down')

    def get_net_speed(self) -> list:
        sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        time.sleep(1)  # 因为有sleep所以窗口会卡顿
        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        sent = (sent_now - sent_before) / 1024  # 算出1秒后的差值
        recv = (recv_now - recv_before) / 1024

        return [
            time.strftime(" %Y-%m-%d %H:%M:%S ",
                          time.localtime()), "\n上传: {}b/s".format("%.2f" % sent + 'K' if sent // 1000 == 0 else "%.2f" % (sent / 1000) + 'M'),
            "\n下载: {}b/s".format("%.2f" % recv + 'K' if recv // 1000 == 0 else "%.2f" % (recv / 1000) + 'M')
        ]

    def update(self):
        data = self.get_net_speed()
        self.canvas.itemconfigure('date', text=data[0])
        self.canvas.itemconfigure('up', text=data[1])
        self.canvas.itemconfigure('down', text=data[2])


def run_app(width, height):
    root = tk.Tk()
    root.title('网速悬浮窗')
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.grid(column=0, row=0)
    nsgui = NetworkSpeedGui(canvas, width, height)
    timer = Timer(root, 1000, nsgui.update)
    timer.start()
    root.mainloop()
    timer.stop()


if __name__ == "__main__":
    run_app(230, 120)
