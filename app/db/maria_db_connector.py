import logging

import mariadb

from app.config import env


class MariaDBConnector(object):

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
            self.db_conn = mariadb.connect(
                user=self.db_properties.get('user'),
                password=self.db_properties.get('password'),
                host=self.db_properties.get('host'),
                port=self.db_properties.get('port'),
                database=self.db_properties.get('database')
            )
            return self.db_conn
        except mariadb.Error as exception:
            logging.exception("Exception in Creating DB connection: ", exception)
            raise

    def process_query(self, query, arguments=None, fetch_result=True, bulk_insert=False, count=None, dictionary=True):
        """
        Method to execute the query and return the obtained result
        :param query:
        :param arguments:
        :param fetch_result:
        :param bulk_insert:
        :param count:
        :param dictionary:
        :return:
        """
        try:
            cursor = self.db_conn.cursor(dictionary=dictionary)
            result = None
            if bulk_insert:
                cursor.executemany(query, arguments)
            else:
                cursor.execute(query, arguments)
                if fetch_result:
                    result = cursor.fetchall()
                    if not dictionary:
                        result_set = []
                        for row in result:
                            result_set.append(row[0])
                        result = result_set
                    else:
                        if count:
                            result = result[:count]
                else:
                    result = cursor.lastrowid
            return result

        except mariadb.Error as exception:
            logging.error("Exception in processing query: ", exception)
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
