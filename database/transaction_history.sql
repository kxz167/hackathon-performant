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


-- GET THE LAST TRANSACTION BEFORE CURRENT LOCATION:
SELECT pl:NUMERIC, plp, avg_price FROM position_transaction_history 
WHERE date < '2022-3-15'
ORDER BY date DESC
LIMIT 1;

-- GRAPHICAL REPRESENTATIONS:
SELECT 
	ticker, 
	jsonb_agg(
		(
			SELECT x 
			FROM (SELECT date AS name, pl::Numeric AS value ORDER BY date) AS x)
	) AS pl,
	jsonb_agg(
		(
			SELECT x 
			FROM (SELECT date AS name, plp AS value ORDER BY date) AS x)
	) AS plp,
	jsonb_agg(
		(
			SELECT x 
			FROM (SELECT date AS name, quantity AS value ORDER BY date) AS x)
	) AS quantity
FROM position_transaction_history
WHERE ticker = 'NVDA'
GROUP BY ticker

-- Get tickers:
SELECT  ticker FROM position_transaction_history GROUP BY ticker;