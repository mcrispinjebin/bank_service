from datetime import datetime
from app.models.transaction import Transaction, TransactionID


class TransactionDAO(object):
    def __init__(self, tran_obj):
        self.tran_obj = tran_obj

    def insert_transaction(self, transaction_data: Transaction) -> TransactionID:
        """
        Method to insert entry in payout table and initiate insert request in payout_status_log table
        :param transaction_data:
        :return:
        """
        query = "insert into transaction (account_id, transaction_type, status, amount, created_at) values (%s, %s, %s, %s, %s)"
        args = (transaction_data.account_id, transaction_data.transaction_type, transaction_data.status, transaction_data.amount,
                datetime.now())
        transaction_id = self.tran_obj.process_query(query, arguments=args, fetch_result=False)
        return transaction_id
