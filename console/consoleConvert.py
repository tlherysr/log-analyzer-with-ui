#!/usr/bin/env python

"""

convert.py

This file is going to make some checks and utilise evtx_dump.py to convert
all evtx files in the evtx_logs folder from evtx to xml.

"""

import logging
import os
import sys
from datetime import datetime
from time import process_time

from evtx_dump import xml_converter

LOG_DIR = "CI5235_Logs"
EVTX_LOGS_DIR = "evtx_logs"

# LOGGING
cwd = os.getcwd()
LOGFILE_PATH = os.path.join(cwd, LOG_DIR)
EVTX_LOGS_PATH = os.path.join(cwd, EVTX_LOGS_DIR)

# Create the logger
logger = logging.getLogger('convert_log')
logger.setLevel(logging.DEBUG)
timestamp = datetime.now().strftime("%d_%b_%Y_%H:%M:%S")


def is_logfile_exist():
    #  Logfile Check
    check = os.path.exists(LOGFILE_PATH)
    if check:
        return True
    else:
        return False

def create_logfile_directory():
    os.mkdir(LOGFILE_PATH)

def check_xml_files(path=EVTX_LOGS_PATH):
    # Check if any .xml file exists in the directories
    xml_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".xml" in file:
                file_path = os.path.join(root, file)
                xml_files.append(file_path)
    return xml_files

def delete_xml_files(xml_files):
    for xml_file in xml_files:
        os.remove(xml_file)

def read_evtx_files(progress_bar):
    c = 0
    folders = [f for f in os.scandir(EVTX_LOGS_PATH) if f.is_dir()]
    for folder in folders:
        files = [f for f in os.scandir(folder.path)]
        for file in files:
            xml_converter(file.path)
            progress_bar.display_message(message=file.name)
            progress_bar.progress(c)
            c += 1
