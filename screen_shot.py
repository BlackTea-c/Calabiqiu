#here to grab your computer screen.
import os.path
import sys
import time

import cv2
import numpy as np
import torch
from win32api import GetSystemMetrics
from win32con import SRCCOPY, SM_CXSCREEN, SM_CYSCREEN, DESKTOPHORZRES, DESKTOPVERTRES
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, GetDC, ReleaseDC, FindWindow
from win32ui import CreateDCFromHandle, CreateBitmap
from win32print import GetDeviceCaps

class Capturer:

    def __init__(self, title: str, region: tuple, interval=60):
        """
        title: 完整的窗体标题, 不支持模糊(因为没有必要)
        region: tuple, (left, top, width, height)
        """
        self.title = title
        self.region = region
        # 设置窗体句柄属性
        self.hwnd = None  # 截图的窗体句柄
        self.timestamp = None  # 上次成功设置句柄的时间戳
        self.interval = interval  # 秒, 更新间隔

    def grab(self):
        """
        还有优化空间, 比如把各个HDC缓存起来, 在截图方法中每次执行BitBlt, 但是考虑到比较麻烦, 而且提升的效果也有限, 就先这样了
        """
        # 检查并按需更新句柄等参数, 在以下时机更新句柄, 1. 句柄属性为空时; 2. 时间戳超过指定更新间隔时
        if (self.hwnd is None) or (self.timestamp is not None and time.perf_counter_ns() - self.timestamp > 1_000_000_000 * self.interval):
            hwnd = FindWindow(None, self.title)  # 找到第一个指定标题的窗体并返回其句柄
            if hwnd != 0:
                self.hwnd = hwnd
                self.timestamp = time.perf_counter_ns()
            else:
                Printer.warning(f'未找到标题为 [{self.title}] 的窗体')
                self.hwnd = None
                self.timestamp = None
        # 获取设备上下文
        left, top, width, height = self.region
        try:
            hWinDC = GetWindowDC(self.hwnd)  # 具有要检索的设备上下文的窗口的句柄。 如果此值为 NULL， GetWindowDC 将检索整个屏幕的设备上下文。等同于调用 GetDesktopWindow() 获得的句柄?
        except BaseException:  # pywintypes.error: (1400, 'GetWindowDC', '无效的窗口句柄。'). 可通过 BaseException 捕获, 通过如右方式判断, if e.args[0] == 1400: pass
            # 此时的句柄不能正常使用, 需要清空并重新获取句柄
            self.hwnd = None
            self.timestamp = None
            # 使用替代句柄
            hWinDC = GetWindowDC(GetDesktopWindow())
        try:
            srcDC = CreateDCFromHandle(hWinDC)
            memDC = srcDC.CreateCompatibleDC()
            bmp = CreateBitmap()
            bmp.CreateCompatibleBitmap(srcDC, width, height)
            memDC.SelectObject(bmp)
            memDC.BitBlt((0, 0), (width, height), srcDC, (left, top), SRCCOPY)
            array = bmp.GetBitmapBits(True)
            img = np.frombuffer(array, dtype='uint8')
            img.shape = (height, width, 4)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            DeleteObject(bmp.GetHandle())
            memDC.DeleteDC()
            srcDC.DeleteDC()
            ReleaseDC(self.hwnd, hWinDC)
            return img
        except BaseException:
            return None

    @staticmethod
    def backup(region):
        """
        region: tuple, (left, top, width, height)
        """
        left, top, width, height = region
        hWin = GetDesktopWindow()
        # hWin = FindWindow(完整类名, 完整窗体标题名)
        hWinDC = GetWindowDC(hWin)
        srcDC = CreateDCFromHandle(hWinDC)
        memDC = srcDC.CreateCompatibleDC()
        bmp = CreateBitmap()
        bmp.CreateCompatibleBitmap(srcDC, width, height)
        memDC.SelectObject(bmp)
        memDC.BitBlt((0, 0), (width, height), srcDC, (left, top), SRCCOPY)
        array = bmp.GetBitmapBits(True)
        DeleteObject(bmp.GetHandle())
        memDC.DeleteDC()
        srcDC.DeleteDC()
        ReleaseDC(hWin, hWinDC)
        img = np.frombuffer(array, dtype='uint8')
        img.shape = (height, width, 4)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img


class Timer:

    @staticmethod
    def cost(interval):
        """
        转换耗时, 输入纳秒间距, 转换为合适的单位
        """
        if interval < 1000:
            return f'{interval} ns'
        elif interval < 1_000_000:
            return f'{round(interval / 1000, 3)} us'
        elif interval < 1_000_000_000:
            return f'{round(interval / 1_000_000, 3)} ms'
        else:
            return f'{round(interval / 1_000_000_000, 3)} s'

