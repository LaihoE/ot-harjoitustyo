from ui.gui import UI, DataVisualizer
from pandastable import Table, TableModel
import tkinter as tk


if __name__ == '__main__':
    u = UI()
    u.start()
    u.generate_table()
