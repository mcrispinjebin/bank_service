# Bank Service

A Production ready system that allows to create & get account for users and also can handle deposit & withdraw transactions for account.

---

[Fast API](https://fastapi.tiangolo.com/)

---

**Contents**

1. [Setup](#setup)
1. [API docs](#api-docs)
1. [DB](#db)
1. [Quality](#quality)
1. [Future Scope](#future-scope)

---

### Setup ###

1. Install MySQL server and provide suitable previleges for user & host.
1. Source the DB schema available in `app/db/schema.sql` file.
1. Clone the repo in local
1. Provide the DB env variables & hosts in `start-container.sh` file.
1. Build the image by running `build-images.sh` file.
1. Start the container by running `start-container.sh` file.

---

### API docs ###

API documentation will be available after starting the service in the below endpoint -`http://0.0.0.0:8000/bank_service/public/redoc`

Swagger is used for API documentation so the api's could be tried by below endpoint - 

```http://0.0.0.0:8000/bank_service/public/doc```

API documentation screenshots are placed in the file - `api_docs.pdf`.

---

### DB Schema ###
Three tables created for the bank service.

- user
- account
- transactions

Deposit & withdrawal handled in same transactions table.

---

### Quality ###

Unit Test cases are available in `bank_service/tests` folder.\
Flake8 is used as static code analyzer to improve code quality.

Also API request validations are handled via models.

End-End testing screenshots are available in `api_responses.pdf`

---

### Future Scope ###

1. Segregate Private & Public API's and update_balance API should be part of Private endpoint.
1. Need to implement proper format for logging and tracing.
1. Need to add authentication to the system.
1. To improve on the test coverage.

---