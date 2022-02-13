from typing import NewType
from pydantic import BaseModel, constr, condecimal
from .account import AccountID  # TODO: remove this
from datetime import datetime
from enum import Enum


TransactionID = NewType("TransactionID", int)

TransactionAmount = condecimal(decimal_places=2)


class TransactionStatus(Enum):
    pending = 'pending'
    success = 'success'
    failed = 'failed'


class TransactionType(Enum):
    credit = "credit"
    debit = "debit"


class Transaction(BaseModel):
    transaction_id: TransactionID
    account_id: AccountID
    amount: TransactionAmount
    transaction_type: TransactionType
    status: TransactionStatus
    created_at: datetime


class TransactionPayload(BaseModel):
    amount: TransactionAmount
    account_id: AccountID
