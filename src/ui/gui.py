import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
from anti_cheat import Model


class UI:
    """
    This one might need some refreshing, just quickly implemented file explorer
    """
    def __init__(self):
        # init model
        dirname = os.path.dirname(__file__)
        model_path = os.path.join(dirname, 'utils', 'ml_model.onnx')
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
            self.model.predict_to_terminal(self.filename)
        else:
            raise FileExistsError("No file selected!")


if __name__ == '__main__':
    u = UI()
    u.start()