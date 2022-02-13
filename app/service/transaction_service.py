import logging

from app.db.maria_db_connector import MariaDBConnector
from app.dao.transaction_dao import TransactionDAO
from app.models.transaction import Transaction, TransactionAmount, TransactionType, TransactionID


class TransactionService(object):
    def __init__(self):
        self.tran_obj = MariaDBConnector()
        self.tran_obj.create_connection()
        self.dao_obj = TransactionDAO(self.tran_obj)

    def create_transaction(self, account_id: int, amount: TransactionAmount, transaction_type: TransactionType) -> Transaction:
        """

        :param account_id:
        :param amount:
        :param transaction_type:
        :return:
        """
        try:
            # get account_data by account_id
            account_data = {}
            if not account_data:
                raise Exception("Account details not found for ID - ", account_id)
            if account_data.status != "active":
                raise Exception("Account status is inactive - ", account_id)
            if transaction_type == TransactionType.debit and account_data.balance < amount:  # TODO: store debit in config
                raise Exception("Insufficient funds to withdraw")

            transaction_dict = {"account_id": account_id, "transaction_type": transaction_type, "status": "success",
                                "amount": amount}
            transaction_data = Transaction(**transaction_dict)
            transaction_id = self.dao_obj.insert_transaction(transaction_data)
            transaction_data.transaction_id = transaction_id
            # TODO: update account balance

            self.tran_obj.save_transaction()
            return transaction_data
        except Exception as error:
            self.tran_obj.rollback_transaction()
            logging.exception("Exception in Creating Transaction: ", error)
            raise
        finally:
            self.tran_obj.end_connection()
