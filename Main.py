import GPUtil
import psutil
import platform
import speedtest
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from datetime import datetime

class SystemScanner(object):
    def get_size(self, bytes, suffix="8"):
        """
        Scale bytes to its proper format
        e.g:
            123456 => '1.20MB
            123456789 => '1.17GB
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:  #bytes < 1024
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor
    
