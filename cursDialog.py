#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

import curses
import sys
import os
import sample_convert

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
        self.displayMessage()

        # Draw the ProgressBar Box
        self.drawProgressBarBox()

        self.win.refresh()

    def drawProgressBarBox(self):
        from curses.textpad import rectangle as rect
        self.win.attrset(self.clr1 | curses.A_BOLD)
        height, width = 2, 50
        y, x = 10, 3
        rect(self.win, y - 1, x - 1, height + y, width + x)

    def displayMessage(self):
        # Display the message if any
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i + 1, 2, msg, curses.A_BOLD)

    def progress(self, currentValue):
        percentage_complete = int((100 * currentValue / self.maxValue))
        blockValue = int(percentage_complete / 2)
        maxValue = str(self.maxValue)
        currentValue = str(currentValue)

        self.win.addstr(9, int(self.x / 2 - len(maxValue)) - 2, "{} of {}".format(currentValue, maxValue))

        for i in range(self.blockValue, blockValue):
            self.win.addstr(10, i + 3, '▋', self.clr2 | curses.A_BOLD)
            self.win.addstr(11, i + 3, '▋', self.clr2 | curses.A_NORMAL)

        if percentage_complete == 100:
            self.win.addstr(10, int(self.x / 2) - 3, 'Finish', curses.A_STANDOUT)
            self.win.getch()
        self.blockValue = blockValue
        self.win.refresh()


class ShowWelcomePage(CursBaseDialog):
    def showWelcomePage(self):
        progress = progressBarDialog(maxValue=100, message='Progressbar for Converting Process', title='Converting Evtx Log Files to XML Files  ',
                                     clr1=COLOR_RED, clr2=COLOR_GREEN)
        while not self.enterKey:
            for idx, row in enumerate(self.menu):
                if idx == self.focus:
                    self.win.addstr(int(self.y / 2 + idx), int(self.x / 2 - len(row) // 2), row, self.opt_attr | self.focus_attr)
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
                    folders = [f for f in os.scandir(sample_convert.EVTX_LOGS_PATH) if f.is_dir()]
                    for counter, folder in enumerate(folders, 1):

                        files = [f for f in os.scandir(folder.path)]
                        for file in files:
                            try:
                                for i in range(101):
                                    sample_convert.xml_converter(file.path)
                                    progress(i)
                            except:
                                print("Unexpected error:", sys.exc_info()[0])
                                raise
                else:
                    self.enterKey = True
        return None


class ShowInfoPage(CursBaseDialog):
    def show_info_page(self):
        while not self.enterKey:
            self.win.addstr(2, 2, INFO)
            rectangle(self.win, int(self.maxy/2), int(self.maxx/2-1), 2, 6, curses.A_NORMAL | self.opt_attr)
            self.win.addstr(int(self.maxy/2+1), int(self.maxx/2), 'Back ', self.focus_attr | self.opt_attr)

            self.win.refresh()
            key = self.win.getch()

            if key == ord('\n'):
                self.enterKey = True


def showWelcomePage(**options):
    return ShowWelcomePage(**options).showWelcomePage()


def progressBarDialog(**options):
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


if __name__ == '__main__':
    from time import sleep

    # test
    import traceback

    try:
        # init curses screen
        stdscr = curses.initscr()

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

        showWelcomePage(title='CI5235 Ethical Hacking')

        maxValue = 100
        progress = progressBarDialog(maxValue=maxValue, message='Progressbar for test', title='Progress test',
                                     clr1=COLOR_RED, clr2=COLOR_GREEN)
        for i in range(maxValue + 1):
            progress(i)
            sleep(0.1)

        curses.endwin()
    except:
        curses.endwin()
        traceback.print_exc()
