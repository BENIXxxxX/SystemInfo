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
    
class GUI(object):
    def __init__(self, master):
        spec = SystemScanner()
        self.methods = {
            "sys":      spec.system_info(),
            "cpu":      spec.cpu_info(),
            "ram":      spec.ram_info(),
            "gpu":      spec.gpu_info(),
            "disk":     spec.disk_info(),
            "network":  spec.network_info()
        }

        frame = Frame(master)
        frame.grid()
        tabControl = ttk.Notebook(root)
        tabControl.configure(width=485, height=290)

        self.system_tab = ttk.Frame(tabControl)
        tabControl.add(self.system_tab, text="System")
        tabControl.grid()

        self.cpu_tab = ttk.Frame(tabControl)
        tabControl.add(self.cpu_tab, text="CPU")
        tabControl.grid()

        self.ram_tab = ttk.Frame(tabControl)
        tabControl.add(self.ram_tab, text="RAM")
        tabControl.grid()

        self.gpu_tab = ttk.Frame(tabControl)
        tabControl.add(self.gpu_tab, text="GPU")
        tabControl.grid()

        self.disk_tab = ttk.Frame(tabControl)
        tabControl.add(self.disk_tab, text="Disk")
        tabControl.grid()

        self.network_tab = ttk.Frame(tabControl)
        tabControl.add(self.network_tab, text="Network")
        tabControl.grid()

        self.style = ttk.Style(frame)
        self.style.configure("My.TLabel", font=("Arial", 12, "bold"))
        self.style.configure("Bold.TLabel", font=("Arial", 10, "bold"))
        self.style.configure("Title.TLabel", font=("Arial", 15, "bold"))

        self.widgets()
    
    def widgets(self):
        # System Tab
        sys_frame_top_label = LabelFrame(self.system_tab, width=480, height=50)
        sys_frame_top_label.grid(column=0, row=0)
        sys_frame_top_label.grid_propagate(0)

        sys_top_label = Label(sys_frame_top_label, text="SYSTEM SPECIFICATIONS", style="Title.TLabel")
        sys_top_label.grid(column=1, row=0, columnspan=3, sticky=E)


        sys_label_frame = LabelFrame(self.system_tab, width=480, height=240)
        sys_label_frame.grid(column=0, row=1)
        sys_label_frame.grid_propagate(0)
                
        sys_system_label = Label(sys_label_frame, text="System: ", style="My.TLabel")
        sys_system_label.grid(column=0, row=1, sticky=W)
        sys_system_spec = Label(sys_label_frame, text=self.methods["sys"]["System"], style="Bold.TLabel")
        sys_system_spec.grid(column=1, row=1, sticky=W, padx=10, pady=2)

        sys_node_label = Label(sys_label_frame, text="Node Name: ", style="My.TLabel")
        sys_node_label.grid(column=0, row=2, sticky=W)
        sys_node_spec = Label(sys_label_frame, text=self.methods["sys"]["Node Name"], style="Bold.TLabel")
        sys_node_spec.grid(column=1, row=2, sticky=W, padx=10, pady=2)
        
        sys_rel_label = Label(sys_label_frame, text="Release: ", style="My.TLabel")
        sys_rel_label.grid(column=0, row=3, sticky=W)
        sys_rel_spec = Label(sys_label_frame, text=self.methods["sys"]["Release"], style="Bold.TLabel")
        sys_rel_spec.grid(column=1, row=3, sticky=W, padx=10, pady=2)

        sys_ver_label = Label(sys_label_frame, text="Version: ", style="My.TLabel")
        sys_ver_label.grid(column=0, row=4, sticky=W)
        sys_ver_label = Label(sys_label_frame, text=self.methods["sys"]["Version"], style="Bold.TLabel")
        sys_ver_label.grid(column=1, row=4, sticky=W, padx=10, pady=2)

        sys_arch_label = Label(sys_label_frame, text="Architecture: ", style="My.TLabel")
        sys_arch_label.grid(column=0, row=5, sticky=W)
        sys_arch_spec = Label(sys_label_frame, text=self.methods["sys"]["Architecture"], style="Bold.TLabel")
        sys_arch_spec.grid(column=1, row=5, sticky=W, padx=10, pady=2)

        sys_pro_label = Label(sys_label_frame, text="Processor: ", style="My.TLabel")
        sys_pro_label.grid(column=0, row=6, sticky=W)
        sys_pro_spec = Label(sys_label_frame, text=self.methods["sys"]["Processor"], style="Bold.TLabel")
        sys_pro_spec.grid(column=1, row=6, sticky=W, padx=10, pady=2)

        sys_boot_label = Label(sys_label_frame, text="Boot Time: ", style="My.TLabel")
        sys_boot_label.grid(column=0, row=7, sticky=W)
        sys_boot_spec = Label(sys_label_frame, text=self.methods["sys"]["Boot Time"], style="Bold.TLabel")
        sys_boot_spec.grid(column=1, row=7, sticky=W, padx=10, pady=2)


        # CPU Tab
        cpu_frame_top_label = LabelFrame(self.cpu_tab, width=480, height=50)
        cpu_frame_top_label.grid(column=0, row=0)
        cpu_frame_top_label.grid_propagate(0)
        
        cpu_system_top_label = Label(cpu_frame_top_label, text="CPU", style="Title.TLabel")
        cpu_system_top_label.grid(column=1, row=0, columnspan=3, sticky=N)

        
        cpu_label_frame = LabelFrame(self.cpu_tab, width=480, height=240)
        cpu_label_frame.grid(column=0, row=1)
        cpu_label_frame.grid_propagate(0)

        cpu_core_label = Label(cpu_label_frame, text="Physical Cores: ", style="My.TLabel")
        cpu_core_label.grid(column=0, row=1, sticky=W)
        cpu_core_spec = Label(cpu_label_frame, text=self.methods["cpu"]["Physical Cores"], style="Bold.TLabel")
        cpu_core_spec.grid(column=1, row=1, sticky=W, padx=10)

        cpu_total_label = Label(cpu_label_frame, text="Total Cores: ", style="My.TLabel")
        cpu_total_label.grid(column=0, row=2, sticky=W)
        cpu_total_spec = Label(cpu_label_frame, text=self.methods["cpu"]["Total Cores"], style="Bold.TLabel")
        cpu_total_spec.grid(column=1, row=2, sticky=W, padx=10)
        
        cpu_max_label = Label(cpu_label_frame, text="Max Frequency: ", style="My.TLabel")
        cpu_max_label.grid(column=0, row=3, sticky=W)
        cpu_max_spec = Label(cpu_label_frame, text=self.methods["cpu"]["Max Frequency"], style="Bold.TLabel")
        cpu_max_spec.grid(column=1, row=3, sticky=W, padx=10)

        cpu_min_label = Label(cpu_label_frame, text="Min Frequency: ", style="My.TLabel")
        cpu_min_label.grid(column=0, row=4, sticky=W)
        cpu_min_spec = Label(cpu_label_frame, text=self.methods["cpu"]["Min Frequency"], style="Bold.TLabel")
        cpu_min_spec.grid(column=1, row=4, sticky=W, padx=10)

        cpu_cur_label = Label(cpu_label_frame, text="Current Frequency: ", style="My.TLabel")
        cpu_cur_label.grid(column=0, row=5, sticky=W)
        cpu_cur_spec = Label(cpu_label_frame, text=self.methods["cpu"]["Current Frequency"], style="Bold.TLabel")
        cpu_cur_spec.grid(column=1, row=5, sticky=W, padx=10)

        cpu_t_usage_label = Label(cpu_label_frame, text="Total Usage: ", style="My.TLabel")
        cpu_t_usage_label.grid(column=0, row=6, sticky=W)
        cpu_t_usage_spec = Label(cpu_label_frame, text=self.methods["cpu"]["Total Usage"], style="Bold.TLabel")
        cpu_t_usage_spec.grid(column=1, row=6, sticky=W, padx=10)


