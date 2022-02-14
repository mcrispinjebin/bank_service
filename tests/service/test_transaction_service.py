import pytest
from app.models.transaction import TransactionType
from app.db.mysql_db_connector import MySQLDBConnector
from app.dao.transaction_dao import TransactionDAO
from app.core.custom_exception import BadRequest
from app.service.account_service import AccountService
from app.service.transaction_service import TransactionService
from .test_data import *

PARAMETRIZED_GET_UPDATED_BALANCE = [(TransactionType.credit, 10.0, 50.0, 60.0),
                                    (TransactionType.debit, 10.0, 50.0, 40.0)]

PARAMETRIZED_CREATE_TRANSACTION = [
    (TransactionType.debit, 50.0, mock_get_account_details_empty_dict, True, "Account details not found for ID - 1"),
    (TransactionType.debit, 50.0, mock_get_inactive_account, True, "Account status is inactive - 1"),
    (TransactionType.debit, 50.0, mock_get_small_balance_account, True, "Insufficient funds to withdraw"),
    (TransactionType.debit, 50.0, mock_get_happy_flow_account, False, {"status": "success"})]


class TestTransactionService(object):
    @pytest.mark.test_get_updated_balance_by_type
    @pytest.mark.parametrize('tran_type, amount, balance, expected', PARAMETRIZED_GET_UPDATED_BALANCE)
    def test_get_updated_balance_by_type(self, monkeypatch, tran_type, amount, balance, expected):
        monkeypatch.setattr(MySQLDBConnector, "__init__", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "create_connection", lambda a: None)
        result = TransactionService()._TransactionService__get_updated_balance_by_type(tran_type, balance, amount)
        assert result == expected

    @pytest.mark.test_create_transaction
    @pytest.mark.parametrize('tran_type, amount, account_details, exception, expected', PARAMETRIZED_CREATE_TRANSACTION)
    def test_create_transaction(self, monkeypatch, tran_type, amount, account_details, exception, expected):
        monkeypatch.setattr(MySQLDBConnector, "__init__", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "create_connection", lambda a: None)
        monkeypatch.setattr(AccountService, 'get_account_details', account_details)
        monkeypatch.setattr(TransactionDAO, 'insert_transaction', lambda a, b: 10)
        monkeypatch.setattr(TransactionService, '_TransactionService__get_updated_balance_by_type',
                            lambda a, b, c, d: 100)
        monkeypatch.setattr(AccountService, 'update_account_balance', mock_assert_account_balance)
        monkeypatch.setattr(MySQLDBConnector, "save_transaction", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "end_connection", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "rollback_transaction", lambda a: None)

        if exception:
            with pytest.raises(BadRequest) as e:
                TransactionService().create_transaction("1", amount, tran_type)
                assert str(e) == expected
        else:
            result = TransactionService().create_transaction("1", amount, tran_type)
            assert result.status.value == expected["status"]
