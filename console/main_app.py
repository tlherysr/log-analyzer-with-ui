#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

import os
import sys
import curses
from time import sleep

from console_logger import LogToFile
from console_convert import (is_logfile_exist, create_logfile_directory, check_xml_files, delete_xml_files,
                            xml_converter, read_evtx_files, EVTX_LOGS_PATH)
from console_analyse import search_xml_files, parse_xml_files
from console_visualise import find_log_files, count_EventID, get_eventID_list, draw_graphs

encoding = sys.getdefaultencoding()
INFO = """ Learning Outcomes:
    - Build and modify Python scripts that can be used in a cyber security context.
    - Demonstrate the practical use of python for surveillance and information gathering
    - Demonstrate the practical use of python for directory navigation, file search, file copying, 
      file opening, file reading, file saving and time stamping
    - Demonstrate the practical use of python for data structuring, analysis and visualisation
"""


class MainPage:
    def __init__(self, **options):
        self.maxy, self.maxx = curses.LINES, curses.COLS
        # self.win = curses.newwin(24, 80, int((self.maxy / 2 - 12)), int((self.maxx / 2) - 40))
        self.win = curses.newwin(self.maxy, self.maxx)
        # self.win.box()
        self.y, self.x = self.win.getmaxyx()
        self.title_attr = options.get('title_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.msg_attr = options.get('msg_attr', curses.A_BOLD)
        self.opt_attr = options.get('opt_attr', curses.A_BOLD)
        self.focus_attr = options.get('focus_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.title = options.get('title', curses.A_NORMAL)
        self.message = options.get('message', '')
        self.win.addstr(0, 0, ' ' * self.maxx, self.title_attr)
        self.win.keypad(True)
        # self.focus = 0
        self.focus = [0, 0]
        self.enterKey = False
        self.win.keypad(True)
        self.menu = ['Info', 'Convert', 'Analyse', 'Visualise', 'Exit']
        self.option = ('Yes   ', 'Cancel')
        self.current_line = ""
        
        # print title
        if self.title:
            self.win.addstr(0, int(self.x / 2 - len(self.title) / 2), self.title, self.title_attr)

        # Print the messages if any
        if self.message:
            for (i, msg) in enumerate(self.message.split('\n')):
                self.win.addstr(i + 1, 2, msg, curses.A_BOLD)

        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

    def key_event_handler(self):
        max = len(self.option)
        self.win.refresh()
        key = self.win.getch()
        if key == curses.KEY_LEFT and self.focus[0] != 0:
            self.focus[0] -= 1
        elif key == curses.KEY_RIGHT and self.focus[0] != max - 1:
            self.focus[0] += 1
        elif key == curses.KEY_UP and self.focus[1] != 0:
            self.focus[1] -= 1
        elif key == curses.KEY_DOWN and self.focus[1] != max - 1:
            self.focus[1] += 1
            self.current_line = self.option[self.focus[1]]
        elif key == ord('\n'):
            self.enterKey = True


class ShowProgressBarPage(MainPage):
    def __init__(self, **options):
        super(self.__class__, self).__init__(**options)
        self.clr1 = options.get("clr1", curses.A_NORMAL)
        self.clr2 = options.get("clr2", curses.A_NORMAL)
        self.maxValue = options.get("maxValue")
        self.blockValue = 0
        self.win.addstr(0, 0, ' ' * self.x, curses.A_STANDOUT)
        self.line_no = 2

        # Display Title
        self.display_title()

        self.win.refresh()

    def draw_progress_bar_box(self):
        from curses.textpad import rectangle as rect
        self.win.attrset(self.clr1 | curses.A_BOLD)
        height, width = 2, 50
        y, x = int(self.maxy / 2) - 5, int(self.maxx / 2) - 26
        rect(self.win, y - 1, x - 1, height + y, width + x)

    def display_title(self):
        # Print the title if there is any
        if self.title:
            self.win.addstr(0, int(self.x / 2 - len(self.title) / 2), self.title, self.title_attr)

    def display_message(self, message=None):
        self.win.addstr(4, 2, '\n')
        if message:
            for msg in message.split('\n'):                
                self.win.addstr(4, 2, msg, curses.A_BOLD)

    def display_message_newline(self, message=None):
        if message:
            for msg in message.split('\n'):                
                self.win.addstr(self.line_no, 2, msg, curses.A_BOLD)
                self.line_no += 1
            self.win.refresh()

    def progress(self, current_value):
        percentage_complete = int((100 * current_value / self.maxValue))
        blockValue = int(percentage_complete / 2)
        maxValue = str(self.maxValue)
        currentValue = str(current_value)

        self.win.addstr(int(self.maxy / 2), int(self.x / 2 - len(maxValue)) - 2,
                        "{} of {}".format(currentValue, maxValue))

        for i in range(self.blockValue, blockValue):
            self.win.addstr(int(self.maxy / 2) - 5, int(self.maxx / 2) + i - 26, '▋', self.clr2 | curses.A_BOLD)
            self.win.addstr(int(self.maxy / 2) - 4, int(self.maxx / 2) + i - 26, '▋', self.clr2 | curses.A_NORMAL)

        if percentage_complete == 100:
            self.win.addstr(int(self.maxy / 2) + 1, int(self.x / 2) - 3, 'Finish', curses.A_STANDOUT)
            self.win.getch()
        self.blockValue = blockValue
        self.win.refresh()


class ShowWelcomePage(MainPage):
    def show_welcome_page(self):
        while not self.enterKey:
            for idx, row in enumerate(self.menu):
                if idx == self.focus[1]:
                    self.win.addstr(int(self.y / 2 + idx), int(self.x / 2 - len(row) // 2), row,
                                    self.opt_attr | self.focus_attr)
                else:
                    self.win.addstr(int(self.y / 2 + idx), int(self.x / 2 - len(row) // 2), row, self.opt_attr)
            self.welcome_key_event_handler()

    def welcome_key_event_handler(self):
        self.win.refresh()
        key = self.win.getch()
        
        if key == curses.KEY_UP and self.focus[1] != 0:
            self.focus[1] -= 1
        elif key == curses.KEY_DOWN and self.focus[1] != len(self.menu) - 1:
            self.focus[1] += 1
        elif key == ord('\n'):
            # if user selected "Exit", exit the program
            if self.menu[self.focus[1]] == 'Exit':
                self.enterKey = True
            # if user wants intro, give it to him :D
            elif self.menu[self.focus[1]] == 'Info':
                show_info_page(title='Info Page')
                self.__init__(title='CI5235 Ethical Hacking')
            elif self.menu[self.focus[1]] == 'Convert':
                show_convert_page()
                self.__init__(title='CI5235 Ethical Hacking')
            elif self.menu[self.focus[1]] == 'Analyse':
                show_analyse_page()
                self.__init__(title='CI5235 Ethical Hacking')
            elif self.menu[self.focus[1]] == 'Visualise':
                show_visualise_page()
                self.__init__(title='CI5235 Ethical Hacking')
            else:
                self.enterKey = True


class ShowInfoPage(MainPage):
    def show_info_page(self):
        while not self.enterKey:
            self.win.addstr(2, 2, INFO)
            self.win.addstr(int(self.maxy / 2 + 1), int(self.maxx / 2)-1, ' Back ', self.focus_attr | self.opt_attr)
            rectangle(self.win, int(self.maxy / 2), int(self.maxx/2)-2, 2, 7, self.focus_attr | self.opt_attr)

            self.win.refresh()
            key = self.win.getch()

            if key == ord('\n'):
                self.enterKey = True


class ShowQuestionPage(MainPage):
    def show_question_page(self):
        rectangle(self.win, int(self.maxy / 2) - 1, int(self.maxx / 2) - 13, 2, len(self.option[0]) + 1, self.opt_attr)
        rectangle(self.win, int(self.maxy / 2) - 1, int(self.maxx / 2) + 2, 2, len(self.option[1]) + 1, self.opt_attr)
        pos_x = [int(self.maxx / 2) - 13, int(self.maxx / 2) + 2]

        while not self.enterKey:
            if self.focus[0] == 0:
                self.win.addstr(int(self.maxy / 2), int(self.maxx / 2) - 12, ' Yes  ', self.focus_attr | self.opt_attr)
                self.win.addstr(int(self.maxy / 2), int(self.maxx / 2) + 3, 'Cancel', self.opt_attr)
            else:
                self.win.addstr(int(self.maxy / 2), int(self.maxx / 2) - 12, ' Yes  ', self.opt_attr)
                self.win.addstr(int(self.maxy / 2), int(self.maxx / 2) + 3, 'Cancel', self.focus_attr | self.opt_attr)

            for i in range(2):
                if i != self.focus[0]:
                    rectangle(self.win, int(self.maxy / 2)-1, pos_x[i], 2, len(self.option[i]) + 1,
                              curses.A_NORMAL | self.opt_attr)
                else:
                    rectangle(self.win, int(self.maxy / 2)-1, pos_x[self.focus[0]], 2, len(self.option[self.focus[0]]) + 1,
                              self.focus_attr | self.opt_attr)
            self.key_event_handler()
        if self.focus[0] == 0:
            return True
        return False


def show_visualise_page():
    analyse_logfiles = find_log_files()
    if analyse_logfiles:
        logger_obj = LogToFile(type='Visualise')
        visualise_page = ShowProgressBarPage(maxValue=100,
                                           title='Visualisation Process Progressing',
                                           clr1=COLOR_RED, clr2=COLOR_GREEN)
        visualise_page.option = analyse_logfiles
        visualise_page.display_message_newline(message='[?] Which logfile do you want to analyse and draw the graph?')
        
        while not visualise_page.enterKey:
            for idx, row in enumerate(analyse_logfiles):
                if idx == visualise_page.focus[1]:
                    visualise_page.win.addstr(5+idx, 2, row, visualise_page.opt_attr | visualise_page.focus_attr)
                    visualise_page.line_no += 1
                else:
                    visualise_page.win.addstr(5+idx, 2, row, visualise_page.opt_attr)
                    visualise_page.line_no += 1
            visualise_page.key_event_handler()
        visualise_logfile_name = visualise_page.option[visualise_page.focus[1]]
        eventID_Dict = count_EventID(visualise_logfile_name)
        
        ### Log to Visualise log file
        for eventID in eventID_Dict:
            logger_obj.logtofile(message="Event ID: {event_id}".format(event_id=eventID))
            logger_obj.logtofile("Event Count: {count}".format(count=eventID_Dict.get(eventID).get("Count")))
            logger_obj.logtofile("")

        eventID_list, eventID_count_list = get_eventID_list(logger_obj.logfile)
        visualise_page.__init__(title='Graph', message='[+] Your graph is ready! Here it is!!')
        draw_graphs(eventID_list, eventID_count_list, logger_obj.logfile)
        visualise_page.win.getch()
    
    else:
        visualise_page = ShowProgressBarPage(maxValue=100,    
                                           title='Visualisation Process Progressing',
                                           clr1=COLOR_RED, clr2=COLOR_GREEN)
        visualise_page.display_message_newline(message='There is no analyse log file yet. Please run "Analyse"  first.')
        visualise_page.win.getch()


def show_analyse_page():
    if check_xml_files():
        logger_obj = LogToFile(type='Analyse')        
        xml_files = search_xml_files()    
        analyse_page = ShowProgressBarPage(maxValue=len(xml_files),
                                         title='Analyse Process Progressing',
                                         clr1=COLOR_RED, clr2=COLOR_GREEN
                                        )
        
        analyse_page.display_message_newline(message='[+] SEARCHING FOR XML FILES NOW')
        sleep(0.2)
        analyse_page.display_message_newline(message='[+] SEARCHING FOR XML FILES NOW.')
        sleep(0.2)
        analyse_page.display_message_newline(message='[+] SEARCHING FOR XML FILES NOW..')
        sleep(0.2)
        analyse_page.display_message_newline(message='[+] SEARCHING FOR XML FILES NOW...')
        sleep(0.2)
        analyse_page.display_message_newline(message='[+] NOW STARTING TO PARSE YOUR XML FILES')
        sleep(0.2)
        analyse_page.draw_progress_bar_box()
        
        parse_xml_files(xml_files, analyse_page, logger_obj)
        
        analyse_page.display_message_newline(message='[+] FINISHED NOWW!!!!')
    else:
        analyse_page = ShowProgressBarPage(title='Analyse Process Progressing',
                                         message='\nYOU SHOULD RUN THE CONVERT SCRIPT FIRST!'
                                        )
        analyse_page.win.getch()
        welcome_page.__init__(title='CI5235 Ethical Hacking')


def show_convert_page():
    maxValue = sum([len(files) for r, d, files in os.walk(EVTX_LOGS_PATH)])
    convert_progress_bar = ShowProgressBarPage(maxValue=maxValue,
                                               title='Convert Process Progressing',
                                               clr1=COLOR_RED, clr2=COLOR_GREEN
                                              )

    # Check if logfile exists.
    if is_logfile_exist():
        # Check if there is any xml files in the log directories
        xml_files = check_xml_files()
        if xml_files: 
            if show_question_page(title='XML Files Delete', 
                                  message='[-] It has been found that some .xml files exist in your evtx_logs folders.\n' \
                                          '[?] Would you want me to delete all of them for you now?'):
                delete_xml_files(xml_files)
                maxValue = sum([len(files) for r, d, files in os.walk(EVTX_LOGS_PATH)])
                convert_progress_bar.__init__(maxValue=maxValue,
                                              message='Your evtx log files are being converted to xml files...\nConverting...',
                                              title='Convert Process Progressing',
                                              clr1=COLOR_RED, clr2=COLOR_GREEN
                                             )
                convert_progress_bar.draw_progress_bar_box()
                logger_obj = LogToFile(type='Convert')

                read_evtx_files(convert_progress_bar, logger_obj)
            else:
                welcome_page.__init__(title='CI5235 Ethical Hacking')

        else:
            convert_progress_bar.__init__(maxValue=maxValue,
                                          message='Your evtx log files are being converted to xml files...\nConverting',
                                          title='Convert Process Progressing',
                                          clr1=COLOR_RED, clr2=COLOR_GREEN
                                         )
            convert_progress_bar.draw_progress_bar_box()
            logger_obj = LogToFile(type='Convert')
            read_evtx_files(convert_progress_bar, logger_obj)
    else:
        # Ask user if she/he wants to create the log directory
        if show_question_page(title='Convert Page Processing',
                              message='[-] I can not find the necessary logfile directory.\n'
                                      '[?] Would you want me to create it for you?'):
            create_logfile_directory()
            convert_progress_bar.__init__(maxValue=maxValue,
                                          message='Your evtx log files are being converted to xml files...\nConverting',
                                          title='Convert Process Progressing',
                                          clr1=COLOR_RED, clr2=COLOR_GREEN
                                         )
            convert_progress_bar.draw_progress_bar_box()
            logger_obj = LogToFile(type='Convert')
            read_evtx_files(convert_progress_bar, logger_obj)
        else:
            welcome_page.__init__(title='CI5235 Ethical Hacking')


def show_question_page(**options):
    return ShowQuestionPage(**options).show_question_page()


def progress_bar_dialog(**options):
    return ShowProgressBarPage(**options).progress


def show_info_page(**options):
    return ShowInfoPage(**options).show_info_page()


def rectangle(win, begin_y, begin_x, height, width, attr):
    win.vline(begin_y, begin_x, curses.ACS_VLINE, height, attr)
    win.hline(begin_y, begin_x, curses.ACS_HLINE, width, attr)
    win.hline(height + begin_y, begin_x, curses.ACS_HLINE, width, attr)
    win.vline(begin_y, begin_x + width, curses.ACS_VLINE, height, attr)
    win.addch(begin_y, begin_x, curses.ACS_ULCORNER, attr)
    win.addch(begin_y, begin_x + width, curses.ACS_URCORNER, attr)
    win.addch(height + begin_y, begin_x, curses.ACS_LLCORNER, attr)
    win.addch(begin_y + height, begin_x + width, curses.ACS_LRCORNER, attr)
    win.refresh()


def main():
    import traceback
    try:
        # init curses screen
        curses.initscr()

        global COLOR_RED
        global COLOR_GREEN
        global COLOR_BLUE
        global COLOR_NORMAL
        global welcome_page

        curses.start_color()
        # stdscr.use_default_colors()
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, 0)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLUE, 0)

        COLOR_RED = curses.color_pair(1)
        COLOR_GREEN = curses.color_pair(2)
        COLOR_BLUE = curses.color_pair(3)
        COLOR_NORMAL = curses.color_pair(4)

        welcome_page = ShowWelcomePage(title='CI5235 Ethical Hacking')
        welcome_page.show_welcome_page()

        curses.endwin()
    except:
        curses.endwin()
        traceback.print_exc()


if __name__ == '__main__':
    main()
