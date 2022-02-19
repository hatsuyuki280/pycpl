#!/bin/env python3
from libs.remote_info import *
from libs.sshlib import *
import json

class Host:
    def __init__(quq, hostname, username, password,port=22):
        quq.hostname = hostname
        quq.port = port
        quq.username = username
        quq.password = password
        quq.ssh = open_ssh(hostname, port, username, password)
        quq.osVersion = get_OS_Version(quq.ssh)
        quq.cpuInfo = get_CPU_Info(quq.ssh)
        quq.cpuUsage = get_CPU_Usage(quq.ssh)
        quq.memoryInfo = get_Memory_Info(quq.ssh)
        quq.memoryUsage = quq.__parse_MemUsage()
        quq.diskUsage = get_Disk_Usage(quq.ssh)
        quq.diskBandwidth = get_Disk_Bandwidth(quq.ssh)
        quq.ipv4Info = get_Network_IP(quq.ssh, 4)
        quq.ipv6Info = get_Network_IP(quq.ssh, 6)
        quq.networkBandwidth = get_Network_Bandwidth(quq.ssh)

    def __parse_MemUsage(quq) -> dict:
        return {'MemTotal':int(quq.memoryInfo['MemTotal'].split()[0])/1024,
                'MemFree':int(quq.memoryInfo['MemFree'].split()[0])/1024,
                'Buffers':int(quq.memoryInfo['Buffers'].split()[0])/1024,
                'Cached':int(quq.memoryInfo['Cached'].split()[0])/1024,
                'SwapTotal':int(quq.memoryInfo['SwapTotal'].split()[0])/1024,
                'SwapFree':int(quq.memoryInfo['SwapFree'].split()[0])/1024
                }

    def __str__(quq) -> str:
        return '''
        Hostname: {}
        OS Version: {}
        CPU Info: {}
        CPU Usage: {}
        Memory Info: {}
        Memory Usage(M): {}
        Disk Usage: {}
        Disk Bandwidth: {}
        IPv4 Info: {}
        IPv6 Info: {}
        Network Bandwidth: {}
        '''.format(json.dumps(quq.hostname),
                   json.dumps(quq.osVersion),
                   json.dumps(quq.cpuInfo),
                   json.dumps(quq.cpuUsage),
                   json.dumps(quq.memoryInfo),
                   json.dumps(quq.memoryUsage),
                   json.dumps(quq.diskUsage),
                   json.dumps(quq.diskBandwidth),
                   json.dumps([i.compressed for i in quq.ipv4Info]),
                   json.dumps([i.compressed for i in quq.ipv6Info]),
                   json.dumps(quq.networkBandwidth))

    def push(quq, localpath, remotepath) -> object:
        quq.pushed = push_ssh(quq.ssh, localpath, remotepath)
        return quq
    def get(quq, remotepath, localpath) -> object:
        quq.getted = get_ssh(quq.ssh, remotepath, localpath)
        return quq

    def distory(quq):
        close_ssh(quq.ssh, quq.hostname, quq.port)
        del quq
        return None