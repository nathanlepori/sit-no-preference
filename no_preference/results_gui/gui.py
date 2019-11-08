from tkinter import * #needed for the file
from os import path
import json
import os
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
from tkinter import Entry
from no_preference.lib.util import get_data_dir
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def get_File_dir():
    return get_data_dir()


def vp_start_gui():
    """
    Starting point when module is the main routine.
    """
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    root.title("Welcome to Social Profiling app")
    root.geometry('600x500')
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    """
    Starting point when module is imported by another program.
    """
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def get_web_path(self, type):
        # get the path of the file
        global web_path
        file_path = path.join(get_File_dir(), 'results')
        web_path = tkinter.filedialog.askopenfilename(initialdir=file_path,
                                                      filetypes=[("json file", "*.json")])
        global web_loaded
        web_loaded = 0  # counter to signify if file has been loaded or not
        web_loaded += 1
        eval("self." + type + ".delete(0,END)")
        eval("self." + type + ".insert(0,web_path)")

    def get_social_path(self, type):  # get path of file
        global social_path
        file_path = path.join(get_File_dir(), 'results')
        social_path = tkinter.filedialog.askopenfilename(initialdir=file_path,
                                                         filetypes=[("json file", "*.json")])
        global social_loaded
        social_loaded = 0  # counter to signify if file has been loaded or not
        social_loaded += 1
        eval("self." + type + ".delete(0,END)")
        eval("self." + type + ".insert(0,social_path)")

    def load_files(self):  # Load the files and store it in it's respective outputs.
        try:
            assert os.path.exists(self.Entry1.get()), "File not found. Enter a valid file path."
            assert ".txt" in self.Entry1.get(), "File is not a .txt file"

        except Exception as e:
            print(e)

    def load_files2(self):  # Load the second file and store it in it's respective outputs
        try:
            assert os.path.exists(self.Entry1.get()), "File not found. Enter a valid file path."
            assert ".txt" in self.Entry1.get(), "File is not a .txt file"

        except Exception as e:
            print(e)

    def __init__(self, top=None):  # initialises the GUI
        global web_loaded
        global social_loaded
        web_loaded = 0
        social_loaded = 0
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font10 = "-family {Courier New} -size 10"
        font16 = "-family {Segoe UI} -size 8"
        font18 = "-family {Segoe UI} -size 8"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font=font18)
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        self.menubar = tk.Menu(top, font=('Segoe UI', 8,), bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)
        # Word to find box
        self.Entry3 = tk.Entry(top)
        self.Entry3.place(relx=0.1, rely=0.91, height=26, relwidth=0.299)
        self.Entry3.configure(background="white")
        self.Entry3.configure(disabledforeground="#a3a3a3")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(foreground="#000000")
        self.Entry3.configure(highlightbackground="#d9d9d9")
        self.Entry3.configure(highlightcolor="black")
        self.Entry3.configure(insertbackground="black")
        self.Entry3.configure(selectbackground="#c4c4c4")
        self.Entry3.configure(selectforeground="black")
        self.Entry3.configure(width=169)

        # Label of Word to Find
        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.1, rely=0.855, height=27, width=130)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font18)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Word to Find''')

        # Label of Social Media Data
        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.01, rely=0.25, height=27, width=130)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font18)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Result Set B''')

        # Label of Comparison between both Datasets
        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.01, rely=0.49, height=27, width=190)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font18)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Comparison between both Datasets''')

        # Label of Web Browser Data
        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.01, rely=0.01, height=27, width=130)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font18)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Result Set A''')

        # Button that triggers the function
        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.097, rely=0.77, height=35, width=114)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font18)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='Result set B')
        self.Button2.configure(command=lambda: load_set_b())  # opening the file directory to choose file

        def load_set_a():
            self.get_web_path("Entry1")

        # Button that triggers the function
        self.Button3 = tk.Button(top)
        self.Button3.place(relx=0.097, rely=0.69, height=35, width=114)
        self.Button3.configure(activebackground="#ececec")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font=font18)
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='Result set A')
        self.Button3.configure(command=lambda: load_set_a())  # opening the file directory to choose file

        def load_set_b():
            self.get_social_path("Entry2")

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.01, rely=0.31, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Word that Appeared the Most''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: social_word_count())

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.32, rely=0.31, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Ranked Appeared Words''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: social_word_count_ranked())

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.32, rely=0.07, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Ranked Appeared Words''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: web_word_count_ranked())

        # button for web timeline
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.63, rely=0.07, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Timeline of Word''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: web_timeline())

        # button for social timeline
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.63, rely=0.31, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Timeline of Word''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: social_timeline())

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.01, rely=0.07, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Word that Appeared the Most''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: web_word_count())

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.01, rely=0.56, height=35, width=190)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Comparison of Top Count Words''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: mst_count_comparison_chart())

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.35, rely=0.56, height=35, width=210)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Comparison of User's Searched Word''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: find_comparison_chart())

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.01, rely=0.145, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Word to Find''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: web_word_to_find())

        self.Button1 = tk.Button(top)  # button to generate web wordcloud
        self.Button1.place(relx=0.32, rely=0.145, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''WordCloud''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: web_word_cloud())

        self.Button1 = tk.Button(top)  # button to generate social wordcloud
        self.Button1.place(relx=0.32, rely=0.385, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''WordCloud''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: social_word_cloud())

        self.Button1 = tk.Button(top)  # button to generate web, social comparision wordcloud
        self.Button1.place(relx=0.72, rely=0.56, height=35, width=160)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''WordCloud''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: web_social_word_cloud())

        # Button that triggers the function
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.01, rely=0.385, height=35, width=170)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font18)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Word to Find''')
        self.Button1.configure(width=62)
        self.Button1.configure(command=lambda: social_word_to_find())

        # Get file directory
        self.Entry1 = Entry(top)
        self.Entry1.place(relx=0.31, rely=0.70, height=26, relwidth=0.431)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font=font10)
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        # Get file directory
        self.Entry2 = Entry(top)
        self.Entry2.place(relx=0.31, rely=0.78, height=26, relwidth=0.431)
        self.Entry2.configure(background="white")
        self.Entry2.configure(disabledforeground="#a3a3a3")
        self.Entry2.configure(font=font10)
        self.Entry2.configure(foreground="#000000")
        self.Entry2.configure(insertbackground="black")

        def open_web_path(x, y):
            with open(web_path, 'r') as f:
                plots = json.loads(f.read())
                for key, val in plots.items():
                    x.append(key)
                    y.append(val)
                Sorty, Sortx = zip(*sorted(zip(y, x)))
                return Sorty, Sortx

        def open_social_path(x, y):
            with open(social_path, 'r') as f:
                plots = json.loads(f.read())
                for key, val in plots.items():
                    x.append(key)
                    y.append(val)
                Sorty, Sortx = zip(*sorted(zip(y, x)))
                return Sorty, Sortx

        def social_word_count():
            """
            Function that gets the Top Count of the Social CSV file
            :return:
            """
            if social_loaded < 1:  # If social media file not loaded, gives error
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")

            elif social_loaded >= 1:  # else if social media file loaded
                x = []
                y = []
                ydisplay = []
                Sorty, Sortx = open_social_path(x, y)
                xmost = Sortx[-1]
                ymost = Sorty[-1]
                ydisplay.append(ymost)
                if len(x) == 0:  # if column is empty
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:  # else, plots
                    fig, ax = plt.subplots(1, 1)  # changing width of the bar chart
                    ax.set_xlim(-2, 2)
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(ydisplay):
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))
                    plt.bar(xmost, ymost)
                    plt.title('Top Word\n')
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    plt.show()  # displays the chart

            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for Social!")

        def web_word_count():
            """
            Function that gets the Top Count of the Web CSV file, same function only using different CSV file
            :return:
            """
            if web_loaded < 1:  # if web file not loaded, prompts error
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif web_loaded >= 1:
                # else if loaded
                x = []
                y = []
                ydisplay = []
                Sorty, Sortx = open_web_path(x, y)
                xmost = Sortx[-1]
                ymost = Sorty[-1]
                ydisplay.append(ymost)
                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    fig, ax = plt.subplots(1, 1)
                    ax.set_xlim(-2, 2)
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(ydisplay):
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))
                    plt.bar(xmost, ymost)
                    plt.title('Top Word\n')
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    plt.show()

            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for web!")

        def social_word_count_ranked():
            """
            Getting all data out and ranking them
            :return:
            """
            # prompts error if social file not loaded
            if social_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif social_loaded >= 1:
                # if social file loaded
                x = []
                y = []
                Sorty, Sortx = open_social_path(x, y)
                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    plt.bar(Sortx, Sorty)
                    plt.xticks(rotation=90)  # rotation so to fill more graphs without the names colliding
                    plt.title('Ranked Word Count\n')
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    manager = plt.get_current_fig_manager()
                    manager.resize(*manager.window.maxsize())
                    plt.show()

            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for social!")

        def web_word_count_ranked():
            """
            Same function as above just using different file
            :return:
            """
            if web_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif web_loaded >= 1:
                y = []
                x = []
                Sorty, Sortx = open_web_path(x, y)
                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    plt.bar(Sortx, Sorty)
                    plt.xticks(rotation=90)
                    plt.title('Ranked Word Count\n')
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    manager = plt.get_current_fig_manager()
                    manager.resize(*manager.window.maxsize())
                    plt.show()

            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for social!")

        def web_word_to_find():  # function that allows user to key in word to find in csv
            entry_string = self.Entry3.get()  # getting what user keyed in for word to find
            if web_loaded < 1:  # if file not loaded, prompts error
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif web_loaded >= 1 and entry_string != "":
                # if file loaded and user has keyed in the word to find
                y = []
                x = []
                Sorty, Sortx = open_web_path(x, y)
                if entry_string in Sortx:
                    position_of_word = Sortx.index(entry_string)
                    x_web = entry_string
                    y_web = (Sorty[position_of_word])
                elif entry_string not in Sortx:  # if word not in
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    list_to_show = [y_web]
                    fig, ax = plt.subplots(1, 1)
                    ax.set_xlim(-2, 2)  # decreases the width of the bar
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(list_to_show):
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))
                    plt.bar(x_web, y_web)
                    plt.title("Searched Word with Count")
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    plt.show()
            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please enter a word to find or enter the files!")

        def social_word_to_find():  # same function as above but is different file
            entry_string = self.Entry3.get()
            if social_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif social_loaded >= 1 and entry_string != "":
                y = []
                x = []
                Sorty, Sortx = open_social_path(x, y)
                if entry_string in Sortx:
                    position_of_word = Sortx.index(entry_string)
                    x_social = entry_string
                    y_social = (Sorty[position_of_word])
                elif entry_string not in Sortx:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    list_to_show = [y_social]
                    fig, ax = plt.subplots(1, 1)
                    ax.set_xlim(-2, 2)
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(list_to_show):
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))
                    plt.bar(x_social, y_social)
                    plt.title("Searched Word with Count")
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    plt.show()

            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please enter a word to find or enter the files!")

        def mst_count_comparison_chart():
            """
            Function that grabs the most appeared word and compare between both files
            :return:
            """
            if social_loaded < 1:  # if file not loaded, prompts error
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load the files!")
            elif social_loaded >= 1 and web_loaded >= 1:  # if both files loaded
                x_web = []
                y_web = []
                x_most = []
                y_most = []
                Sorty, Sortx = open_web_path(x_web, y_web)
                x_most.append("Result A Data :" + (Sortx[-1]))
                y_most.append(Sorty[-1])
                x_social = []
                y_social = []
                Sorty, Sortx = open_social_path(x_social, y_social)
                x_most.append(("Result B Data :") + Sortx[-1])
                y_most.append(Sorty[-1])
                if len(x_most) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(y_most):
                        plt.text(xlocs[i] - -0.36, v + 0.01, str(v))
                    plt.bar(x_most, y_most)
                    plt.title("Top word count for each Dataset")
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    plt.show()

            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please enter a word to find or enter the files!")

        def find_comparison_chart():  # allows user to key in the word they want to find and compares both datasets
            entry_string = self.Entry3.get()  # getting the user keyed in string
            if social_loaded < 1:  # if social file not loaded
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load the files!")
            elif social_loaded >= 1 and entry_string != "" and web_loaded >= 1:
                # If string, web browser file and social media file is keyed in
                y_social = []
                x_social = []
                y_web = []
                x_web = []
                x_find = []
                y_find = []
                Sorty_web, Sortx_web = open_web_path(x_web, y_web)
                if entry_string in Sortx_web:
                    position_of_word = Sortx_web.index(entry_string)
                    x_find.append("Result A Data: " + entry_string)  # appending the data to x and y axis
                    y_find.append(Sorty_web[position_of_word])

                elif entry_string not in Sortx_web:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()

                Sorty_social, Sortx_social = open_social_path(x_social, y_social)
                if entry_string in Sortx_social:
                    position_of_word = Sortx_social.index(entry_string)
                    x_find.append("Result B Data: " + entry_string)  # appending the data to x and y axis
                    y_find.append(Sorty_social[position_of_word])

                elif entry_string not in Sortx_social:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()

                if len(x_find) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(y_find):
                        plt.text(xlocs[i] - -0.36, v + 0.01, str(v))
                    plt.bar(x_find, y_find)
                    plt.title("Searched Word with Count")
                    plt.xlabel('Word')
                    plt.ylabel('Count')
                    plt.show()

            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please enter a word to find or enter the files!")

        def web_timeline():
            """
            Getting timeline for web
            :return:
            """
            filedir = self.Entry1.get()
            filename = (os.path.basename(filedir))

            if web_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif web_loaded >= 1:
                x = []
                y = []
                Sorty, Sortx = open_web_path(x, y)
                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    plt.bar(Sortx, Sorty)  # rotation so to fill more graphs without the names colliding
                    plt.title(filename)
                    plt.xlabel('Date')
                    plt.ylabel('Count')
                    manager = plt.get_current_fig_manager()
                    manager.resize(*manager.window.maxsize())
                    plt.show()
            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for social!")

        def social_timeline():
            """
            Getting timeline for social
            :return:
            """
            filedir = self.Entry2.get()
            filename = (os.path.basename(filedir))
            if social_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif social_loaded >= 1:
                x = []
                y = []
                Sorty, Sortx = open_social_path(x, y)
                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    plt.bar(Sortx, Sorty)  # rotation so to fill more graphs without the names colliding
                    plt.title(filename)
                    plt.xlabel('Date')
                    plt.ylabel('Count')
                    manager = plt.get_current_fig_manager()
                    manager.resize(*manager.window.maxsize())
                    plt.show()
            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for social!")

        def social_word_cloud():
            """
            Getting wordcloud for social
            :return:
            """
            if social_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif social_loaded >= 1:
                x = []
                y = []
                Sorty, Sortx = open_social_path(x, y)
                xcloud = str(Sortx)
                xcloud2 = xcloud.replace("\'", "")  # replaces all the '

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    wordcloud = WordCloud(max_font_size=40).generate(xcloud2)  # generates wordcloud
                    plt.figure()
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    plt.show()
            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for social!")

        def web_word_cloud():
            """
            Getting wordcloud for web
            :return:
            """
            if web_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif web_loaded >= 1:
                x = []
                y = []
                Sorty, Sortx = open_web_path(x, y)
                xcloud = str(Sortx)
                xcloud2 = xcloud.replace("\'", "")  # replaces all the '

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    wordcloud = WordCloud(max_font_size=40).generate(xcloud2)  # generate wordcloud
                    plt.figure()
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    plt.show()
            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please only load 1 file for social!")

        def web_social_word_cloud():  # getting wordcloud for web and social
            if web_loaded < 1 or social_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif social_loaded >= 1 and web_loaded >= 1:
                x_web = []
                y_web = []
                x_social = []
                y_social = []
                xcloud = []
                Sorty_web, Sortx_web = open_web_path(x_web, y_web)
                xcloud.append(Sortx_web)
                Sorty_social, Sortx_social = open_social_path(x_social, y_social)
                xcloud.append(Sortx_social)
                xcloud2 = str(xcloud)
                finalxcloud = xcloud2.replace("\'", "")
                if len(x_web) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    word_cloud = WordCloud(max_font_size=40).generate(finalxcloud)  # generates wordcloud
                    plt.figure()
                    plt.imshow(word_cloud, interpolation="bilinear")
                    plt.axis("off")
                    plt.show()
            else:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load files!")


def run():
    vp_start_gui()


if __name__ == '__main__':
    run()
