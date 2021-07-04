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
    
    def system_info(self):
        uname = platform.uname()
        boot_time_stamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_stamp)
        data = {
            "System":       uname.system,
            "Node Name":    uname.node,
            "Release":      uname.release,
            "Version":      uname.version,
            "Architecture": uname.machine,
            "Processor":    uname.processor,
            "Boot Time": str(f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        }
        return data
    
    def cpu_info(self):
        cpu_freq = psutil.cpu_freq()
        data = {
            "Physical Cores":   psutil.cpu_count(logical=False),
            "Total Cores":      psutil.cpu_count(logical=True),
            "Max Frequency":    str(f"{cpu_freq.max:.2f} Mhz"),
            "Min Frequency":    str(f"{cpu_freq.min:.2f} Mhz"),
            "Total Usage":      str(f"{psutil.cpu_percent()}%")
        }
        return data
    
    