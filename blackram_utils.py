import os
import platform

param_dict = {}

def get_param_config():
    file = open("/home/bhanureddy/Python/PythonScripts/param_config.txt", "r")
    for config in file.readlines():
        temp_holder = config.split('=')
        param_dict[str(temp_holder[0].strip())] = str(temp_holder[1].strip())

def get_param_value(value):
    get_param_config()
    return param_dict[value]

#Checking the OS

def checkOS():
    if platform.system()=='Windows':
        return "WIN"
    elif platform.system()=='Darwin':
        return "MAC"
    elif platform.system()=='Linux':
        return "LIN"
