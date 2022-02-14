import logging
import cuid
from datetime import datetime

from app.core.custom_exception import BadRequest
from app.db.mysql_db_connector import MySQLDBConnector
from app.dao.transaction_dao import TransactionDAO
from app.models.transaction import Transaction, TransactionAmount, TransactionType, TransactionStatus
from app.service.account_service import AccountService


class TransactionService(object):
    def __init__(self):
        self.tran_obj = MySQLDBConnector()
        self.tran_obj.create_connection()
        self.dao_obj = TransactionDAO(self.tran_obj)

    def create_transaction(self, account_id: str, amount: TransactionAmount,
                           transaction_type: TransactionType) -> Transaction:
        """
            Method to handle deposit and withdrawal transactions
        :param account_id:
        :param amount:
        :param transaction_type:
        :return:
        """
        try:
            account_service = AccountService()
            account_data = account_service.get_account_details(account_id)

            # TODO: Move validations to separate method
            if not account_data:
                raise BadRequest("Account details not found for ID - %s" % account_id)
            if account_data.account_status != account_data.account_status.active:
                raise BadRequest("Account status is inactive - %s" % account_id)
            if transaction_type == TransactionType.debit and account_data.balance < amount:
                raise BadRequest("Insufficient funds to withdraw")
            transaction_dict = {"transaction_id": cuid.cuid(), "account_id": account_id,
                                "transaction_type": transaction_type,
                                "status": TransactionStatus.success, "amount": amount, "created_at": datetime.now()}
            transaction_data = Transaction(**transaction_dict)
            self.dao_obj.insert_transaction(transaction_data)

            new_balance = self.__get_updated_balance_by_type(transaction_type, account_data.balance, amount)
            account_service.update_account_balance(account_id, balance=new_balance)

            self.tran_obj.save_transaction()
            return transaction_data
        except Exception as error:
            self.tran_obj.rollback_transaction()
            logging.exception("Exception in Creating Transaction: %s" % error)
            raise
        finally:
            self.tran_obj.end_connection()

    def __get_updated_balance_by_type(self, transaction_type: TransactionType, original_balance: float,
                                      tran_amount: TransactionAmount) -> float:
        """
         Private Method to calculate new updated balance by transaction type and account old balance.
        :param transaction_type:
        :param original_balance:
        :param tran_amount:
        :return:
        """
        modified_balance = original_balance
        if transaction_type == TransactionType.credit:
            modified_balance += tran_amount
        else:
            modified_balance -= tran_amount
        return modified_balance
