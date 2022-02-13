from datetime import datetime
from typing import NewType, Optional
from pydantic import BaseModel, condecimal
from .user import UserID, FirstName, Email, Nationality
from enum import Enum


AccountID = NewType("AccountID", int)
AccountBalance = condecimal(decimal_places=2)


class AccountType(Enum):
    premium = "premium"
    saving = "saving"


class AccountStatus(Enum):
   active = "active"
   inactive = "inactive"


class Account(BaseModel):
    account_id: AccountID
    user_id: UserID
    account_type: AccountType
    account_status: AccountStatus
    balance: AccountBalance
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class CreateAccountPayload(BaseModel):
    first_name: FirstName
    email: Email
    nation: Nationality
    account_type: AccountType
    initial_deposit: AccountBalance


class UpdateAccount(BaseModel):
    balance: AccountBalance
