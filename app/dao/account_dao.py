from datetime import datetime

from app.models.account import Account, AccountBalance, AccountStatus, User
from app.models.user import UserID


class AccountDAO(object):
    def __init__(self, tran_obj):
        self.tran_obj = tran_obj

    def insert_account(self, account_data: Account):
        """
            Method to insert account record.
        :param account_data:
        :param user_id:
        :return:
        """
        query = "insert into account (account_id, user_id, account_type, account_status, balance, created_at, " \
                "modified_at) values (%s, %s, %s, %s, %s, %s, %s)"
        args = (account_data.account_id, account_data.user_id, account_data.account_type.value,
                AccountStatus.active.value, account_data.balance, account_data.created_at, None)
        account_id = self.tran_obj.process_query(query, arguments=args, fetch_result=False)
        return account_id

    def insert_user(self, user_data: User) -> UserID:
        """
            Method to insert user entry in user table
        :param user_data:
        :return:
        """
        query = "insert into user (user_id, first_name, email, nationality, created_at, modified_at) " \
                "values (%s, %s, %s, %s, %s, %s)"
        args = (user_data.user_id, user_data.first_name, user_data.email, user_data.nation, datetime.now(), None)
        user_id = self.tran_obj.process_query(query, arguments=args, fetch_result=False)
        return user_id

    def get_user_by_email(self, email) -> dict:
        """
            Method to fetch user information by user email
        :param email:
        :return:
        """
        query = "select u.first_name, u.email, u.nationality from user u where u.email=%s"
        args = (email,)
        result = self.tran_obj.process_query(query, arguments=args)
        return result and result[0]

    def get_account_by_id(self, account_id: str) -> dict:
        """
            Method to fetch account details by account ID
        :param account_id:
        :return:
        """
        query = "select * from account a where a.account_id=%s"
        args = (account_id,)
        result = self.tran_obj.process_query(query, arguments=args)
        return result and result[0]

    def update_account_balance_by_id(self, account_id: str, balance: AccountBalance):
        """
            Method to update account balance by account ID
        :param account_id:
        :param balance:
        :return:
        """
        query = "update account set balance=%s, modified_at=%s where account_id=%s"
        args = (balance, datetime.now(), account_id)
        self.tran_obj.process_query(query, arguments=args, fetch_result=False)
