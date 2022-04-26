import sqlite3
import sqlalchemy
import pandas as pd


class Database():
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.engine = sqlalchemy.create_engine(
            f'sqlite:///{db_path}', echo=False)

    def find_data(self, table):
        df = pd.read_sql(f'SELECT predictions, player_names, player_ids, file_names, ticks '
                         f'FROM {table} ORDER BY predictions DESC',self.engine)
        print(df.columns)
        return df

    def insert_prediction(self, datadict, table):
        df = pd.DataFrame.from_dict(datadict)
        df.to_sql(table, con=self.engine, if_exists='append')
