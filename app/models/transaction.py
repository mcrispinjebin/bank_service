from typing import NewType
from pydantic import BaseModel, condecimal
from .account import AccountID
from datetime import datetime
from enum import Enum

TransactionID = NewType("TransactionID", str)

TransactionAmount = condecimal(decimal_places=2, ge=0)


class TransactionStatus(Enum):
    pending = 'pending'
    success = 'success'
    failed = 'failed'


class TransactionType(Enum):
    credit = "credit"
    debit = "debit"


class TransactionPayload(BaseModel):
    amount: TransactionAmount
    account_id: AccountID


class Transaction(TransactionPayload):
    transaction_type: TransactionType
    status: TransactionStatus
    created_at: datetime
    amount: TransactionAmount
    transaction_id: TransactionID
