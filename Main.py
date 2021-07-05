import GPUtil
import psutil
import platform
import speedtest
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from datetime import datetime

class SystemScanner(object):
    def get_size(self, bytes, suffix="B"):
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
    
    def ram_info(self):
        svmem = psutil.virtual_memory()
        data = {
            "Total":        self.get_size(svmem.total),
            "Available":    self.get_size(svmem.available),
            "Used":         self.get_size(svmem.used),
            "Percentage":   str(f"{svmem.percent}%")
        }
        return data
    
    def gpu_info(self):
        gpus = GPUtil.getGPUs()
        data = {}
        for gpu in gpus:
            data["ID"] = gpu.id
            data["Name"] = gpu.name
            data["Load"] = f"{gpu.load*100}%"
            data["Free"] = f"{gpu.memoryFree} MB"
            data["Used"] = f"{gpu.memoryUsed} MB"
            data["Total"] = f"{gpu.memoryTotal} MB"
            data["Temp"] = f"{gpu.temperature} °C"
            data["UUID"] = gpu.uuid
        return data
    
    def disk_info(self):
        drive = psutil.disk_partitions()[0]
        disk_io = psutil.disk_io_counters()
        try:
            partition_usage = psutil.disk_usage(drive.mountpoint)
        except PermissionError:
            pass
        data = {
            "Device":       drive.device,
            "Mountpoint":   drive.mountpoint,
            "File System":  drive.fstype,
            "Total Size":   self.get_size(partition_usage.total),
            "Used":         self.get_size(partition_usage.used),
            "Free":         self.get_size(partition_usage.free),
            "Percentage":   str(f"{partition_usage.percent}%"),
            "Total Read":   self.get_size(disk_io.read_bytes),
            "Total Write":  self.get_size(disk_io.write_bytes)
        }
        return data
    
    def network_info(self):
        print("\nWill now do a scan, this won't take long...\n")
        scanner = psutil.net_if_addrs()
        interfaces = []
        for interface_name, _ in scanner.items():
            interfaces.append(str(interface_name))
        net_io = psutil.net_io_counters()
        speed = speedtest.Speedtest()
        data = {
            "Interface": str(interfaces[0]),
            "Download": str(f"{round(speed.download() / 1_000_000, 2)} Mbps"),
            "Upload":   str(f"{round(speed.upload() / 1_000_000, 2)} Mbps"),
            "Total Bytes Sent": str(self.get_size(net_io.bytes_sent)),
            "Total Bytes Received": str(self.get_size(net_io.bytes_recv))
        }
        return data
    
