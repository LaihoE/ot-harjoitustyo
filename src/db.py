import sqlite3
import sqlalchemy
import pandas as pd


class Database():
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database/database.db')
        self.engine = sqlalchemy.create_engine(
            'sqlite:///database/database.db', echo=False)

    def find_data(self):
        cursor = self.conn.execute('SELECT * FROM mytable')
        return cursor

    def insert_prediction(self, datadict):
        df = pd.DataFrame.from_dict(datadict)
        df.to_sql('mytable', con=self.engine, if_exists='append')
