# 🖥️ System Monitor

A real-time system monitoring tool built with **Python**, **psutil**, and **Rich**.

System Monitor is a lightweight terminal-based application that displays important system information in a clean, organized, and continuously updating dashboard.

## 🚀 Features

- **CPU Monitoring** — Track CPU utilization and system load.
- **RAM Monitoring** — Monitor memory usage in real time.
- **Disk Monitoring** — Display disk usage, available space, and total storage.
- **Network Monitoring** — Track sent and received data.
- **Network Speed** — Monitor upload and download speeds.
- **IP Address** — Display local network information.
- **Live Dashboard** — Automatically refresh system statistics every 3 seconds.
- **Terminal Interface** — Beautiful tables and layouts powered by Rich.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| psutil | Collect system performance metrics |
| Rich | Build a modern terminal interface |
| time | Manage monitoring intervals |

## 📦 Installation

**1. Clone the repository**

`git clone https://github.com/Eldar1of1/system-monitor.git`

**2. Navigate to the project directory**

`cd system-monitor`

**3. Install dependencies**

`pip install psutil rich`

**4. Run the application**

`python3 monitor.py`

*Replace main.py with your script's filename if different.*

## ⚙️ How It Works

The application uses the psutil library to retrieve system performance metrics such as CPU usage, memory consumption, disk statistics, and network activity.

Rich is responsible for formatting and displaying this information in a structured terminal dashboard.

The dashboard automatically updates every 3 seconds using Rich's Live functionality, allowing users to observe changes without restarting the application.

Network transfer speeds are calculated by comparing the number of bytes sent and received between consecutive measurements.

## 🎯 Project Goals

This project was developed to strengthen practical skills in:

- Python programming and modular code organization
- System resource monitoring
- Working with operating system statistics
- Network traffic analysis
- Real-time terminal interfaces
- Fundamentals of system administration and DevOps


## 👨‍💻 Author

**Eldar Karaev**

Computer Engineering Student | Python & DevOps Enthusiast

GitHub: https://github.com/Eldar1of1

## 📄 License

This project is intended for educational purposes and personal development.
