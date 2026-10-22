from os.path import split
import psutil
import time
from rich import console
from rich.columns import Columns
from rich.console import Console
from rich.table import Table, Column
from rich.live import Live
from rich.panel import Panel


console = Console()

def show_info():
    table = Table(
        title="CPU-RAM INFO" ,
        width=30 ,
        border_style= "bright_blue" ,
        title_style= "bold green " ,
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
        border_style="yellow" ,
        title_style= "bold green" ,
    )
    disk_table.add_column("Component")
    disk_table.add_column("Usage")
    disk_info = psutil.disk_usage("/System/Volumes/Data")
    disk_table.add_row("TOTAL" , f"{disk_info.total / 1024**3:.2f}GB")
    disk_table.add_row("USED" , f"{disk_info.used / 1024**3:.2f}GB")
    disk_table.add_row("FREE" , f"{disk_info.free / 1024**3:.2f}GB")
    disk_table.add_row("USAGE" , f"{disk_info.percent}%")




    return Columns([table , disk_table] , padding=2)


def show_network_info():
    net_info = psutil.net_io_counters()
    print("-" * 100)
    print("Sent -",conver_bytes(net_info.bytes_sent))
    print("Got -",conver_bytes(net_info.bytes_recv))
    print("-" * 100)
    time.sleep(3)


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
            time.sleep(3)
            live.update(show_info())



if __name__ == "__main__":
    main()
