from app.models.transaction import Transaction, TransactionID


class TransactionDAO(object):
    def __init__(self, tran_obj):
        self.tran_obj = tran_obj

    def insert_transaction(self, transaction_data: Transaction) -> TransactionID:
        """
            Method to insert entry in transaction table.
        :param transaction_data:
        :return:
        """
        query = "insert into transaction (transaction_id, account_id, transaction_type, status, amount, created_at) " \
                "values (%s, %s, %s, %s, %s, %s)"
        args = (transaction_data.transaction_id, transaction_data.account_id, transaction_data.transaction_type.value,
                transaction_data.status.value, transaction_data.amount, transaction_data.created_at)
        transaction_id = self.tran_obj.process_query(query, arguments=args, fetch_result=False)
        return transaction_id
