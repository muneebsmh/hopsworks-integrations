import json
import logging
from sqlalchemy import create_engine
import pandas as pd

logger = logging.getLogger('logger')


class DbTables:

    def __init__(self, config):
        self.conf = config
        with open(self.conf, "r") as jsonfile:
            data = json.load(jsonfile)

        self.db_host = data['host']
        self.db_name = data['database']
        self.db_user = data['username']
        self.db_password = data['password']

    def get_db_conn(self):
        try:
            logger.info('Trying to establish connection with the database')
            engine = create_engine(f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}",
                                   echo=True)
            conn = engine.connect()
            return conn

        except Exception as e:
            logger.error(e)

        finally:
            logger.info('Database connection successful')

    def close_db_conn(self, conn):
        try:
            conn.close()

        except Exception as e:
            logger.error(e)

        finally:
            logger.info('Database connection closed')

    def run_query(self, conn, query):
        try:
            logger.info('Running query in the database')
            results = conn.execute(query)
            df = pd.DataFrame(results.fetchall())
            return df

        except Exception as e:
            logger.error(e)

        finally:
            logger.info('Query executed successfully')