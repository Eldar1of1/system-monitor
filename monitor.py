import pathlib

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
import speedtest
from threading import Event, Lock, Thread
from pathlib import Path


console = Console()


class PingMonitor:

    def __init__(self, interval=10):
        self.interval = interval
        self._value = "Measuring..."
        self._lock = Lock()
        self._stop = Event()
        self._thread = Thread(target=self._run, daemon=True)

    @property
    def value(self):
        with self._lock:
            return self._value

    def start(self):
        self._thread.start()

    def close(self):
        self._stop.set()
        self._thread.join(timeout=0.1)

    def _run(self):
        while not self._stop.is_set():
            try:
                test = speedtest.Speedtest(
                    secure=True, timeout=3, shutdown_event=self._stop
                )
                test.get_best_server()
                value = f"{test.results.ping:.2f} ms"
            except Exception:
                value = "Unavailable (retrying...)"

            with self._lock:
                self._value = value

            if self._stop.wait(self.interval):
                break


def measure(name , func):
    start = time.perf_counter()
    result = func()
    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed:.3f} секунд")
    return result


def usage_bar(percent, width=20):
    filled = round(percent / 100 * width)
    empty = width - filled

    if percent < 60:
        color = "green"
    elif percent < 80:
        color = "yellow"
    else:
        color = "red"

    return (f"[{color}]{'█' * filled}[/]"
            f"[dim]{"░" * empty} [/]"
            f"[bold white]{percent:.1f}%"
            )

def show_info(ping="Measuring..."):

    top = Columns([])


    header = Panel(
        Align.center("[bright_white]System Information[/bright_white]"),
        border_style="bright_black",
        height=3
    )

    table = Table(
        title="CPU" ,
        expand= True ,
        border_style= "light_sky_blue1" ,
        title_style= "bright_white" ,
    )

    ram_table = Table(
        title="RAM" ,
        expand= True,
        border_style= "light_sky_blue1" ,
        title_style= "bright_white"  ,
    )

    def show_ram():
        ram_info = psutil.virtual_memory().percent
        return ram_info

    def show_cpu():
        cpu_info = psutil.cpu_percent()
        return cpu_info


    table.add_column("Component")
    table.add_column("Usage")

    ram_table.add_column("Component")
    ram_table.add_column("Usage")

    ram_table.add_row("RAM" , usage_bar(show_ram()))

    table.add_row("CPU",usage_bar(show_cpu()))

    disk_table = Table(
        title= "DISK INFO" ,
        expand= True,
        border_style="light_sky_blue1" ,
        title_style= "bright_white" ,
    )


    disk_table.add_column("Component")
    disk_table.add_column("Usage")

    disk_info = psutil.disk_usage(str(Path.home()))
    disk_table.add_row("TOTAL" , f"{disk_info.total / 1024**3:.2f}GB")
    disk_table.add_row("USED" , f"{disk_info.used / 1024**3:.2f}GB")
    disk_table.add_row("FREE" , f"{disk_info.free / 1024**3:.2f}GB")
    disk_table.add_row("USAGE" , usage_bar(disk_info.percent))

    net_table = Table(
        title="NETWORK INFO" ,
        expand= True,
        border_style="light_sky_blue1" ,
        title_style="bright_white"
    )

    pid_table = Table(
        title="PID INFO",
        expand=True,
        border_style="light_sky_blue1",
        title_style="bright_white"
    )

    pid_table.add_column("NAME")
    pid_table.add_column("PID")
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
        interface = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for name , adresses in interface.items():
            if name not in stats or stats[name].isup:
                continue

            for addr in adresses:
                if addr.family == socket.AF_INET:
                    if not addr.address.startswith(("127.", "169.254.")):
                        return addr.address

                    return "Unavailable"



    def get_Download_Speed():
        before = psutil.net_io_counters().bytes_recv
        time.sleep(2)
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
    net_table.add_row("PING", ping)
    #net_table.add_row("SPEED" , show_dowln_speed())



    def show_board():
        top = Table.grid(expand=True, padding=(0, 1))

        top.add_column(ratio=1)
        top.add_column(ratio=1)

        top.add_row(table, ram_table)

        middle = Table.grid(expand=True, padding=(0, 1))

        middle.add_column(ratio=1)
        middle.add_column(ratio=1)

        middle.add_row(disk_table, net_table)

        return Group(
            header,
            top,
            middle,
            pid_table
        )

    return show_board()


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
    ping = PingMonitor()
    ping.start()
    try:
        with Live(show_info(ping.value), refresh_per_second=1, screen=True) as live:
            while True:
                time.sleep(3)
                live.update(show_info(ping.value))
    except KeyboardInterrupt:
        pass
    finally:
        ping.close()




if __name__ == "__main__":
    main()

