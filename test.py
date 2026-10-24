
import psutil
from rich import print
from rich.table import Table

processes = []

for p in psutil.process_iter(["pid", "name", "memory_info"]):
    info = p.info
    if info["memory_info"]:
        ram = info["memory_info"].rss / 1024**2
        processes.append((info["pid"], info["name"] or "Unknown", ram))

processes.sort(key=lambda x: x[2], reverse=True)

table = Table("PID", "Process", "RAM", title="TOP 5 PROCESSES")

for pid, name, ram in processes[:5]:
    table.add_row(str(pid), name, f"{ram:.2f} MiB")

print(table)
