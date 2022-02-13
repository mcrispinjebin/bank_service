from fastapi import APIRouter
from app.models.transaction import Transaction, TransactionPayload, TransactionType
from app.service.transaction_service import TransactionService

transactions_router = APIRouter(tags=['Handle Transactions'])


@transactions_router.post("/deposit", response_model=Transaction)  # TODO: add documentation
async def create_account(deposit_data: TransactionPayload):
    service_obj = TransactionService()
    transaction_data = service_obj.create_transaction(deposit_data.account_id, deposit_data.amount,
                                                      TransactionType.credit)
    return transaction_data


@transactions_router.post("/withdraw", response_model=Transaction)  # TODO: add documentation
async def create_account(withdraw_data: TransactionPayload):
    service_obj = TransactionService()
    transaction_data = service_obj.create_transaction(withdraw_data.account_id, withdraw_data.amount,
                                                      TransactionType.debit)
    return transaction_data
