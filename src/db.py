import sqlite3
import sqlalchemy
import pandas as pd


class Database():
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.engine = sqlalchemy.create_engine(
            f'sqlite:///{db_path}', echo=False)

    def find_data(self):
        cursor = self.conn.execute('SELECT * FROM mytable')
        return cursor

    def insert_prediction(self, datadict):
        df = pd.DataFrame.from_dict(datadict)
        df.to_sql('mytable', con=self.engine, if_exists='append')

