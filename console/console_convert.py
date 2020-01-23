#!/usr/bin/env python

"""

convert.py

This file is going to make some checks and utilise evtx_dump.py to convert
all evtx files in the evtx_logs folder from evtx to xml.

"""

import os
import sys
from datetime import datetime
from time import process_time

from evtx_dump import xml_converter
from console_logger import LOGFILE_PATH, EVTX_LOGS_PATH


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

def read_evtx_files(progress_bar, logger_obj):
    startTime = process_time()
    # Count folders and files
    folder_counter = sum([len(folder) for p, folder, f in os.walk(EVTX_LOGS_PATH)])
    file_counter = sum([len(files) for r, d, files in os.walk(EVTX_LOGS_PATH)])
    
    c = 1
    folders = [f for f in os.scandir(EVTX_LOGS_PATH) if f.is_dir()]
    for counter, folder in enumerate(folders, 1):
        logger_obj.logtofile(message="{}: Working in the {} folder:".format(counter, folder.name))
        files = [f for f in os.scandir(folder.path)]
        for file in files:
            logger_obj.logtofile(message="Convert {} from evtx to xml format, started...".format(file.name))
            xml_converter(file.path)
            logger_obj.logtofile(message="Converted successfully!")
            
            progress_bar.display_message(message=file.name)
            progress_bar.progress(c)
            c += 1
        logger_obj.logtofile(message='')

    # Print summary
    logger_obj.logtofile(message="SUMMARY OF CONVERSION PROCESS!")
    logger_obj.logtofile(message="Folder Count: {}".format(folder_counter))
    logger_obj.logtofile(message="File Count: {}".format(file_counter))
    runningTime = process_time() - startTime
    logger_obj.logtofile(message="The time to complete this conversion was: {}".format(runningTime))

