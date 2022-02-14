from app.models.account import CreateAccountPayload, Account

ACCOUNT_DICT = {"account_id": "1", "user_id": "1", "account_status": "inactive", "account_type": "saving",
                "balance": 20}

ACCOUNT_PAYLOAD = {"first_name": "Crispin", "email": "crispin@gmail.com", "nation": "india", "account_type": "saving",
                   "initial_deposit": 120}
acc_payload = CreateAccountPayload(**ACCOUNT_PAYLOAD)


def mock_get_account_dict(self, account_id):
    return ACCOUNT_DICT


def mock_get_account_empty_dict(self, account_id):
    return {}


def mock_get_account_dict_exception(self, account_id):
    raise Exception("DB Exception")


def mock_get_user(self, email):
    return {"user_id": 200}


def mock_get_user_empty(self, email):
    return {}


def mock_get_user_exception(self, email):
    raise Exception("DB Exception")


def mock_get_account_details_empty_dict(self, account_id):
    return {}


def mock_get_inactive_account(self, account):
    account_data = {"account_id": "1", "user_id": "1", "account_status": "inactive",
                    "account_type": "saving", "balance": 20}
    return Account(**account_data)


def mock_get_small_balance_account(self, account):
    account_data = {"account_id": "1", "user_id": "1", "account_status": "active",
                    "account_type": "saving", "balance": 20}
    return Account(**account_data)


def mock_get_happy_flow_account(self, account_id):
    account_data = {"account_id": "1", "user_id": "1", "account_status": "active",
                    "account_type": "saving", "balance": 120}
    return Account(**account_data)


def mock_assert_account_balance(self, acc_id, balance):
    assert balance == 100
    assert acc_id == "1"
