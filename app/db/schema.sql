CREATE DATABASE bank_service;
use bank_service;

CREATE TABLE user(user_id varchar(30) PRIMARY KEY, first_name varchar(30), email varchar(30), nationality varchar(20), created_at datetime, modified_at datetime);
CREATE TABLE account(account_id varchar(30) PRIMARY KEY, user_id varchar(30) REFERENCES user(user_id), account_type enum('premium', 'saving'), account_status enum('active', 'inactive'), balance float, created_at datetime, modified_at datetime);
CREATE TABLE transaction(transaction_id varchar(30) PRIMARY KEY, account_id varchar(30) REFERENCES account(account_id), amount float, transaction_type enum('credit', 'debit'), status enum('success', 'failed'), created_at datetime);
