from fastapi import APIRouter
from app.models.account import Account, CreateAccountPayload, AccountID, UpdateAccount
from app.service.account_service import AccountService

account_router = APIRouter(tags=['Account Creation and Account details'])


@account_router.post("/account", response_model=Account)  # TODO: add documentation
async def create_account(account_payload: CreateAccountPayload):
    service_obj = AccountService()
    account_data = service_obj.create_account(account_payload)
    return account_data


@account_router.get("/account/{account_id}", response_model=Account)  # TODO: add documentation
async def get_account_details(account_id: AccountID):
    service_obj = AccountService()
    account_data = service_obj.get_account_details(account_id)
    return account_data


@account_router.patch("/account/{account_id}", response_model=Account)
async def update_payout_status(account_id: AccountID, update_data: UpdateAccount):
    service_obj = AccountService()
    account_data = service_obj.update_account_balance(account_id, update_data.balance)
    return account_data
