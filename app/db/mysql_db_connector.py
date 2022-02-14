import logging
import mysql.connector

from app.config import env


class MySQLDBConnector(object):

    def __init__(self):
        self.db_conn = None
        self.db_properties = {'host': env.DB_URL,
                              'user': env.DB_USER, 'password': env.DB_PASS,
                              'database': env.DB_NAME,
                              'port': 3306}

    def create_connection(self):
        """
        Method to create a db connection
        :return:
        """
        try:
            self.db_conn = mysql.connector.connect(
                user=self.db_properties.get('user'),
                passwd=self.db_properties.get('password'),
                host=self.db_properties.get('host'),
                port=self.db_properties.get('port'),
                db=self.db_properties.get('database')
            )
            return self.db_conn
        except Exception as exception:
            logging.exception("Exception in Creating DB connection: ", exception)
            raise

    def process_query(self, query, arguments=None, fetch_result=True):
        """
            Method for DB Wrapper to process query
        :param query:
        :param arguments:
        :param fetch_result:
        :return:
        """
        try:
            cursor = self.db_conn.cursor(dictionary=True)

            cursor.execute(query, arguments)
            if fetch_result:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid
            return result

        except Exception as exception:
            logging.error("Exception in processing query: %s" % exception)
            raise

    def save_transaction(self):
        """
        Method to save the current transaction
        :return:
        """
        self.db_conn.commit()

    def rollback_transaction(self):
        """
        Method to rollback the transaction
        :return:
        """
        self.db_conn.rollback()

    def end_connection(self):
        """
        Method to end the db connection
        :return:
        """
        self.db_conn.close()
