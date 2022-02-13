from fastapi import APIRouter
from .account_controller import account_router
from .transaction_controller import transactions_router

router = APIRouter()

router.include_router(account_router, prefix="/account")
router.include_router(transactions_router, prefix="/transactions")
