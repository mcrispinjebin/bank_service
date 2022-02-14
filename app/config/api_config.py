ACCOUNT = "ACCOUNT"
CREATE_ACCOUNT = "CREATE ACCOUNT API"
GET_ACCOUNT = "GET ACCOUNT API"
UPDATE_ACCOUNT = "UPDATE ACCOUNT API"
TRANSACTION = "TRANSACTION"
DEPOSIT = "DEPOSIT TRANSACTION API"
WITHDRAW = "WITHDRAW TRANSACTION API"

API_DESCRIPTION = {
    ACCOUNT: {
        CREATE_ACCOUNT: {
            "summary": "Create Account",
            "description": "API to create account",
            "response_description": "Created Account data",
        },
        GET_ACCOUNT: {
            "summary": "Get Account details",
            "description": "API to fetch account details by account ID",
            "response_description": "Retreived Account data",
        },
        UPDATE_ACCOUNT: {
            "summary": "Update Account balance",
            "description": "API to update account balance by account ID",
            "response_description": "Updated Account data",
        }
    },
    TRANSACTION: {
        DEPOSIT: {
            "summary": "Deposit amount",
            "description": "API to deposit amount by account ID",
            "response_description": "Created Transaction Record",
        },
        WITHDRAW: {
            "summary": "Withdraw amount",
            "description": "API to withdraw amount by account ID",
            "response_description": "Created Transaction Record",
        }
    }
}
