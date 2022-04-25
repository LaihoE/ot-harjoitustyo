from ui.gui import UI, DataVisualizer
from pandastable import Table, TableModel
import tkinter as tk
from ui.test import Example


if __name__ == '__main__':
    u = UI()
    u.start()
    d = DataVisualizer()
    d.mainloop()
