import sqlite3
import sqlalchemy
import pandas as pd


class Database():
    def __init__(self, db_path) -> None:
        """

        :param db_path: Path where db is
        """
        """
        Creates two connections, one for pythons native sqlite3 and one for
        sqlalchemy. Sqlalchemy is needed for df.to_sql()

        :param db_path: path to db file
        """
        self.conn = sqlite3.connect(db_path)
        self.engine = sqlalchemy.create_engine(
            f'sqlite:///{db_path}', echo=False)

    def find_data(self, table):
        """
        Query SQL database with pd.read_sql()

        :param table: Table where we query from
        :return: df
        """
        df = pd.read_sql(f'SELECT predictions, player_names, player_ids, file_names, ticks '
                         f'FROM {table} ORDER BY predictions DESC',self.engine)
        return df

    def insert_prediction(self, datadict, table):
        """
        Inserts predictions to sql using pandas df.to_sql()

        :param datadict: Dictionary containing all insertable data
        :param table: table name where we insert
        :return:
        """
        df = pd.DataFrame.from_dict(datadict)
        df.to_sql(table, con=self.engine, if_exists='append')
