import tkinter as tk
from tkinter import messagebox as msg
from tkinter import filedialog
from time import sleep
from os import path
import shutil

disabled_state(), normal_state(), run_progressbar(),


def disabled_state(self):
    self.compression_button.configure(state='disabled')
    self.decompression_button.configure(state='disabled')
    self.save_file_button.configure(state='disabled')
    self.choose_file_button.configure(state='disabled')
    self.file_entry.configure(state='disabled')
    self.new_entry.configure(state='disabled')


def normal_state(self):
    self.decompression_button.configure(text='Decompression', state='normal')
    self.compression_button.configure(text='  Compression  ', state='normal')
    self.save_file_button.configure(state='normal')
    self.choose_file_button.configure(state='normal')
    self.file_entry.configure(state='normal')
    self.new_entry.configure(state='normal')


def run_progressbar(self):
    self.progress_bar["maximum"] = 100
    for i in range(101):
        sleep(0.05)
        self.progress_bar["value"] = i  # increment progressbar
        value = str(i)
        self.scroll.insert(tk.INSERT, value + '%' + '\n')
        self.progress_bar.update()  # have to call update() in loop
        self.scroll.delete("end-2l", "end")
    self.progress_bar["value"] = 0  # reset/clear progressbar


def get_filename(self):
    self.file.set(filedialog.askopenfilename(initialdir=path.expanduser('~'), title="Select file"))


def copy_file(self):
    src = self.file_entry.get()
    file = src.split('/')[-1]
    dst = self.new_entry.get() + '' + file
    try:
        shutil.copy(src, dst)
        msg.showinfo('Copy File to Network', 'Succes:')
    except FileNotFoundError as err:
        msg.showerror('Copy File to Network',
                      '*** Failed to copy file! ***\n\n' +
                      str(err))
    except Exception as ex:
        msg.showerror('Copy File to Network',
                      '*** Failed to copy file! ***\n\n' + str(ex))


def _compression(self):
    self.compression_button.configure(text="     Progress     ")


def _decompression(self):
    self.decompression_button.configure(text="    Progress    ")


def com_start(self):
    self.scroll.insert(tk.INSERT, "Start Compression" + '\n')


def com_end(self):
    self.scroll.insert(tk.INSERT, "End Compression" + '\n')


def dec_start(self):
    self.scroll.insert(tk.INSERT, "Start Decompression" + '\n')


def dec_end(self):
    self.scroll.insert(tk.INSERT, "End Decompression" + '\n')


def clear_scrol(self):
    self.scroll.delete(1.0, tk.END)


@staticmethod
def _quit():
    exit()