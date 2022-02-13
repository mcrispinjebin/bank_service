from datetime import datetime

from app.models.account import Account, AccountID, CreateAccountPayload, AccountBalance
from app.models.user import UserID


class AccountDAO(object):
    def __init__(self, tran_obj):
        self.tran_obj = tran_obj

    def insert_account(self, account_data: Account) -> AccountID:
        """
        Method to insert entry in payout table and initiate insert request in payout_status_log table
        :param account_data:
        :return:
        """
        query = "insert into account (user_id, account_type, account_status, balance, created_at, modified_at) values (%s, %s, %s, %s, %s, %s)"
        args = (account_data.user_id, account_data.account_type, account_data.account_status, account_data.balance,
                datetime.now(), None)
        account_id = self.tran_obj.process_query(query, arguments=args, fetch_result=False)
        return account_id

    def insert_user(self, user_data: CreateAccountPayload) -> UserID:
        """
        Method to insert entry in payout table and initiate insert request in payout_status_log table
        :param user_data:
        :return:
        """
        query = "insert into user (first_name, email, nationality, created_at, modified_at) values (%s, %s, %s, %s, %s)"
        args = (user_data.first_name, user_data.email, user_data.nation, datetime.now(), None)
        user_id = self.tran_obj.process_query(query, arguments=args, fetch_result=False)
        return user_id

    def get_user_by_email(self, email) -> dict:
        """

        :param email:
        :return:
        """
        query = "select u.first_name, u.email, u.nationality from user u where u.email=%s"
        args = (email, )
        result = self.tran_obj.process_query(query, arguments=args)
        return result and result[0]

    def get_account_by_id(self, account_id: int) -> dict:
        """

        :param account_id:
        :return:
        """
        query = "select * from account a where a.id=%s"
        args = (account_id, )
        result = self.tran_obj.process_query(query, arguments=args)
        return result and result[0]

    def update_account_balance_by_id(self, account_id: int, balance: AccountBalance):
        """

        :param account_id:
        :param balance:
        :return:
        """
        query = "update account set balance=%s where account_id=%s"
        args = (balance, account_id)
        self.tran_obj.process_query(query, arguments=args, fetch_result=False)



