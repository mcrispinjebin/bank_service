from fastapi import APIRouter
from app.models.transaction import TransactionPayload, TransactionType, Transaction
from app.config.api_config import API_DESCRIPTION, TRANSACTION, DEPOSIT, WITHDRAW
from app.service.transaction_service import TransactionService

transactions_router = APIRouter(tags=['Transaction Endpoints'])


@transactions_router.post("/deposit", response_model=Transaction, **API_DESCRIPTION[TRANSACTION][DEPOSIT])
async def deposit_amount(deposit_data: TransactionPayload):
    service_obj = TransactionService()
    transaction_data = service_obj.create_transaction(deposit_data.account_id, deposit_data.amount,
                                                      TransactionType.credit)
    return transaction_data


@transactions_router.post("/withdraw", response_model=Transaction, **API_DESCRIPTION[TRANSACTION][WITHDRAW])
async def withdraw_amount(withdraw_data: TransactionPayload):
    service_obj = TransactionService()
    transaction_data = service_obj.create_transaction(withdraw_data.account_id, withdraw_data.amount,
                                                      TransactionType.debit)
    return transaction_data
