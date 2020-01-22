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
        self.display_message()

        # Draw the ProgressBar Box
        self.draw_progress_bar_box()

        self.win.refresh()

    def draw_progress_bar_box(self):
        from curses.textpad import rectangle as rect
        self.win.attrset(self.clr1 | curses.A_BOLD)
        height, width = 2, 50
        y, x = int(self.maxy/2)-5, int(self.maxx/2)-26
        rect(self.win, y - 1, x - 1, height + y, width + x)

    def display_message(self):
        # Print the title if there is any
        if self.title:
            self.win.addstr(0, int(self.x / 2 - len(self.title) / 2), self.title, self.title_attr)

        # Display the message if any
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i + 1, 2, msg, curses.A_BOLD)

    def progress(self, current_value):
        percentage_complete = int((100 * current_value / self.maxValue))
        blockValue = int(percentage_complete / 2)
        maxValue = str(self.maxValue)
        currentValue = str(current_value)

        self.win.addstr(int(self.maxy/2), int(self.x / 2 - len(maxValue)) - 2, "{} of {}".format(currentValue, maxValue))

        for i in range(self.blockValue, blockValue):
            self.win.addstr(int(self.maxy/2)-5, int(self.maxx/2)+i-26, '▋', self.clr2 | curses.A_BOLD)
            self.win.addstr(int(self.maxy/2)-4, int(self.maxx/2)+i-26, '▋', self.clr2 | curses.A_NORMAL)

        if percentage_complete == 100:
            self.win.addstr(int(self.maxy/2)+1, int(self.x / 2) - 3, 'Finish', curses.A_STANDOUT)
            self.win.getch()
        self.blockValue = blockValue
        self.win.refresh()


class ShowWelcomePage(CursBaseDialog):
    def showWelcomePage(self):
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


def show_convert_page():
    maxValue = 100
    progress = progress_bar_dialog(maxValue=maxValue,
                                   message='Your evtx log files is being converted to xml files...\nAnd this is a sample second line\nAnd this is third',
                                   title='Convert Process Progressing',
                                   clr1=COLOR_RED, clr2=COLOR_GREEN)
    sample_convert.is_logfile_exist()

    c = 0
    e = 0
    folders = [f for f in os.scandir(sample_convert.EVTX_LOGS_PATH) if f.is_dir()]
    for counter, folder in enumerate(folders, 1):
        files = [f for f in os.scandir(folder.path)]
        for file in files:
            sample_convert.xml_converter(file.path)
            progress(e)
            e = int(c*(100/166))
            c += 1


def show_welcome_page(**options):
    return ShowWelcomePage(**options).showWelcomePage()


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

        show_welcome_page(title='CI5235 Ethical Hacking')

        curses.endwin()
    except:
        curses.endwin()
        traceback.print_exc()


if __name__ == '__main__':
    main()
