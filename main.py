#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCP协议最大传输速率计算器 - 启动文件
版本: 1.0.0
作者: 曹宇
许可证: MIT License
"""

import tkinter as tk
from tcp_throughput_calculator import TCPThroughputCalculator

def main():
    """
    程序入口点，创建主窗口并启动应用
    """
    root = tk.Tk()
    app = TCPThroughputCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()