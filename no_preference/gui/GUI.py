import csv
import os
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
from tkinter import StringVar, Entry

import matplotlib.pyplot as plt
from wordcloud import WordCloud


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
        web_path = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                                      filetypes=[("csv file", "*.csv")])

        global web_loaded
        web_loaded = 0  # counter to signify if file has been loaded or not
        web_loaded += 1
        eval("self." + type + ".delete(0,END)")
        eval("self." + type + ".insert(0,webPath)")

    def get_social_path(self, type):  # get path of file
        global socialPath
        socialPath = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                                        filetypes=[("csv file", "*.csv")])
        global social_loaded
        social_loaded = 0  # counter to signify if file has been loaded or not
        social_loaded += 1
        eval("self." + type + ".delete(0,END)")
        eval("self." + type + ".insert(0,socialPath)")

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
        self.Label3.configure(text='''Social Media Data''')

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
        self.Label3.configure(text='''Web Browser Data''')

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
        self.Button2.configure(text='''WebBrowser History''')
        self.Button2.configure(command=lambda: load_from_web())  # opening the file directory to choose file

        def load_from_web():
            self.get_web_path("Entry1")
            file_name = "test2"

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
        self.Button3.configure(text='''Social Media''')
        self.Button3.configure(command=lambda: load_from_social())  # opening the file directory to choose file

        def load_from_social():
            self.get_social_path("Entry2")
            file_name = "test2"

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
        updateEntry = StringVar()

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
        updateEntry = StringVar()

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
        self.Entry1.place(relx=0.31, rely=0.78, height=26, relwidth=0.431)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font=font10)
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        # Get file directory
        self.Entry2 = Entry(top)
        self.Entry2.place(relx=0.31, rely=0.70, height=26, relwidth=0.431)
        self.Entry2.configure(background="white")
        self.Entry2.configure(disabledforeground="#a3a3a3")
        self.Entry2.configure(font=font10)
        self.Entry2.configure(foreground="#000000")
        self.Entry2.configure(insertbackground="black")

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
                before_sort_x = []
                before_sort_y = []
                x1 = []
                with open(socialPath, 'r') as f:  # open the file
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:  # for i in row to get a single column out
                            column = i  # column
                            column.replace("{", "")  # removing all special characters
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")

                            separate = ":"  # the count and word of the CSV is separated by :
                            position = column.find(separate)  # find the position of : in the column
                            length = len(newstr3)  # calculates total length of the column
                            word = newstr3[0:position]  # slices the word out of the column
                            count = newstr3[position:length]  # slices the count out of the column
                            before_sort_x.append(word)  # appending it to list
                            before_sort_y.append(int(count))  # appending it to list
                        # sorts both files in same order
                        before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                        # appending biggest value which is sorted to the end
                        y.append(before_sort_y[-1])
                    x1.append(before_sort_x[-1])
                    xword = str(x1)  # removing all special characters
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    x.append(xword2)  # append to x which will be used to display the chart

                if len(x) == 0:  # if column is empty
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:  # else, plots
                    fig, ax = plt.subplots(1, 1)  # changing width of the bar chart
                    ax.set_xlim(-2, 2)
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(y):  # displays the bar chart value
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))
                    plt.bar(x, y)
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
                x1 = []
                before_sort_x = []
                before_sort_y = []

                with open(web_path, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            new_str = column.replace("{", "")
                            new_str2 = new_str.replace("}", "")
                            new_str3 = new_str2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(new_str3)
                            word = new_str3[0:position]
                            count = new_str3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))
                        before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                        y.append(before_sort_y[-1])
                        x1.append(before_sort_x[-1])
                        xword = str(x1)
                        xword2 = xword.replace(":", "")
                        xword2 = xword2.replace("[", "")
                        xword2 = xword2.replace("]", "")
                        xword2 = xword2.replace("'", "")
                        xword2 = xword2.replace("\"", "")
                        x.append(xword2)

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    fig, ax = plt.subplots(1, 1)
                    ax.set_xlim(-2, 2)
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(y):
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))

                    plt.bar(x, y)
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
                before_sort_x = []
                before_sort_y = []
                x1 = []
                y1 = []
                with open(socialPath, 'r') as f:  # opening the file
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(newstr3)
                            word = newstr3[0:position]
                            count = newstr3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))
                        before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                        x1.append(before_sort_x)  # append all the sorted
                        xword = str(x1)
                        xword2 = xword.replace(":", "")
                        xword2 = xword2.replace("[", "")
                        xword2 = xword2.replace("]", "")
                        xword2 = xword2.replace("'", "")
                        xword2 = xword2.replace("\"", "")
                        xword2 = xword2.replace("(", "")
                        xword2 = xword2.replace(")", "")
                        y1.append(before_sort_y)  # append all stored in y
                        x = xword2.split()  # splitting the str and making it into a list
                        yword = str(y1)  # removes special characters
                        yword2 = yword.replace(":", "")
                        yword2 = yword2.replace("[", "")
                        yword2 = yword2.replace("]", "")
                        yword2 = yword2.replace("'", "")
                        yword2 = yword2.replace("\"", "")
                        yword2 = yword2.replace("(", "")
                        yword2 = yword2.replace(")", "")
                        yword2 = yword2.replace(",", "")
                        # splitting the str and making it into a list
                        y = yword2.split()
                        # converting to int to display on graph
                        new_numbers = []
                        for n in y:
                            new_numbers.append(int(n))
                        numbers = new_numbers

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:

                    plt.bar(x, numbers)

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
                before_sort_x = []
                before_sort_y = []
                x1 = []
                y = []
                x = []
                y1 = []
                with open(web_path, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(newstr3)
                            word = newstr3[0:position]
                            count = newstr3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))
                    before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                    x1.append(before_sort_x)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    y1.append(before_sort_y)
                    x = xword2.split()
                    yword = str(y1)
                    yword2 = yword.replace(":", "")
                    yword2 = yword2.replace("[", "")
                    yword2 = yword2.replace("]", "")
                    yword2 = yword2.replace("'", "")
                    yword2 = yword2.replace("\"", "")
                    yword2 = yword2.replace("(", "")
                    yword2 = yword2.replace(")", "")
                    yword2 = yword2.replace(",", "")
                    # splitting the str and making it into a list
                    y = yword2.split()
                    # converting to int to display on graph
                    new_numbers = []
                    for n in y:
                        new_numbers.append(int(n))
                    numbers = new_numbers

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:

                    plt.bar(x, numbers)
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
                before_sort_x = []
                before_sort_y = []
                x1 = []
                with open(web_path, 'r') as f:  # opening the file
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i  # same as above
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(newstr3)
                            word = newstr3[0:position]
                            count = newstr3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))

                    before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                    x1.append(before_sort_x)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace(",", "")

                    if entry_string in xword2:  # if user keyed in string is found in the csv
                        position_of_word = [i + 1 for i, w in enumerate(xword2.split()) if w == entry_string]
                        for positions in position_of_word:
                            pos = positions  # find the position of that word

                        pos -= 1  # minus 1 because using enumerate the numbering starts from 1 instead of 0
                        x = entry_string  # x is the user keyed in string
                        y = (before_sort_y[
                            pos])  # shows the count of that word, position is based on the position of where it is in x

                    elif entry_string not in xword2:  # if word not in the csv
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
                    list_to_show = [y]
                    fig, ax = plt.subplots(1, 1)
                    ax.set_xlim(-2, 2)  # decreases the width of the bar
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(list_to_show):
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))
                    plt.bar(x, y)
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
                before_sort_x = []
                before_sort_y = []
                x1 = []
                with open(socialPath, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(newstr3)
                            word = newstr3[0:position]
                            count = newstr3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))

                    before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                    x1.append(before_sort_x)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace(",", "")

                    if entry_string in xword2:
                        position_of_word = [i + 1 for i, w in enumerate(xword2.split()) if w == entry_string]
                        for positions in position_of_word:
                            pos = positions

                        pos -= 1  # minus 1 because using enumerate the numbering starts from 1 instead of 0
                        x = entry_string
                        y = (before_sort_y[pos])

                    elif entry_string not in xword2:
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
                    list_to_show = [y]
                    fig, ax = plt.subplots(1, 1)
                    ax.set_xlim(-2, 2)
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(list_to_show):
                        plt.text(xlocs[i] - -2, v + 0.01, str(v))
                    plt.bar(x, y)
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
                before_sort_x = []
                before_sort_y = []
                before_sort_x2 = []
                before_sort_y2 = []
                x = []
                y = []
                x1 = []
                with open(socialPath, 'r') as f:  # opening the file
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            new_str = column.replace("{", "")
                            new_str2 = new_str.replace("}", "")
                            new_str3 = new_str2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(new_str3)
                            word = new_str3[0:position]
                            count = new_str3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))

                    before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                    # appends the first file of social media to x and y
                    x.append(f'Social Media Data: {before_sort_x[-1]}')
                    y.append(before_sort_y[-1])

                with open(web_path, 'r') as f:  # opening the web file
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            new_str = column.replace("{", "")
                            new_str2 = new_str.replace("}", "")
                            new_str3 = new_str2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(new_str3)
                            word = new_str3[0:position]
                            count = new_str3[position:length]
                            before_sort_x2.append(word)
                            before_sort_y2.append(int(count))

                    before_sort_y2, before_sort_x2 = zip(*sorted(zip(before_sort_y2, before_sort_x2)))
                    # appending web file in to x and y
                    x.append(f'Web Browser Data: {before_sort_x2[-1]}')
                    y.append(before_sort_y2[-1])

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(y):
                        plt.text(xlocs[i] - -0.36, v + 0.01, str(v))
                    plt.bar(x, y)
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
                before_sort_x = []
                before_sort_y = []
                before_sort_x2 = []
                before_sort_y2 = []
                x = []
                y = []
                x1 = []
                x2 = []
                with open(socialPath, 'r') as f:  # opening the file
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(newstr3)
                            word = newstr3[0:position]
                            count = newstr3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))
                    before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                    x1.append(before_sort_x)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace(",", "")
                    if entry_string in xword2:  # if word found in the csv
                        position_of_word = [i + 1 for i, w in enumerate(xword2.split()) if w == entry_string]
                        for positions in position_of_word:
                            pos = positions  # get position of the word

                        pos -= 1  # minus 1 because using enumerate the numbering starts from 1 instead of 0
                        x.append(f'Social Media Data: {entry_string}')  # appending the data to x and y axis
                        y.append(before_sort_y[pos])

                    elif entry_string not in xword2:
                        plt.title('No Data to be Found\n')
                        plt.xlabel('Word')
                        plt.ylabel('Counts')
                        plt.show()

                with open(web_path, 'r') as f:  # opening the web browser file
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(newstr3)
                            word = newstr3[0:position]
                            count = newstr3[position:length]
                            before_sort_x2.append(word)
                            before_sort_y2.append(int(count))
                    before_sort_y2, before_sort_x2 = zip(*sorted(zip(before_sort_y2, before_sort_x2)))
                    x2.append(before_sort_x2)
                    xword3 = str(x2)
                    xword4 = xword3.replace(":", "")
                    xword4 = xword4.replace("[", "")
                    xword4 = xword4.replace("]", "")
                    xword4 = xword4.replace("'", "")
                    xword4 = xword4.replace("\"", "")
                    xword4 = xword4.replace("(", "")
                    xword4 = xword4.replace(")", "")
                    xword4 = xword4.replace(",", "")

                    if entry_string in xword4:
                        positionofword2 = [i + 1 for i, w in enumerate(xword4.split()) if w == entry_string]
                        for positions in positionofword2:
                            pos2 = positions

                        pos2 -= 1  # minus 1 because using enumerate the numbering starts from 1 instead of 0

                        x.append(f'Web Browser Data: {entry_string}')  # appending web browser data to x and y axis
                        y.append(before_sort_y2[pos2])

                    elif entry_string not in xword2:
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
                    xlocs, xlabs = plt.xticks()
                    for i, v in enumerate(y):
                        plt.text(xlocs[i] - -0.36, v + 0.01, str(v))
                    plt.bar(x, y)
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

            reversed_string = ''.join(reversed(filename))

            if web_loaded < 1:
                win3 = tk.Toplevel()
                win3.geometry('300x200')
                win3.wm_title("Error")
                label3 = tk.Label(win3)
                label3.place(relx=0.100, rely=0.151, relheight=0.7, relwidth=0.8)
                label3.config(text="Please load a file!")
            elif web_loaded >= 1:
                before_sort_x = []
                before_sort_y = []
                x1 = []
                y = []
                x = []
                y1 = []
                with open(web_path, 'r') as f:

                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            new_str = column.replace("{", "")
                            new_str2 = new_str.replace("}", "")
                            new_str3 = new_str2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(new_str3)
                            word = new_str3[0:position]
                            count = new_str3[position:length]
                            before_sort_x.append(word)

                            before_sort_y.append(int(count))
                    before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                    x1.append(before_sort_x)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace("/", "-")
                    xword2 = xword2.replace(",", "")
                    y1.append(before_sort_y)
                    x = xword2.split()
                    yword = str(y1)
                    yword2 = yword.replace(":", "")
                    yword2 = yword2.replace("[", "")
                    yword2 = yword2.replace("]", "")
                    yword2 = yword2.replace("'", "")
                    yword2 = yword2.replace("\"", "")
                    yword2 = yword2.replace("(", "")
                    yword2 = yword2.replace(")", "")
                    yword2 = yword2.replace(",", "")

                    y = yword2.split()
                    new_numbers = [];  # converting to int to display on graph
                    for n in y:
                        new_numbers.append(int(n));
                    numbers = new_numbers;
                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    plt.bar(x, numbers)  # rotation so to fill more graphs without the names colliding
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

        def social_timeline():  # getting timeline for web
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
                before_sort_x = []
                before_sort_y = []
                x1 = []
                y = []
                x = []
                y1 = []
                with open(socialPath, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            new_str = column.replace("{", "")
                            new_str2 = new_str.replace("}", "")
                            new_str3 = new_str2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            length = len(new_str3)
                            word = new_str3[0:position]
                            count = new_str3[position:length]
                            before_sort_x.append(word)
                            before_sort_y.append(int(count))
                    before_sort_y, before_sort_x = zip(*sorted(zip(before_sort_y, before_sort_x)))
                    x1.append(before_sort_x)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace("/", "-")
                    xword2 = xword2.replace(",", "")
                    y1.append(before_sort_y)
                    x = xword2.split()
                    yword = str(y1)
                    yword2 = yword.replace(":", "")
                    yword2 = yword2.replace("[", "")
                    yword2 = yword2.replace("]", "")
                    yword2 = yword2.replace("'", "")
                    yword2 = yword2.replace("\"", "")
                    yword2 = yword2.replace("(", "")
                    yword2 = yword2.replace(")", "")
                    yword2 = yword2.replace(",", "")

                    y = yword2.split()

                    # converting to int to display on graph
                    new_numbers = []
                    for n in y:
                        new_numbers.append(int(n))
                    numbers = new_numbers
                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    plt.bar(x, numbers)  # rotation so to fill more graphs without the names colliding
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
                beforeSortx = []
                x1 = []
                with open(socialPath, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            word = newstr3[0:position]
                            beforeSortx.append(word)
                    x1.append(beforeSortx)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace("/", "-")
                    xword2 = xword2.replace(",", "")
                    x = xword2.split()
                    xcloud = str(x)

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    wordcloud = WordCloud(max_font_size=40).generate(xcloud)
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
                beforeSortx = []
                x1 = []
                with open(web_path, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            word = newstr3[0:position]
                            beforeSortx.append(word)
                    x1.append(beforeSortx)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace("/", "-")
                    xword2 = xword2.replace(",", "")
                    x = xword2.split()
                    xcloud = str(x)

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    wordcloud = WordCloud(max_font_size=40).generate(xcloud)
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
                before_sort_x = []
                before_sort_x2 = []
                x1 = []
                x = []
                x4 = []
                with open(web_path, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            word = newstr3[0:position]
                            before_sort_x.append(word)
                    x1.append(before_sort_x)
                    xword = str(x1)
                    xword2 = xword.replace(":", "")
                    xword2 = xword2.replace("[", "")
                    xword2 = xword2.replace("]", "")
                    xword2 = xword2.replace("'", "")
                    xword2 = xword2.replace("\"", "")
                    xword2 = xword2.replace("(", "")
                    xword2 = xword2.replace(")", "")
                    xword2 = xword2.replace("/", "-")
                    x.append(xword2)

                with open(socialPath, 'r') as f:
                    plots = csv.reader(f, delimiter=',')
                    for row in plots:
                        for i in row:
                            column = i
                            column.replace("{", "")
                            newstr = column.replace("{", "")
                            newstr2 = newstr.replace("}", "")
                            newstr3 = newstr2.replace(" ", "")
                            column.strip("}")
                            separate = ":"
                            position = column.find(separate)
                            wordpart2 = newstr3[0:position]
                            before_sort_x2.append(wordpart2)
                    x4.append(before_sort_x2)
                    xwording = str(x4)
                    xwording2 = xwording.replace(":", "")
                    xwording2 = xwording2.replace("[", "")
                    xwording2 = xwording2.replace("]", "")
                    xwording2 = xwording2.replace("'", "")
                    xwording2 = xwording2.replace("\"", "")
                    xwording2 = xwording2.replace("(", "")
                    xwording2 = xwording2.replace(")", "")
                    xwording2 = xwording2.replace("/", "-")
                    x.append(xwording2)
                    xcloud = str(x)

                if len(x) == 0:
                    plt.title('No Data to be Found\n')
                    plt.xlabel('Word')
                    plt.ylabel('Counts')
                    plt.show()
                else:
                    word_cloud = WordCloud(max_font_size=40).generate(xcloud)
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


if __name__ == '__main__':
    vp_start_gui()
