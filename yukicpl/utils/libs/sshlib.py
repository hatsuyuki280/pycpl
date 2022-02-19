#!/bin/env python3
import logging
import random
import paramiko

def open_ssh(host, port, username, password):
    try:
        quq = paramiko.SSHClient()
        quq.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        quq.connect(host, port, username, password)
    except Exception as e:
        logging.error(f'failed to connect to {host}:{port}', e)
        return None
    logging.info(f'connected to {host}:{port}')
    return quq

def exec_ssh(quq, command):
    try:
        logging.info(f'try to execute command: {command}')
        stdin, stdout, stderr = quq.exec_command(command)
    except Exception as e:
        logging.error(f'failed to execute command: {command}', e)
        return None    
    if stderr.channel.recv_exit_status() != 0:
        logging.error(f'failed to execute command: {command}', e)
        return None
    return stdout.readlines()

def push_ssh(quq, localpath, remotepath) -> bool:
    try:
        sftp = quq.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()
    except Exception as e:
        logging.error(f'failed to push {localpath} to {remotepath}', e)
        return False
    logging.info(f'{localpath} pushed to {remotepath}')
    return True

def get_ssh(quq, remotepath, localpath) -> bool:
    try:
        sftp = quq.open_sftp()
        sftp.get(remotepath, localpath)
        sftp.close()
    except Exception as e:
        logging.error(f'failed to get {remotepath} to {localpath}', e)
        return False
    logging.info(f'{remotepath} pulled to {localpath}')
    return True


def close_ssh(quq, host, port):
    try:
        logging.info(f'try to close ssh connection: {host}:{port}')
        quq.close()
    except Exception as e:
        logging.error(f'failed to close ssh connection: {host}:{port}', e) 
        return False
    logging.info(f'ssh connection closed: {host}:{port}')
    return True