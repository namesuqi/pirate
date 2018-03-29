#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Feb 28, 2018 02:43:54 PM
import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

import unknown_support


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = AndroidTool(root)
    unknown_support.init(root, top)
    root.mainloop()


w = None


def create_AndroidTool(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel(root)
    top = AndroidTool(w)
    unknown_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_AndroidTool():
    global w
    w.destroy()
    w = None


class AndroidTool:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'

        top.geometry("616x388+607+202")
        top.title("AndroidTool")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.06, rely=0.05, relheight=0.17, relwidth=0.87)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=535)

        self.ButtonStartApplication = Button(self.Frame1)
        self.ButtonStartApplication.place(relx=0.58, rely=0.18, height=40
                                          , width=100)
        self.ButtonStartApplication.configure(activebackground="#d9d9d9")
        self.ButtonStartApplication.configure(activeforeground="#000000")
        self.ButtonStartApplication.configure(background="#80ff80")
        self.ButtonStartApplication.configure(command=unknown_support.start)
        self.ButtonStartApplication.configure(disabledforeground="#a3a3a3")
        self.ButtonStartApplication.configure(foreground="#000000")
        self.ButtonStartApplication.configure(highlightbackground="#d9d9d9")
        self.ButtonStartApplication.configure(highlightcolor="black")
        self.ButtonStartApplication.configure(pady="0")
        self.ButtonStartApplication.configure(text='''Start App''')

        self.ButtonStopApplication = Button(self.Frame1)
        self.ButtonStopApplication.place(relx=0.79, rely=0.18, height=40
                                         , width=100)
        self.ButtonStopApplication.configure(activebackground="#d9d9d9")
        self.ButtonStopApplication.configure(activeforeground="#000000")
        self.ButtonStopApplication.configure(background="#ff8080")
        self.ButtonStopApplication.configure(command=unknown_support.stop)
        self.ButtonStopApplication.configure(disabledforeground="#a3a3a3")
        self.ButtonStopApplication.configure(foreground="#000000")
        self.ButtonStopApplication.configure(highlightbackground="#d9d9d9")
        self.ButtonStopApplication.configure(highlightcolor="black")
        self.ButtonStopApplication.configure(pady="0")
        self.ButtonStopApplication.configure(text='''Stop App''')

        self.ButtonGetSN = Button(self.Frame1)
        self.ButtonGetSN.place(relx=0.39, rely=0.2, height=40, width=80)
        self.ButtonGetSN.configure(activebackground="#d9d9d9")
        self.ButtonGetSN.configure(activeforeground="#000000")
        self.ButtonGetSN.configure(background="#ffffff")
        self.ButtonGetSN.configure(command=unknown_support.get)
        self.ButtonGetSN.configure(disabledforeground="#a3a3a3")
        self.ButtonGetSN.configure(foreground="#000000")
        self.ButtonGetSN.configure(highlightbackground="#d9d9d9")
        self.ButtonGetSN.configure(highlightcolor="black")
        self.ButtonGetSN.configure(pady="0")
        self.ButtonGetSN.configure(text='''Get SN''')

        self.ButtonInstall = Button(self.Frame1)
        self.ButtonInstall.place(relx=0.04, rely=0.18, height=40, width=80)
        self.ButtonInstall.configure(activebackground="#d9d9d9")
        self.ButtonInstall.configure(activeforeground="#000000")
        self.ButtonInstall.configure(background="#80ff80")
        self.ButtonInstall.configure(command=unknown_support.install)
        self.ButtonInstall.configure(disabledforeground="#a3a3a3")
        self.ButtonInstall.configure(foreground="#000000")
        self.ButtonInstall.configure(highlightbackground="#d9d9d9")
        self.ButtonInstall.configure(highlightcolor="black")
        self.ButtonInstall.configure(pady="0")
        self.ButtonInstall.configure(text='''Install''')
        self.ButtonInstall.configure(width=69)

        self.ButtonUninstall = Button(self.Frame1)
        self.ButtonUninstall.place(relx=0.21, rely=0.2, height=40, width=80)
        self.ButtonUninstall.configure(activebackground="#d9d9d9")
        self.ButtonUninstall.configure(activeforeground="#000000")
        self.ButtonUninstall.configure(background="#ff8080")
        self.ButtonUninstall.configure(command=unknown_support.uninstall)
        self.ButtonUninstall.configure(disabledforeground="#a3a3a3")
        self.ButtonUninstall.configure(foreground="#000000")
        self.ButtonUninstall.configure(highlightbackground="#d9d9d9")
        self.ButtonUninstall.configure(highlightcolor="black")
        self.ButtonUninstall.configure(pady="0")
        self.ButtonUninstall.configure(text='''Uninstall''')

        self.Labelframe1 = LabelFrame(top)
        self.Labelframe1.place(relx=0.06, rely=0.49, relheight=0.22
                               , relwidth=0.88)
        self.Labelframe1.configure(relief=GROOVE)
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Push''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")
        self.Labelframe1.configure(width=540)

        self.ButtonPushMeta = Button(self.Labelframe1)
        self.ButtonPushMeta.place(relx=0.39, rely=0.24, height=40, width=150)
        self.ButtonPushMeta.configure(activebackground="#d9d9d9")
        self.ButtonPushMeta.configure(activeforeground="#000000")
        self.ButtonPushMeta.configure(background="#ffff00")
        self.ButtonPushMeta.configure(command=unknown_support.push_meta)
        self.ButtonPushMeta.configure(disabledforeground="#a3a3a3")
        self.ButtonPushMeta.configure(foreground="#000000")
        self.ButtonPushMeta.configure(highlightbackground="#d9d9d9")
        self.ButtonPushMeta.configure(highlightcolor="black")
        self.ButtonPushMeta.configure(pady="0")
        self.ButtonPushMeta.configure(text='''Push Meta''')

        self.ButtonPushConf = Button(self.Labelframe1)
        self.ButtonPushConf.place(relx=0.06, rely=0.24, height=40, width=150)
        self.ButtonPushConf.configure(activebackground="#d9d9d9")
        self.ButtonPushConf.configure(activeforeground="#000000")
        self.ButtonPushConf.configure(background="#ffff00")
        self.ButtonPushConf.configure(command=unknown_support.push_conf)
        self.ButtonPushConf.configure(disabledforeground="#a3a3a3")
        self.ButtonPushConf.configure(foreground="#000000")
        self.ButtonPushConf.configure(highlightbackground="#d9d9d9")
        self.ButtonPushConf.configure(highlightcolor="black")
        self.ButtonPushConf.configure(pady="0")
        self.ButtonPushConf.configure(text='''Push Conf''')

        self.ButtonPushData = Button(self.Labelframe1)
        self.ButtonPushData.place(relx=0.7, rely=0.24, height=40, width=150)
        self.ButtonPushData.configure(activebackground="#d9d9d9")
        self.ButtonPushData.configure(activeforeground="#000000")
        self.ButtonPushData.configure(background="#ffff00")
        self.ButtonPushData.configure(command=unknown_support.push_data)
        self.ButtonPushData.configure(disabledforeground="#a3a3a3")
        self.ButtonPushData.configure(foreground="#000000")
        self.ButtonPushData.configure(highlightbackground="#d9d9d9")
        self.ButtonPushData.configure(highlightcolor="black")
        self.ButtonPushData.configure(pady="0")
        self.ButtonPushData.configure(text='''Push Data''')

        self.Labelframe2 = LabelFrame(top)
        self.Labelframe2.place(relx=0.06, rely=0.72, relheight=0.22
                               , relwidth=0.88)
        self.Labelframe2.configure(relief=GROOVE)
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Delete''')
        self.Labelframe2.configure(background="#d9d9d9")
        self.Labelframe2.configure(highlightbackground="#d9d9d9")
        self.Labelframe2.configure(highlightcolor="black")
        self.Labelframe2.configure(width=540)

        self.lab51_but52 = Button(self.Labelframe2)
        self.lab51_but52.place(relx=0.39, rely=0.24, height=40, width=150)
        self.lab51_but52.configure(activebackground="#d9d9d9")
        self.lab51_but52.configure(activeforeground="#000000")
        self.lab51_but52.configure(background="#0080ff")
        self.lab51_but52.configure(command=unknown_support.delete_meta)
        self.lab51_but52.configure(disabledforeground="#a3a3a3")
        self.lab51_but52.configure(foreground="#000000")
        self.lab51_but52.configure(highlightbackground="#d9d9d9")
        self.lab51_but52.configure(highlightcolor="black")
        self.lab51_but52.configure(pady="0")
        self.lab51_but52.configure(text='''Delete Meta''')

        self.lab51_but53 = Button(self.Labelframe2)
        self.lab51_but53.place(relx=0.06, rely=0.24, height=40, width=150)
        self.lab51_but53.configure(activebackground="#d9d9d9")
        self.lab51_but53.configure(activeforeground="#000000")
        self.lab51_but53.configure(background="#0080ff")
        self.lab51_but53.configure(command=unknown_support.delete_conf)
        self.lab51_but53.configure(disabledforeground="#a3a3a3")
        self.lab51_but53.configure(foreground="#000000")
        self.lab51_but53.configure(highlightbackground="#d9d9d9")
        self.lab51_but53.configure(highlightcolor="black")
        self.lab51_but53.configure(pady="0")
        self.lab51_but53.configure(text='''Delete Conf''')

        self.ButtonDeleteData = Button(self.Labelframe2)
        self.ButtonDeleteData.place(relx=0.7, rely=0.24, height=40, width=150)
        self.ButtonDeleteData.configure(activebackground="#d9d9d9")
        self.ButtonDeleteData.configure(activeforeground="#000000")
        self.ButtonDeleteData.configure(background="#0080ff")
        self.ButtonDeleteData.configure(command=unknown_support.delete_data)
        self.ButtonDeleteData.configure(disabledforeground="#a3a3a3")
        self.ButtonDeleteData.configure(foreground="#000000")
        self.ButtonDeleteData.configure(highlightbackground="#d9d9d9")
        self.ButtonDeleteData.configure(highlightcolor="black")
        self.ButtonDeleteData.configure(pady="0")
        self.ButtonDeleteData.configure(text='''Delete Data''')

        self.Labelframe3 = LabelFrame(top)
        self.Labelframe3.place(relx=0.06, rely=0.26, relheight=0.22
                               , relwidth=0.88)
        self.Labelframe3.configure(relief=GROOVE)
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''Pull''')
        self.Labelframe3.configure(background="#d9d9d9")
        self.Labelframe3.configure(highlightbackground="#d9d9d9")
        self.Labelframe3.configure(highlightcolor="black")
        self.Labelframe3.configure(width=540)

        self.ButtonPullMeta = Button(self.Labelframe3)
        self.ButtonPullMeta.place(relx=0.38, rely=0.24, height=40, width=150)
        self.ButtonPullMeta.configure(activebackground="#d9d9d9")
        self.ButtonPullMeta.configure(activeforeground="#000000")
        self.ButtonPullMeta.configure(background="#80ffff")
        self.ButtonPullMeta.configure(command=unknown_support.pull_meta)
        self.ButtonPullMeta.configure(disabledforeground="#a3a3a3")
        self.ButtonPullMeta.configure(foreground="#000000")
        self.ButtonPullMeta.configure(highlightbackground="#d9d9d9")
        self.ButtonPullMeta.configure(highlightcolor="black")
        self.ButtonPullMeta.configure(pady="0")
        self.ButtonPullMeta.configure(text='''Pull Meta''')

        self.ButtonPullConf = Button(self.Labelframe3)
        self.ButtonPullConf.place(relx=0.06, rely=0.22, height=40, width=150)
        self.ButtonPullConf.configure(activebackground="#d9d9d9")
        self.ButtonPullConf.configure(activeforeground="#000000")
        self.ButtonPullConf.configure(background="#80ffff")
        self.ButtonPullConf.configure(command=unknown_support.pull_conf)
        self.ButtonPullConf.configure(disabledforeground="#a3a3a3")
        self.ButtonPullConf.configure(foreground="#000000")
        self.ButtonPullConf.configure(highlightbackground="#d9d9d9")
        self.ButtonPullConf.configure(highlightcolor="black")
        self.ButtonPullConf.configure(pady="0")
        self.ButtonPullConf.configure(text='''Pull Conf''')

        self.ButtonPullData = Button(self.Labelframe3)
        self.ButtonPullData.place(relx=0.69, rely=0.22, height=40, width=150)
        self.ButtonPullData.configure(activebackground="#d9d9d9")
        self.ButtonPullData.configure(activeforeground="#000000")
        self.ButtonPullData.configure(background="#80ffff")
        self.ButtonPullData.configure(command=unknown_support.pull_data)
        self.ButtonPullData.configure(disabledforeground="#a3a3a3")
        self.ButtonPullData.configure(foreground="#000000")
        self.ButtonPullData.configure(highlightbackground="#d9d9d9")
        self.ButtonPullData.configure(highlightcolor="black")
        self.ButtonPullData.configure(pady="0")
        self.ButtonPullData.configure(text='''Pull Data''')

        self.menubar = Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.menubar.add_command(
            activebackground="#d8d8d8",
            activeforeground="#000000",
            background="#d9d9d9",
            command=unknown_support.quit,
            font="TkMenuFont",
            foreground="#000000",
            label="Exit")


if __name__ == '__main__':
    vp_start_gui()
