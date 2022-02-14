import pytest
from app.db.mysql_db_connector import MySQLDBConnector
from app.dao.account_dao import AccountDAO
from app.service.account_service import AccountService
from app.core.custom_exception import BadRequest
from .test_data import *

PARAMETRIZED_GET_ACCOUNT_DETAILS = [(mock_get_account_dict, False, ACCOUNT_DICT),
                                    (mock_get_account_dict_exception, True, "DB Exception")]

PARAMETRIZED_UPDATE_ACCOUNT_BALANCE = [
    (500.0, mock_get_account_empty_dict, BadRequest, "Account does not exists with given ID - 1"),
    (500.0, mock_get_account_dict, False, 500.0),
    (500.0, mock_get_account_dict_exception, Exception, "DB Exception")]

PARAMETRIZED_CREATE_ACCOUNT = [
    (acc_payload, mock_get_user, BadRequest, "Account exists with user email - %s" % acc_payload.email),
    (acc_payload, mock_get_user_empty, False, {"account_status": "active", "balance": 120.0}),
    (acc_payload, mock_get_user_exception, Exception, "DB Exception")]


class TestAccountService(object):
    @pytest.mark.test_get_account_details
    @pytest.mark.parametrize('get_account, exception, expected', PARAMETRIZED_GET_ACCOUNT_DETAILS)
    def test_get_account_details(self, monkeypatch, get_account, exception, expected):
        monkeypatch.setattr(MySQLDBConnector, "__init__", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "create_connection", lambda a: None)
        monkeypatch.setattr(AccountDAO, 'get_account_by_id', get_account)
        if exception:
            with pytest.raises(Exception) as e:
                AccountService().get_account_details("1")
            assert str(e.value) == expected
        else:
            result = AccountService().get_account_details("1")
            assert result.__dict__ == Account(**expected).__dict__

    @pytest.mark.test_update_account_balance
    @pytest.mark.parametrize('balance, get_account, exception, expected', PARAMETRIZED_UPDATE_ACCOUNT_BALANCE)
    def test_update_account_balance(self, monkeypatch, balance, get_account, exception, expected):
        monkeypatch.setattr(MySQLDBConnector, "__init__", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "create_connection", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "save_transaction", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "end_connection", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "rollback_transaction", lambda a: None)

        monkeypatch.setattr(AccountDAO, 'get_account_by_id', get_account)
        monkeypatch.setattr(AccountDAO, 'update_account_balance_by_id', lambda a, b, c: None)
        if exception:
            with pytest.raises(exception) as e:
                AccountService().update_account_balance("1", balance)
            assert str(e.value) == expected
        else:
            result = AccountService().update_account_balance("1", balance)
            assert result.balance == expected

    @pytest.mark.test_create_account
    @pytest.mark.parametrize('account_payload, get_user, exception, expected', PARAMETRIZED_CREATE_ACCOUNT)
    def test_create_account(self, monkeypatch, account_payload, get_user, exception, expected):
        monkeypatch.setattr(MySQLDBConnector, "__init__", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "create_connection", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "save_transaction", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "end_connection", lambda a: None)
        monkeypatch.setattr(MySQLDBConnector, "rollback_transaction", lambda a: None)

        monkeypatch.setattr(AccountDAO, 'get_user_by_email', get_user)
        monkeypatch.setattr(AccountDAO, 'insert_user', lambda a, b: None)
        monkeypatch.setattr(AccountDAO, 'insert_account', lambda a, b: None)
        if exception:
            with pytest.raises(exception) as e:
                AccountService().create_account(account_payload)
            assert str(e.value) == expected
        else:
            result = AccountService().create_account(account_payload)
            assert result.balance == expected["balance"]
            assert result.account_status.value == expected["account_status"]
