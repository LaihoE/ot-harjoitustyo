import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
from anti_cheat import Model
from tkinter import *
from pandastable import Table, TableModel
from db import Database


class UI:
    """
    This one might need some refreshing, just quickly implemented file explorer
    """
    def __init__(self):
        # init model
        dirname = os.path.dirname(__file__)
        model_path = os.path.join(dirname, '..', 'utils', 'ml_model.onnx')
        self.model = Model(model_path)
        # Init tkinter
        self.root = tk.Tk()
        self.root.title('DLAC')
        self.root.geometry('300x150')
        self.filename = None
        self.open_button = ttk.Button(
            self.root,
            text='Select csv file (game to analyse)',
            command=self.select_game
        )

    def select_game(self):
        filetypes = (
            ('CSV', '*.csv'),
        )
        dirname = os.path.dirname(__file__)
        csv_folder_path = os.path.join(dirname, 'csvs')
        self.filename = fd.askopenfilename(
            title='Select csv file (game to analyse)',
            initialdir=csv_folder_path,
            filetypes=filetypes,
        )
        self.root.destroy()

    def start(self):
        self.open_button.pack(expand=True)
        self.root.mainloop()
        if self.filename is not None:
            self.model.predict_to_sql(self.filename)
        else:
            raise FileExistsError("No file selected!")


class DataVisualizer(Frame):
        def __init__(self, parent=None):
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('600x400+200+100')
            self.main.title('Table app')
            f = Frame(self.main)
            f.pack(fill=BOTH, expand=1)

            dirname = os.path.dirname(__file__)
            path_to_db = os.path.join(dirname, '..', 'database', 'database.db')
            db = Database(path_to_db)
            df = db.find_data('mytable')

            self.table = pt = Table(f, dataframe=df,
                                    showtoolbar=True, showstatusbar=True)
            pt.show()
