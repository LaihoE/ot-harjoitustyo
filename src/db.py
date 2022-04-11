from multiprocessing.spawn import import_main_path
import sqlite3
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd


class Database():
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db')
        self.engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)

    def find_data(self):
        cursor = self.conn.execute('SELECT * FROM mytable')

    def insert_prediction(self, datadict):
        df = pd.DataFrame.from_dict(datadict)
        df.to_sql('mytable', con=self.engine, if_exists='append')
