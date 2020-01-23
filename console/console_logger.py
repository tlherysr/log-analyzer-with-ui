#!/usr/bin/env python

import os
import logging
from datetime import datetime


LOG_DIR = "CI5235_Logs"
EVTX_LOGS_DIR = "evtx_logs"

# LOGGING
LOGFILE_PATH = os.path.join(os.getcwd(), LOG_DIR)
EVTX_LOGS_PATH = os.path.join(os.getcwd(), EVTX_LOGS_DIR)


class LogToFile:
    def __init__(self, **options):
        # self.message = options.get("message")
        self.type = options.get("type")

        # Create the logger
        self.logger = logging.getLogger('console_convert_log')
        self.logger.setLevel(logging.DEBUG)
        self.timestamp = datetime.now().strftime("%d_%b_%Y_%H:%M:%S")

        # Create file handler which logs even debug messages
        if self.type == "Convert":
            self.logfile = os.path.join(LOGFILE_PATH, "convert_log_" + self.timestamp)
        elif self.type == "Analyse":
            self.logfile = os.path.join(LOGFILE_PATH, "analyse_log_" + self.timestamp)
        elif self.type == "Visualise":
            self.logfile = os.path.join(LOGFILE_PATH, "visualise_log_" + self.timestamp)

        self.fh = logging.FileHandler(filename=self.logfile, mode='w+')
        self.fh.setLevel(logging.DEBUG)
        # add the handlers to logger
        self.logger.addHandler(self.fh)

        # Print the header to the logfile
        self.logtofile(message="LOG DATE and TIME: {timestamp}".format(timestamp=self.timestamp))
        self.logtofile(message="")

    def logtofile(self, message):
        self.logger.info(message)
