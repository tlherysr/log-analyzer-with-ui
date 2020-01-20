#!/usr/bin/env python

"""

visualise.py 

This script is going to find every xml file in evtx_logs/ folder and compare the EventID tags
with the given list.

"""

import os
import sys
import logging
from datetime import datetime
import xml.dom.minidom as xml

LOG_DIR = "CI5235_Logs"
EVTX_LOGS_DIR = "evtx_logs"

### LOGGING
cwd = os.getcwd()
LOGFILE_PATH = os.path.join(cwd, LOG_DIR)
EVTX_LOGS_PATH = os.path.join(cwd, EVTX_LOGS_DIR)

EVENT_ID_LIST = [1102, 4611, 4624, 4634, 4648, 4661, 4662, 4663, 4672, 4673, 4688, 4698, 4699, 4702, 4703, 4719, 4732, 4738, 4742, 4776, 4798, 4799, 4985, 5136, 5140, 5142, 5156, 5158]

### Create the logger
logger = logging.getLogger('analyse_log')
logger.setLevel(logging.DEBUG)
timestamp = datetime.now().strftime("%d_%b_%Y_%H:%M:%S")

def searchXMLFiles():
    print("[+] Searching for XML files now.")
    
    xmlFiles = list()
    for root, _, files in os.walk(EVTX_LOGS_DIR):
        for file in files:
            if file.endswith(".xml"):
                xmlFiles.append(os.path.join(root, file))

    return xmlFiles

def parseXMLFiles(xmlFiles):
    eventIDCounter = 0
    matchedEventIDCounter = 0
    for xmlFile in xmlFiles:
        doc = xml.parse(xmlFile)
        eventIDs = doc.getElementsByTagName("EventID")
        for eventID in eventIDs:
            eventID = eventID.firstChild.data
            eventIDCounter += 1
            logger.info("File Source: {fileSource}".format(fileSource=xmlFile))
            if int(eventID) in EVENT_ID_LIST:
                matchedEventIDCounter += 1
                logger.info("MATCHED Event ID: {EventID}".format(EventID=int(eventID)))
                dateTime = datetime.now().strftime("%Y-%b-%d %H:%M:%S.%f")
                logger.info("Date and Time: {date}".format(date=dateTime))
                logger.info("")
            else:
                logger.info("No Match For Event ID: {EventID}".format(EventID=int(eventID)))
                dateTime = datetime.now().strftime("%Y-%b-%d %H:%M:%S.%f")
                logger.info("Date and Time: {date}".format(date=dateTime))
                logger.info("")
        logger.info('')
    logger.info('')

    return eventIDCounter, matchedEventIDCounter

def main():
    
    # create file handler which logs even debug messages
    logfile = os.path.join(LOGFILE_PATH, "analyse_log_"+timestamp)
    fh = logging.FileHandler(filename=logfile, mode='w+')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("LOG DATE and TIME: {timestamp}".format(timestamp=timestamp))
    logger.info("")

    xmlFiles = searchXMLFiles()
    eventIDCounter, matchedEventIDCounter = parseXMLFiles(xmlFiles)

    # Print Summary
    logger.info("ANALYSIS SUMMARY:")
    logger.info("{noOfLogFiles} log files analysed.".format(noOfLogFiles=len(xmlFiles)))
    logger.info("{noOfEventID} Event IDs found.".format(noOfEventID=eventIDCounter))
    logger.info("{noOfMatchedEventID} Event IDs matched in Event ID List.".format(noOfMatchedEventID=matchedEventIDCounter))

if __name__ == "__main__":
    main()