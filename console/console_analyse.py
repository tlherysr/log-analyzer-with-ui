#!/usr/bin/env python

"""

visualise.py 

This script is going to find every xml file in evtx_logs/ folder and compare the EventID tags
with the given list.

"""

import logging
import os
import xml.dom.minidom as xml
from datetime import datetime

from console_logger import LOGFILE_PATH, EVTX_LOGS_PATH, EVTX_LOGS_DIR

EVENT_ID_LIST = [1102, 4611, 4624, 4634, 4648, 4661, 4662, 4663, 4672, 4673, 4688, 4698, 4699, 4702, 4703, 4719, 4732, 4738, 4742, 4776, 4798, 4799, 4985, 5136, 5140, 5142, 5156, 5158]

def search_xml_files():
    xml_files = []
    for root, _, files in os.walk(EVTX_LOGS_DIR):
        for file in files:
            if file.endswith(".xml"):
                xml_files.append(os.path.join(root, file))

    return xml_files

def parse_xml_files(xml_files, analyse_page, logger_obj):
    eventIDCounter = 0
    matchedEventIDCounter = 0
    c = 1
    for xml_file in xml_files:
        doc = xml.parse(xml_file)
        eventIDs = doc.getElementsByTagName("EventID")
        for eventID in eventIDs:
            eventID = eventID.firstChild.data
            eventIDCounter += 1
            logger_obj.logtofile(message="File Source: {fileSource}".format(fileSource=xml_file))
            if int(eventID) in EVENT_ID_LIST:
                matchedEventIDCounter += 1
                logger_obj.logtofile(message="MATCHED Event ID: {EventID}".format(EventID=int(eventID)))
                date_time = datetime.now().strftime("%Y-%b-%d %H:%M:%S.%f")
                logger_obj.logtofile(message="Date and Time: {date}".format(date=date_time))
                logger_obj.logtofile(message="")
            else:
                logger_obj.logtofile(message="No Match For Event ID: {EventID}".format(EventID=int(eventID)))
                date_time = datetime.now().strftime("%Y-%b-%d %H:%M:%S.%f")
                logger_obj.logtofile(message="Date and Time: {date}".format(date=date_time))
                logger_obj.logtofile(message="")
        analyse_page.progress(c)
        c += 1
        
        logger_obj.logtofile(message="")
    logger_obj.logtofile(message="")

    
    # Print Summary
    logger_obj.logtofile(message="ANALYSIS SUMMARY:")
    logger_obj.logtofile(message="{noOfLogFiles} log files analysed.".format(noOfLogFiles=len(xml_files)))
    logger_obj.logtofile(message="{noOfEventID} Event IDs found.".format(noOfEventID=eventIDCounter))
    logger_obj.logtofile(message="{noOfMatchedEventID} Event IDs matched in Event ID List.".format(noOfMatchedEventID=matchedEventIDCounter))