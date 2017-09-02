import os
import psutil

def memory_usage_psutil():
    process = psutil.Process(os.getpid())
    mem = process.memory_percent()
    return mem

def cpu_usage_psutil():
    process = psutil.Process(os.getpid())
    cpu = process.cpu_percent()
    return cpu

while True:
	print(memory_usage_psutil())
	print(cpu_usage_psutil())