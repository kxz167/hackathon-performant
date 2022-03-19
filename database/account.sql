-- TABLES
CREATE TABLE account (
    uuid UUID DEFAULT gen_random_uuid(),
    name TEXT,
    description TEXT,
    PRIMARY KEY (uuid)
);

CREATE TABLE account_transaction(
    uuid UUID DEFAULT gen_random_uuid(),
    account_uuid UUID,
    amount MONEY,
    date DATE,
    PRIMARY KEY (uuid),
    FOREIGN KEY (account_uuid)
        REFERENCES account (uuid)
        ON DELETE CASCADE
);

-- INSERTION:
-- ACCOUNT
INSERT INTO account (name, description) VALUES ('TDA', 'TD Ameritrade IRA');

-- ACCOUNT TRANSACTIONS:
INSERT INTO account_transaction (account_uuid, amount, date) VALUES ('3d23e8c1-71f1-48f8-a323-60fd159f3c37', 200, '2022-01-14');
INSERT INTO account_transaction (account_uuid, amount, date) VALUES ('3d23e8c1-71f1-48f8-a323-60fd159f3c37', -200, '2022-01-19');
INSERT INTO account_transaction (account_uuid, amount, date) VALUES ('3d23e8c1-71f1-48f8-a323-60fd159f3c37', 250.89, '2022-02-5');

-- ACCOUNT SUMMARY:
-- GET THE DEPOSITED BALANCE
SELECT sum(account_transaction.amount) FROM account_transaction;