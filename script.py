import psycopg2
import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Version: {uname.version}")

systeem = f"{uname.system}"
naam = f"{uname.node}"
versie = f"{uname.version}"

# Boot Time
print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

# let's print CPU information
print("="*40, "CPU Info", "="*40)
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

fysieke_cores = psutil.cpu_count(logical=False)
totale_cores = psutil.cpu_count(logical=True)
cpu_gebruik = f"{psutil.cpu_percent()}"


# Memory Information
print("="*40, "Memory Information", "="*40)
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")

totaal_geheugen = f"{get_size(svmem.total)}"
beschikbaar_geheugen = f"{get_size(svmem.available)}"
gebruikt_geheugen = f"{get_size(svmem.used)}"
procent_gebruikt = f"{svmem.percent}"

# Disk Information
print("="*40, "Disk Information", "="*40)
partitions = psutil.disk_partitions()
for partition in partitions:
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue

    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")

totaal_opslag = f"{get_size(partition_usage.total)}"
gebruikt_opslag = f"{get_size(partition_usage.used)}"
beschikbaar_opslag = f"{get_size(partition_usage.free)}"
procent_gebruikto = f"{partition_usage.percent}"

con = psycopg2.connect(
             host='192.168.3.1',
             database='datapool',
             user='postgres',
             password='Wachtwoord1')

cur = con.cursor()
cur.execute("insert into cpu_info (fisieke_cores, totale_cores, cpu_gebruik) values(%s, %s, %s)", (fysieke_cores, totale_cores, cpu_gebruik))
cur.execute("insert into systeem_info (systeem, naam, versie) values(%s, %s, %s)", (systeem, naam, versie))
cur.execute("insert into geheugen (totaal_geheugen, beschikbaar_geheugen, gebruikt_geheugen, procent_gebruikt) values(%s, %s, %s, %s)", (totaal_geheugen, beschikbaar_geheugen, gebruikt_geheugen, procent_gebruikt))
cur.execute("insert into opslag (totaal_opslag, gebruikt_opslag, beschikbaar_opslag, procent_gebruikt) values(%s, %s, %s, %s)", (totaal_opslag, gebruikt_opslag, beschikbaar_opslag, procent_gebruikto))
con.commit()
cur.close()
con.close()
