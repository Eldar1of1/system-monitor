import psutil
import time
from rich.columns import Columns
from rich.table import Table
from rich.live import Live
import socket
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.console import Group

console = Console()


def show_info():

    header = Panel(
        Align.center("[bright_white]System Information[/bright_white]"),
        border_style="bright_black",
        height=3
    )

    table = Table(
        title="CPU-RAM INFO" ,
        width=30 ,
        border_style= "light_sky_blue1" ,
        title_style= "bright_white" ,
    )
    table.add_column("Component")
    table.add_column("Usage")
    ram_info = psutil.virtual_memory().percent
    table.add_row("RAM", f"{ram_info}%")
    cpu_info = psutil.cpu_percent()
    table.add_row("CPU",f"{cpu_info}%")

    disk_table = Table(
        title= "DISK INFO" ,
        width=30 ,
        border_style="light_sky_blue1" ,
        title_style= "bright_white" ,
    )
    disk_table.add_column("Component")
    disk_table.add_column("Usage")
    disk_info = psutil.disk_usage("/System/Volumes/Data")
    disk_table.add_row("TOTAL" , f"{disk_info.total / 1024**3:.2f}GB")
    disk_table.add_row("USED" , f"{disk_info.used / 1024**3:.2f}GB")
    disk_table.add_row("FREE" , f"{disk_info.free / 1024**3:.2f}GB")
    disk_table.add_row("USAGE" , f"{disk_info.percent}%")

    net_table = Table(
        title="NETWORK INFO" ,
        width=45,
        border_style="light_sky_blue1" ,
        title_style="bright_white"
    )

    pid_table = Table(
        title="PID INFO",
        width=45,
        border_style="light_sky_blue1",
        title_style="bright_white"
    )

    pid_table.add_column("PID")
    pid_table.add_column("NAME")
    pid_table.add_column("RAM USAGE")

    def show_pid_info():
        processes = []
        for proc in psutil.process_iter():
            try:
                name = proc.name()
                pid = proc.pid
                ram = proc.memory_info().rss / 1024 ** 2  # MiB
                processes.append((name, pid, ram))
            except(psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda x: x[2], reverse=True)

        for name, pid, ram in processes[:10]:
            pid_table.add_row(name, str(pid), f"{ram/1024:.2f}GB")

    show_pid_info()


    def get_ip():
        ip_addr = psutil.net_if_addrs()
        for addr in ip_addr.get("en0", []):
            if addr.family == socket.AF_INET:
                return addr.address


    def get_Download_Speed():
        before = psutil.net_io_counters().bytes_recv
        time.sleep(3)
        after = psutil.net_io_counters().bytes_recv
        total_speed = (after - before) / 3 / 1_000_000
        return f"{total_speed:.2f} Mb/s"

    net = psutil.net_io_counters()

    net_table.add_column("COMPONENT")
    net_table.add_column("INFO")
    net_table.add_row("IP" , f"{get_ip()}")
    net_table.add_row("DOWNLOAD SPEED" , f"{get_Download_Speed()}") # Download Speed
    net_table.add_row("BYTES SENT" , f"{conver_bytes(net.bytes_sent)}")
    net_table.add_row("BYTES RECEIVED" , f"{conver_bytes(net.bytes_recv)}")

    def show_board():
        pass

    return Group(header,Columns([table , disk_table , net_table , pid_table] , padding=2))


def conver_bytes(size):
    if size >= 1_000_000_000:
        return f"{size /1_000_000_000:.2f} GB."
    elif size >= 1_000_000 :
        return f"{size / 1_000_000:.2f} MB."
    elif size >= 1_000 :
        return f"{size / 1_000:.2f} KB."
    else :
        return f"{size} Bytes."


def main():
    with Live(show_info(),refresh_per_second=1) as live:
        while True:
            time.sleep(1)
            live.update(show_info())




if __name__ == "__main__":
    main()
