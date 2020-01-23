#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

import curses
import sys
import os
from .console_convert import is_logfile_exist, create_logfile_directory, check_xml_files, EVTX_LOGS_PATH, xml_converter


encoding = sys.getdefaultencoding()
INFO = """ Learning Outcomes:
    - Build and modify Python scripts that can be used in a cyber security context.
    - Demonstrate the practical use of python for surveillance and information gathering
    - Demonstrate the practical use of python for directory navigation, file search, file copying, 
      file opening, file reading, file saving and time stamping
    - Demonstrate the practical use of python for data structuring, analysis and visualisation
"""


class CursBaseDialog:
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
        self.focus = 0
        self.enterKey = False
        self.win.keypad(True)
        self.menu = ['Info', 'Convert', 'Analyse', 'Visualise', 'Exit']
        self.win.addstr(0, int(self.x / 2 - len(self.title) / 2), self.title, self.title_attr)

        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

    def left_right_key_event_handler(self, max):
        self.win.refresh()
        key = self.win.getch()
        if key == curses.KEY_LEFT and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_RIGHT and self.focus != max - 1:
            self.focus += 1
        elif key == ord('\n'):
            self.enterKey = True

    def up_down_key_event_handler(self):
        self.win.refresh()
        key = self.win.getch()

        if key == curses.KEY_UP and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_DOWN and self.focus != len(self.menu) - 1:
            self.focus += 1
        elif key == ord('\n'):
            # if user selected "Exit", exit the program
            if self.menu[self.focus] == "Exit":
                self.enterKey = True
            # if user wants intro, give it to him :D
            elif self.menu[self.focus] == "Info":
                show_info_page(title='INFO PAGE TITLE')


class ProgressBarDialog(CursBaseDialog):
    def __init__(self, **options):
        super(self.__class__, self).__init__(**options)
        self.clr1 = options.get("clr1", curses.A_NORMAL)
        self.clr2 = options.get("clr2", curses.A_NORMAL)
        self.maxValue = options.get("maxValue")
        self.blockValue = 0
        self.win.addstr(0, 0, ' ' * self.x, curses.A_STANDOUT)

        # Display message
        self.display_message()

        # Draw the ProgressBar Box
        self.draw_progress_bar_box()

        self.win.refresh()

    def draw_progress_bar_box(self):
        from curses.textpad import rectangle as rect
        self.win.attrset(self.clr1 | curses.A_BOLD)
        height, width = 2, 50
        y, x = int(self.maxy / 2) - 5, int(self.maxx / 2) - 26
        rect(self.win, y - 1, x - 1, height + y, width + x)

    def display_message(self, message=None):
        # Print the title if there is any
        if self.title:
            self.win.addstr(0, int(self.x / 2 - len(self.title) / 2), self.title, self.title_attr)

        if message:
            for (i, msg) in enumerate(message.split('\n')):
                self.win.addstr(i + 4, 2, msg, curses.A_BOLD)

        # Display the message if any
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i + 1, 2, msg, curses.A_BOLD)

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


class ShowWelcomePage(CursBaseDialog):
    def show_welcome_page(self):
        while not self.enterKey:
            for idx, row in enumerate(self.menu):
                if idx == self.focus:
                    self.win.addstr(int(self.y / 2 + idx), int(self.x / 2 - len(row) // 2), row,
                                    self.opt_attr | self.focus_attr)
                else:
                    self.win.addstr(int(self.y / 2 + idx), int(self.x / 2 - len(row) // 2), row, self.opt_attr)

            self.win.refresh()
            key = self.win.getch()

            if key == curses.KEY_UP and self.focus != 0:
                self.focus -= 1
            elif key == curses.KEY_DOWN and self.focus != len(self.menu) - 1:
                self.focus += 1
            elif key == ord('\n'):
                # if user selected "Exit", exit the program
                if self.menu[self.focus] == 'Exit':
                    sys.exit(0)
                # if user wants intro, give it to him :D
                elif self.menu[self.focus] == 'Info':
                    show_info_page(title='Info Page')
                    self.__init__(title='CI5235 Ethical Hacking')
                elif self.menu[self.focus] == 'Convert':
                    show_convert_page()
                    self.__init__(title='CI5235 Ethical Hacking')
                else:
                    self.enterKey = True
        return None


class ShowInfoPage(CursBaseDialog):
    def show_info_page(self):
        while not self.enterKey:
            self.win.addstr(2, 2, INFO)
            rectangle(self.win, int(self.maxy / 2), int(self.maxx / 2 - 1), 2, 7, curses.A_NORMAL | self.opt_attr)
            self.win.addstr(int(self.maxy / 2 + 1), int(self.maxx / 2), ' Back ', self.focus_attr | self.opt_attr)

            self.win.refresh()
            key = self.win.getch()

            if key == ord('\n'):
                self.enterKey = True


class AskLogfileCreate(CursBaseDialog):
    def ask_logfile_create(self):
        self.message = '[-] I can not find the necessary log directory. Would you want me to create it for you?'

        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(int(self.maxy/2)+i-10, int(self.maxx/2)-int(len(msg)/2), msg,  self.msg_attr)

        options = ('Yes   ', 'Cancel')
        rectangle(self.win, int(self.maxy/2)-1, int(self.maxx/2)-13, 2, len(options[0])+1, self.opt_attr)
        rectangle(self.win, int(self.maxy/2)-1, int(self.maxx/2)+2, 2, len(options[1])+1, self.opt_attr)
        pos_x = [int(self.maxx/2)-13, int(self.maxx/2)+2]

        while not self.enterKey:
            if self.focus == 0:
                self.win.addstr(int(self.maxy/2), int(self.maxx/2)-12, ' Yes  ', self.focus_attr | self.opt_attr)
                self.win.addstr(int(self.maxy/2), int(self.maxx/2)+3, 'Cancel', self.opt_attr)
            else:
                self.win.addstr(int(self.maxy/2), int(self.maxx/2)-12, ' Yes  ', self.opt_attr)
                self.win.addstr(int(self.maxy/2), int(self.maxx/2)+3, 'Cancel', self.focus_attr | self.opt_attr)

            for i in range(2):
                if i != self.focus:
                    rectangle(self.win, int(self.maxy/2)-1, pos_x[i], 2, len(options[i]) + 1, curses.A_NORMAL | self.opt_attr)
                else:
                    rectangle(self.win, int(self.maxy/2)-1, pos_x[self.focus], 2, len(options[self.focus]) + 1,
                              self.focus_attr | self.opt_attr)
            self.left_right_key_event_handler(2)
        if self.focus == 0:
            return True
        return False


def show_convert_page():
    maxValue = sum([len(files) for r, d, files in os.walk(EVTX_LOGS_PATH)])

    progress_bar = ProgressBarDialog(maxValue=maxValue,
                                     message='Your evtx log files is being converted to xml files...\nAnd this is a '
                                             'sample second line\nAnd this is third',
                                     title='Convert Process Progressing',
                                     clr1=COLOR_RED, clr2=COLOR_GREEN)

    # Check if logfile exists.
    if is_logfile_exist():
        progress_bar.display_message(message='[+] You have the necessary logfile directory. Keep going...')
        # TODO: Check if there is any xml files in the log directories
        xml_files = check_xml_files()
        if xml_files:
            pass # TODO: New Xml file delete ask class will be thrown here

    else:
        # Ask user if she/he wants to create the log directory
        if ask_logfile_create(title='Convert Page Processing'):
            create_logfile_directory()
            progress_bar.__init__(maxValue=maxValue,
                                  message='Your evtx log files is being converted to xml files...\nAnd this is a '
                                          'sample second line\nAnd this is third',
                                  title='Convert Process Progressing',
                                  clr1=COLOR_RED, clr2=COLOR_GREEN)
        else:
            welcome.__init__(title='CI5235 Ethical Hacking')
            welcome.show_welcome_page()

    c = 0
    folders = [f for f in os.scandir(sample_convert.EVTX_LOGS_PATH) if f.is_dir()]
    for counter, folder in enumerate(folders, 1):
        files = [f for f in os.scandir(folder.path)]
        for file in files:
            xml_converter(file.path)
            progress_bar.progress(c)
            c += 1


def show_welcome_page(**options):
    return ShowWelcomePage(**options).show_welcome_page()


def ask_logfile_create(**options):
    return AskLogfileCreate(**options).ask_logfile_create()


def progress_bar_dialog(**options):
    return ProgressBarDialog(**options).progress


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
        stdscr = curses.initscr()

        global COLOR_RED
        global COLOR_GREEN
        global COLOR_BLUE
        global COLOR_NORMAL
        global welcome

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

        welcome = ShowWelcomePage(title='CI5235 Ethical Hacking')
        welcome.show_welcome_page()

        curses.endwin()
    except:
        curses.endwin()
        traceback.print_exc()


if __name__ == '__main__':
    main()
