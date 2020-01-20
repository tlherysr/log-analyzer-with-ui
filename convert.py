#!/usr/bin/env python

"""

convert.py

This file is going to make some checks and utilise evtx_dump.py to convert
all evtx files in the evtx_logs folder from evtx to xml.

"""

import os
import sys
import logging
from time import process_time
from datetime import datetime
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
        print("[+] Your log directory: {} exists. So let's keep going.".format(LOG_DIR))
    else:
        print("[+] Your log directory does not exist. So it has been created for you.")
        os.mkdir(LOGFILE_PATH)


def check_xml_files(path=EVTX_LOGS_PATH):
    # Check if any .xml file exists in the directories
    xml_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".xml" in file:
                file_path = os.path.join(root, file)
                xml_files.append(file_path)

    if xml_files:
        print("[-] It has been found that .xml files exist in your evtx_logs folders.")
        print("[?] Would you want me to delete all of them for you now?")
        answer = input("[?] Y for Yes N for NO\n")
        if answer == "Y" or answer == "y":
            for xml_file in xml_files:
                os.remove(xml_file)
            print("[+] Deleted!")
        elif answer == "N" or answer == "n":
            print(
                "[-] Process can not start if you don't remove .xml files! Do it manually or let the script to do it "
                "for you!")
            sys.exit(1)
        else:
            print("[-] Please press Y or N!")
            sys.exit(1)
    else:
        pass


def read_evtx_files():
    logger.debug("LOG DATE and TIME: {timestamp}".format(timestamp=timestamp))
    logger.info('')
    print("[+] Starting to read evtx logs...\n")
    print("A log file for this xml conversion session will be saved to a folder called 'CI5235_Logs'.")
    print(timestamp)
    print("CONVERSION PROCESS STARTED")
    print()

    folders = [f for f in os.scandir(EVTX_LOGS_PATH) if f.is_dir()]
    for counter, folder in enumerate(folders, 1):
        logger.info("{}: Working in the {} folder:".format(counter, folder.name))

        files = [f for f in os.scandir(folder.path)]
        for file in files:
            logger.info(
                "Convert {} from evtx to xml format, started...".format(file.name))
            try:
                xml_converter(file.path)
                logger.info("Converted successfully!")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        logger.info('')


def main():
    startTime = process_time()
    print("[*] First of all let's do some checks.")

    # Check if the required logfile exist. If not, create it.
    is_logfile_exist()

    # create file handler which logs even debug messages
    logfile = os.path.join(LOGFILE_PATH, "convert_log_" + timestamp)
    fh = logging.FileHandler(filename=logfile, mode='w+')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Read all evtx files in evtx_logs directory.
    print("[+] Checking is there any .xml file in your evtx_logs directories and subdirectories...")
    check_xml_files()

    # Count folders and files
    folder_counter = sum([len(folder) for p, folder, f in os.walk(EVTX_LOGS_PATH)])
    file_counter = sum([len(files) for r, d, files in os.walk(EVTX_LOGS_PATH)])

    # Convert EVTX file to xml files
    read_evtx_files()

    # Print summary
    logger.info("SUMMARY OF CONVERSION PROCESS!")
    logger.info("Folder Count: {}".format(folder_counter))
    logger.info("File Count: {}".format(file_counter))
    runningTime = process_time() - startTime
    logger.info("The time to complete this conversion was: {}".format(runningTime))


if __name__ == "__main__":
    main()
