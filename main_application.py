import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from time import sleep
from os import path
from lz77 import LZ77Algorithm


class MainApplication(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("LZ77")
        self.lz77 = LZ77Algorithm()

        # Compression, decompression buttons - start
        mng_command = ttk.LabelFrame(self.root, text='Procedure:')
        mng_command.grid(column=1, row=0, sticky='WE', padx=5, pady=5)

        self.compression_button = ttk.Button(mng_command, text="  Compression  ",
                                             command=lambda: [self._disabled_state(),
                                                              self._compression(),
                                                              self._normal_state()])
        self.compression_button.grid(column=0, row=0, sticky=tk.W)

        self.decompression_button = ttk.Button(mng_command, text="Decompression",
                                               command=lambda: [self._disabled_state(),
                                                                self._decompression(),
                                                                self._normal_state()])
        self.decompression_button.grid(column=0, row=1, sticky=tk.E)

        for child in mng_command.winfo_children():
            child.grid_configure(padx=6, pady=6)
        # Compression, decompression buttons - end

        # Manage files - start
        files_frame = ttk.LabelFrame(self.root, text=' Files: ')
        files_frame.grid(column=0, row=0, sticky='WE', padx=10, pady=5)

        self.input_file_button = ttk.Button(files_frame, text="Input", command=self._get_input_filepath)
        self.input_file_button.grid(column=0, row=0, sticky=tk.W)

        self.input_file = tk.StringVar()
        self.input_file_entry = ttk.Entry(files_frame, width=40, textvariable=self.input_file)
        self.input_file_entry.grid(column=1, row=0, sticky=tk.W)

        self.output_file_button = ttk.Button(files_frame, text="Output", command=self._get_output_filepath)
        self.output_file_button.grid(column=0, row=1, sticky=tk.E)

        self.output_file = tk.StringVar()
        self.output_file_entry = ttk.Entry(files_frame, width=40, textvariable=self.output_file)
        self.output_file_entry.grid(column=1, row=1, sticky=tk.W)

        for child in files_frame.winfo_children():
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

    def _disabled_state(self):
        self.compression_button.configure(state='disabled')
        self.decompression_button.configure(state='disabled')
        self.output_file_button.configure(state='disabled')
        self.input_file_button.configure(state='disabled')
        self.input_file_entry.configure(state='disabled')
        self.output_file_entry.configure(state='disabled')

    def _normal_state(self):
        self.decompression_button.configure(text='Decompression', state='normal')
        self.compression_button.configure(text='  Compression  ', state='normal')
        self.output_file_button.configure(state='normal')
        self.input_file_button.configure(state='normal')
        self.input_file_entry.configure(state='normal')
        self.output_file_entry.configure(state='normal')

    def _run_progressbar(self):
        self.progress_bar["maximum"] = 100
        for i in range(101):
            sleep(0.02)
            self.progress_bar["value"] = i  # increment progressbar
            value = str(i)
            if i % 10 == 0:
                self.scroll.insert(tk.INSERT, value + '%' + '\n')
                self.scroll.see(tk.END)
            self.progress_bar.update()  # have to call update() in loop
        self.progress_bar["value"] = 0  # reset/clear progressbar
        self.scroll.insert(tk.INSERT, 'Completed!' + '\n')
        self.scroll.see(tk.END)

    def _get_input_filepath(self):
        self.input_file.set(filedialog.askopenfilename(initialdir=path.expanduser('.'), title="Select file"))

    def _get_output_filepath(self):
        self.output_file.set(filedialog.asksaveasfilename())

    def _compression(self):
        try:
            self.lz77.compress(self.input_file, self.output_file)
        except Exception as err:
            self.scroll.insert(tk.INSERT, err.args[0] + '\n')
            self.scroll.see(tk.END)
            return
        self.scroll.insert(tk.INSERT, "Started Compression" + '\n')
        self._run_progressbar()
        self.scroll.see(tk.END)
        self.compression_button.configure(text="     Progress     ")

    def _decompression(self):
        try:
            self.lz77.decompress(self.input_file, self.output_file)
        except Exception as err:
            self.scroll.insert(tk.INSERT, err.args[0] + '\n')
            self.scroll.see(tk.END)
            return
        self.scroll.insert(tk.INSERT, "Started Decompression" + '\n')
        self._run_progressbar()
        self.scroll.see(tk.END)
        self.decompression_button.configure(text="    Progress    ")
