#!/bin/env python3
from telnetlib import IP
from urllib import response
from libs.sshlib import *
import ipaddress

def get_OS_Version(quq) -> dict:
    osVersion = exec_ssh(quq, 'cat /etc/os-release')
    osVersion = [i.replace('\n','') for i in osVersion]
    osVersion = [i.replace('"','') for i in osVersion]
    osVersion = [i.split('=') for i in osVersion]
    osVersion = {i[0].strip(): i[1].strip() for i in osVersion}
    return osVersion

def get_CPU_Info(quq) -> dict:
    cpuInfo = exec_ssh(quq, 'lscpu')
    cpuInfo = [i.replace('\n','') for i in cpuInfo]
    cpuInfo = [i.replace('\t','') for i in cpuInfo]
    cpuInfo = [i.split(':') for i in cpuInfo]
    cpuInfo = {i[0].strip(): i[1].strip() for i in cpuInfo}
    return cpuInfo

def get_CPU_Usage(quq):
    cpuUsage = exec_ssh(quq, 'top -b -n 1 | grep "Cpu(s)"')
    cpuUsage = [i.replace('\n','') for i in cpuUsage]
    cpuUsage = [i.split() for i in cpuUsage]
    cpuUsage = {i[0].strip(): i[1].strip() for i in cpuUsage}
    return cpuUsage

def get_Memory_Info(quq) -> dict:
    memoryInfo = exec_ssh(quq, 'cat /proc/meminfo')
    memoryInfo = [i.replace('\n','') for i in memoryInfo]
    memoryInfo = [i.split(':') for i in memoryInfo]
    memoryInfo = {i[0].strip(): i[1].strip() for i in memoryInfo}
    return memoryInfo

def get_Disk_Usage(quq):
    diskUsage = exec_ssh(quq, 'df -hm | grep -v loop | grep -v tmpfs | grep -v udev | grep -v boot')
    diskUsage = [i.replace('\n','') for i in diskUsage]
    diskUsage = [i.split() for i in diskUsage][1:]
    diskUsage = {i[0].strip(): {'cap(M)':i[1].strip(),'used(M)':i[2].strip(),'avail(M)':i[3].strip(),'use%':i[4].strip().replace('%',''),'mount':i[5].strip()} for i in diskUsage}
    return diskUsage

def get_Disk_Bandwidth(quq):
    diskBandwidth = exec_ssh(quq, 'cat /proc/diskstats | grep -v "loop" | grep -v "tmpfs" | grep -v "udev" | grep -v "boot"')
    diskBandwidth = [i.replace('\n','') for i in diskBandwidth]
    diskBandwidth = [i.split() for i in diskBandwidth]
    diskBandwidth = {i[2].strip(): {'r/s':i[3].strip(),'w/s':i[7].strip(),'r/s(%)':i[5].strip(),'w/s(%)':i[9].strip()} for i in diskBandwidth}
    return diskBandwidth

def get_Network_IP(quq, protocol=4):
    response = exec_ssh(quq, 'hostname -I')
    response = [i.replace('\n','') for i in response]
    response = [i.split() for i in response][0]
    IP = [ipaddress.ip_address(i) for i in response]
    return [i for i in IP if i.version == protocol]

def get_Network_Bandwidth(quq):
    networkBandwidth = exec_ssh(quq, 'cat /proc/net/dev')
    networkBandwidth = [i.replace('\n','') for i in networkBandwidth]
    networkBandwidth = [i.replace('|','') for i in networkBandwidth]
    networkBandwidth = [i.replace('\t','') for i in networkBandwidth]
    networkBandwidth = [i.replace('-','') for i in networkBandwidth]
    networkBandwidth = [i.split() for i in networkBandwidth][2:]
    networkBandwidth = {i[0].strip(): {'r/s':i[1].strip(),'w/s':i[9].strip(),'r/s(%)':i[3].strip(),'w/s(%)':i[11].strip()} for i in networkBandwidth}
    return networkBandwidth
