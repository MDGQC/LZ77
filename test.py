import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import scrolledtext
from tkinter import filedialog
from time import sleep
from os import path
import shutil
import def_function

class MainApplication(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("LZ77")

        # Menu bar - start
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)
        # Menu bar - end

        # Compression, decompression buttons - start
        mng_command = ttk.LabelFrame(self.root, text='Procedure')
        mng_command.grid(column=1, row=0, sticky='WE', padx=5, pady=5)

        self.compression_button = ttk.Button(mng_command, text="  Compression  ",
                                             command=lambda: [self.disabled_state(), self.clear_scrol(),
                                                              self._compression(), self.com_start(),
                                                              self.run_progressbar(), self.normal_state(),
                                                              self.com_end()])
        self.compression_button.grid(column=0, row=0, sticky=tk.W)

        self.decompression_button = ttk.Button(mng_command, text="Decompression",
                                               command=lambda: [self.disabled_state(), self.clear_scrol(),
                                                                self._decompression(), self.dec_start(),
                                                                self.run_progressbar(), self.normal_state(),
                                                                self.dec_end()])
        self.decompression_button.grid(column=0, row=1, sticky=tk.E)

        for child in mng_command.winfo_children():
            child.grid_configure(padx=6, pady=6)
        # Compression, decompression buttons - end

        # Manage files - start
        manage_files_frame = ttk.LabelFrame(self.root, text=' Manage Files: ')
        manage_files_frame.grid(column=0, row=0, sticky='WE', padx=10, pady=5)

        self.choose_file_button = ttk.Button(manage_files_frame, text="Chosen File", command=self.get_filename)
        self.choose_file_button.grid(column=0, row=0, sticky=tk.W)

        self.file = tk.StringVar()
        self.file_entry = ttk.Entry(manage_files_frame, width=40, textvariable=self.file)
        self.file_entry.grid(column=1, row=0, sticky=tk.W)

        log_dir = tk.StringVar()
        self.new_entry = ttk.Entry(manage_files_frame, width=40, textvariable=log_dir)
        self.new_entry.grid(column=1, row=1, sticky=tk.W)

        self.save_file_button = ttk.Button(manage_files_frame, text="Save File", command=self.copy_file)
        self.save_file_button.grid(column=0, row=1, sticky=tk.E)

        for child in manage_files_frame.winfo_children():
            child.grid_configure(padx=6, pady=6)
        # Manage files - end

        # Message - start
        message_frame = ttk.LabelFrame(self.root, text=' Message Log: ')
        message_frame.grid(columnspan=2, row=2, sticky='WE', padx=10, pady=5)

        scroll_w = 90
        scroll_h = 10
        self.scroll = scrolledtext.ScrolledText(message_frame, width=scroll_w, height=scroll_h, wrap=tk.WORD)
        self.scroll.grid(column=0, row=0, sticky='WE')

        self.progress_bar = ttk.Progressbar(message_frame, orient='horizontal', length=342, mode='determinate')
        self.progress_bar.grid(column=0, row=1, pady=2)

        for child in message_frame.winfo_children():
            child.grid_configure(padx=6, pady=6)
        # Message - end

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
