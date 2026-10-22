import psutil

def memory():
    disk = psutil.disk_usage('/System/Volumes/Data')
    total = disk.total / 1024**3
    used = disk.used / 1024**3
    free = disk.free / 1024 **3
    usege = disk.percent
    print(usege)
    print(f"Total - {total:.2f}GB\nUsed - {used:.2f}GB\nFree - {free:.2f}GB")

memory()