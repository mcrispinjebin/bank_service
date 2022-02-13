import logging

from app.db.maria_db_connector import MariaDBConnector
from app.dao.account_dao import AccountDAO
from app.models.account import CreateAccountPayload, Account, AccountBalance, AccountID


class AccountService(object):
    def __init__(self):
        self.tran_obj = MariaDBConnector()
        self.tran_obj.create_connection()
        self.dao_obj = AccountDAO(self.tran_obj)

    def create_account(self, account_payload: CreateAccountPayload) -> Account:
        try:
            if self.dao_obj.get_user_by_email(account_payload.email):
                raise Exception("Account exists with user email - ", account_payload.email)
            user_id = self.dao_obj.insert_user(account_payload)

            account_dict = {"user_id": user_id, "account_status": "active",
                            "account_type": account_payload.account_type, "balance": account_payload.initial_deposit}
            account_obj = Account(**account_dict)
            account_id = self.dao_obj.insert_account(account_obj)

            self.tran_obj.save_transaction()
            account_obj.account_id = account_id
            return account_obj

        except Exception as error:
            self.tran_obj.rollback_transaction()
            logging.exception("Exception in Creating Account: ", error)
            raise
        finally:
            self.tran_obj.end_connection()

    def get_account_details(self, account_id: int) -> Account:
        try:
            account_details = self.dao_obj.get_account_by_id(account_id)
            if not account_details:
                raise Exception("Account does not exists with given ID - ", account_id)

            account_data = Account(**account_details)
            return account_data

        except Exception as error:
            logging.exception("Exception in Fetching Account: ", error)
            raise
        finally:
            self.tran_obj.end_connection()

    def update_account_balance(self, account_id: int, balance: AccountBalance) -> Account:
        try:
            account_details = self.dao_obj.get_account_by_id(account_id)
            if not account_details:
                raise Exception("Account does not exists with given ID - ", account_id)

            self.dao_obj.update_account_balance_by_id(account_id, balance)
            self.tran_obj.save_transaction()

            account_data = Account(**account_details)
            account_data.balance = balance
            return account_data
        except Exception as error:
            self.tran_obj.rollback_transaction()
            logging.exception("Exception in Updating Account: ", error)
            raise
        finally:
            self.tran_obj.end_connection()

