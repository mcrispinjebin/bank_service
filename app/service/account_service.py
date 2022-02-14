import logging
import cuid
from datetime import datetime

from app.core.custom_exception import BadRequest
from app.db.mysql_db_connector import MySQLDBConnector
from app.dao.account_dao import AccountDAO
from app.models.account import CreateAccountPayload, Account, AccountBalance, AccountStatus, User


class AccountService(object):
    def __init__(self):
        self.tran_obj = MySQLDBConnector()
        self.tran_obj.create_connection()

        self.dao_obj = AccountDAO(self.tran_obj)

    def create_account(self, account_payload: CreateAccountPayload) -> Account:
        """
            Method to create user and thereby create account for same user. If user email exists, return with 400
            status code.
        :param account_payload:
        :return:
        """
        try:
            if self.dao_obj.get_user_by_email(account_payload.email):
                raise BadRequest("Account exists with user email - %s" % account_payload.email)
            user_dict = account_payload.__dict__
            user_dict["user_id"] = cuid.cuid()
            user_data = User(**user_dict)
            self.dao_obj.insert_user(user_data)

            account_dict = {"account_id": cuid.cuid(), "user_id": user_data.user_id,
                            "account_status": AccountStatus.active, "created_at": datetime.now(),
                            "account_type": account_payload.account_type, "balance": account_payload.initial_deposit}
            account_obj = Account(**account_dict)

            self.dao_obj.insert_account(account_obj)
            self.tran_obj.save_transaction()
            return account_obj

        except Exception as error:
            self.tran_obj.rollback_transaction()
            logging.exception("Exception in Creating Account: %s" % error)
            raise
        finally:
            self.tran_obj.end_connection()

    def get_account_details(self, account_id: str) -> Account:
        """
            Method to fetch account details from account ID.
        :param account_id:
        :return:
        """
        try:
            account_details = self.dao_obj.get_account_by_id(account_id)
            if not account_details:
                raise BadRequest("Account does not exists with given ID - %s" % account_id)

            account_data = Account(**account_details)
            return account_data

        except Exception as error:
            logging.exception("Exception in Fetching Account - %s" % error)
            raise

    def update_account_balance(self, account_id: str, balance: AccountBalance) -> Account:
        """
            Method to update account balance by account ID
        :param account_id:
        :param balance:
        :return:
        """
        try:
            account_details = self.dao_obj.get_account_by_id(account_id)
            if not account_details:
                raise BadRequest("Account does not exists with given ID - %s" % account_id)

            self.dao_obj.update_account_balance_by_id(account_id, balance)
            self.tran_obj.save_transaction()

            account_data = Account(**account_details)
            account_data.balance = balance
            return account_data
        except Exception as error:
            self.tran_obj.rollback_transaction()
            logging.exception("Exception in Updating Account - %s" % error)
            raise
        finally:
            self.tran_obj.end_connection()
