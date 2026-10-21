from os.path import split
import psutil
import time
from rich import console
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel


console = Console()


def show_ram_cpu_info():
    table = Table(
        title="SYSTEM INFO" ,
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

    return table




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
    with Live(show_ram_cpu_info(),refresh_per_second=1) as live:
        while True:
            time.sleep(3)
            live.update(show_ram_cpu_info())



main()
