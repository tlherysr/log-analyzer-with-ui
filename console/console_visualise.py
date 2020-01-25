#!/usr/bin/env python
"""
visualise.py 

This script is going to open specified log file and create a graph
according to the data in the log file.
"""

import logging
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from console_logger import LOGFILE_PATH


def find_log_files():
    analyse_logs = []
    if os.path.isdir(LOGFILE_PATH):
        for file in os.listdir(LOGFILE_PATH):
            if file.startswith('analyse_log'):
                analyse_logs.append(file)
        
        return analyse_logs
    else:
        return None

def count_EventID(logfile_path):
    logfile_path = os.path.join(LOGFILE_PATH, logfile_path)
    # Create the necessary nested dictionary structure
    EVENT_ID_DICT = {
        1102: {
            "Count": 0
        },
        4611: {
            "Count": 0
        },
        4624: {
            "Count": 0
        },    
        4634: {
            "Count": 0
        }, 
        4648: {
            "Count": 0
        }, 
        4661: {
            "Count": 0
        }, 
        4662: {
            "Count": 0
        }, 
        4663: {
            "Count": 0
        }, 
        4672: {
            "Count": 0
        }, 
        4673: {
            "Count": 0
        }, 
        4688: {
            "Count": 0
        }, 
        4698: {
            "Count": 0
        },
        4699: {
            "Count": 0
        }, 
        4702: {
            "Count": 0
        }, 
        4703: {
            "Count": 0
        }, 
        4719: {
            "Count": 0
        }, 
        4732: {
            "Count": 0
        }, 
        4738: {
            "Count": 0
        }, 
        4742: {
            "Count": 0
        }, 
        4776: {
            "Count": 0
        }, 
        4798: {
            "Count": 0
        }, 
        4799: {
            "Count": 0
        }, 
        4985: {
            "Count": 0
        }, 
        5136: {
            "Count": 0
        }, 
        5140: {
            "Count": 0
        }, 
        5142: {
            "Count": 0
        }, 
        # 5145: {
        #     "Count": 0
        # }, 
        5156: {
            "Count": 0
        }, 
        5158: {
            "Count": 0
        }
    }

    # Open the specified logfile and count how many Event_ids in the dictionary is in the file.
    with open(logfile_path, 'r') as logfile:
        for line in logfile.readlines():
            if "MATCHED Event ID:" in line:
                event_id = int(line.split(':')[1].split()[0])
                if event_id in EVENT_ID_DICT:
                    EVENT_ID_DICT[event_id]["Count"] += 1
                else:
                    continue
        logfile.close()
    
    return EVENT_ID_DICT

def get_eventID_list(logfile_path):
    eventIDList = list()
    eventIDCountList = list()

    with open(logfile_path, "r") as eventIDFile:
        for line in eventIDFile.readlines():
            if "ID" in line:
                eventID = int(line.split(':')[1].split()[0])
                eventIDList.append(eventID)
            elif "Count" in line:                
                eventIDCount = int(line.split(':')[1].split()[0])
                eventIDCountList.append(eventIDCount)
            else:
                continue
    
    return eventIDList, eventIDCountList

def draw_graphs(eventIDList, eventIDCountList, logfileName):
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    plt.rcdefaults()
    _, ax = plt.subplots()

    y_pos = np.arange(len(eventIDList))

    ax.barh(y_pos, eventIDCountList, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(eventIDList)
    ax.set_xlabel('Event Count')
    ax.set_xlabel('Event ID Codes')
    ax.set_title('Event ID Counts (February 2019 - August 2019)')

    plt.savefig(os.path.join(LOGFILE_PATH, logfileName+".png"))
    plt.show()