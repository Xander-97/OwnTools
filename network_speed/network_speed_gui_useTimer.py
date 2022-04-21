#!/usr/bin/env python3
# coding:utf-8

import os
import sys
import psutil
import time
import tkinter as tk
from threading import Timer
from PIL import Image, ImageTk


PUBLIC_FONT = '"B612 Mono" 13 bold'
WIDTH = 230
HEIGHT = 120
# WIDTH = 260
# HEIGHT = 267
BASIC_COLOR = 'gray'
FONT_COLOR = "blue"
ROOT = None
CANVAS = None
BACKGROUND = None

# 初始化更新标志
Flag = True


class Unit:
    '''计量单位'''
    Mbps: int = 0
    Mbs: int = 1


# default unit
Mode: int = Unit.Mbps


def modify(e):
    '''switch units'''
    global Mode
    if Mode == Unit.Mbs:
        Mode = Unit.Mbps
    else:
        Mode = Unit.Mbs
    # print(Mode)


def exit(e):
    ROOT.destroy()


def on_resize(e):
    ROOT.configure(width=e.width, height=e.height)
    create_rectangle(CANVAS)


def set_content_and_mode(sent, recv, mode: Unit):
    sent /= 1024
    recv /= 1024
    if mode == Unit.Mbps:
        return ("\n\r上传:{:.2f} Mbps".format(sent / 1000 * 8), "\n\r下载:{:.2f} Mbps".format(recv / 1000 * 8))
    else:
        return ("\n\r上传:{}b/s".format('%.2f K' % sent if sent // 1000 == 0 else '%.2f M' % (sent / 1000)),
                "\n\r下载:{}b/s".format('%.2f K' % recv if recv // 1000 == 0 else '%.2f M' % (recv / 1000)))


def get_time(localtime):
    return time.strftime("%Y-%m-%d %H:%M:%S", localtime)


def create_rectangle(canvas):
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=BASIC_COLOR, outline=BASIC_COLOR)


def main():
    global BACKGROUND
    root = tk.Tk()
    root.title('网速悬浮窗')
    # root.overrideredirect(True)  # 无边框窗口
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.grid(column=0, row=0)
    # BACKGROUND = ImageTk.PhotoImage(Image.open(os.path.dirname(__file__) + os.sep + 'pkq1.png'))
    canvas.create_image(125, 125, anchor='center')  # image=BACKGROUND
    # create_rectangle(canvas)
    if sys.platform == 'win32':
        # 设置透明窗口
        root.wm_attributes('-transparentcolor', BASIC_COLOR)

    return root, canvas


class NetworkSpeedGui():
    def __init__(self, _canvas, _width, _height) -> None:
        self.canvas = _canvas
        self.width = _width
        self.height = _height
        self.canvas.create_text(self.width / 2, self.height / 4, font=PUBLIC_FONT, tags='date', text='', fill=FONT_COLOR, justify=tk.CENTER)  # tag带不带s都可以
        self.canvas.create_text(self.width / 2, self.height / 3, font=PUBLIC_FONT, text='', tag='up', fill=FONT_COLOR, justify=tk.LEFT)
        self.canvas.create_text(self.width / 2, self.height / 2 + 10, font=PUBLIC_FONT, text='', tag='down', fill=FONT_COLOR, justify=tk.LEFT)
        self.sent_before, self.recv_before = 0, 0

        # timer
        self.timer = Timer(0, self.get_net_speed)
        self.timer.start()

    def get_net_speed(self):
        global Flag

        # 时间获取应该在此处,不然就隔着运行2秒 初始化数值 clock
        self.canvas.itemconfigure('date', text=get_time(time.localtime()))
        if Flag:
            sent, recv = set_content_and_mode(self.sent_before, self.recv_before, Mode)
            self.canvas.itemconfigure('up', text=sent)
            self.canvas.itemconfigure('down', text=recv)
            Flag = False

        self.sent_before = psutil.net_io_counters().bytes_sent  # traffic sent
        self.recv_before = psutil.net_io_counters().bytes_recv  # received traffic

        self.timer.cancel()
        self.timer = Timer(1, self.update)
        self.timer.start()
        # print('- - ' * 16)
        # print('get_net_speed:', self.sent_before, self.recv_before)

    def update(self):
        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        sent = sent_now - self.sent_before
        recv = recv_now - self.recv_before
        # print('update:', sent_now, recv_now)
        data = [get_time(time.localtime()), *set_content_and_mode(sent, recv, Mode)]

        self.canvas.itemconfigure('date', text=data[0])
        self.canvas.itemconfigure('up', text=data[1])
        self.canvas.itemconfigure('down', text=data[2])
        self.timer.cancel()
        self.timer = Timer(0, self.get_net_speed)
        self.timer.start()


if __name__ == "__main__":
    ROOT, CANVAS = main()
    NetworkSpeedGui(CANVAS, WIDTH, HEIGHT)
    # ROOT.bind('<Configure>', on_resize)
    ROOT.bind('<Double-Button-3>', exit)
    ROOT.bind('<Double-Button-1>', modify)
    ROOT.mainloop()
