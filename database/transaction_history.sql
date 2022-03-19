CREATE TABLE position_transaction_history(
    account_uuid UUID,
    date DATE,
    ticker TEXT,
    quantity INTEGER,
    pl MONEY,
    plp NUMERIC,
    avg_price MONEY,
    PRIMARY KEY (account_uuid, date, ticker),
    FOREIGN KEY (account_uuid)
        REFERENCES account (uuid)
);

-- TRANSACTION HISTORY REPLACING UPDATE:
INSERT INTO position_transaction_history 
	(account_uuid, date, ticker, quantity) 
VALUES ('3d23e8c1-71f1-48f8-a323-60fd159f3c37', '2022-03-15', 'AAPL', 4)
	ON CONFLICT 
	ON CONSTRAINT position_transaction_history_pkey 
	DO UPDATE SET quantity = EXCLUDED.quantity, pl = EXCLUDED.pl, plp = EXCLUDED.plp;