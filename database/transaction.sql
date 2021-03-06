-- TABLES
CREATE TABLE position_transaction (
    uuid UUID DEFAULT gen_random_uuid(),
    account_uuid UUID,
    quantity INTEGER,
    ticker TEXT,
    date DATE,
    price MONEY,
    PRIMARY KEY (uuid),
    FOREIGN KEY (account_uuid)
        REFERENCES account (uuid)
        ON DELETE CASCADE
);

-- INSERTION:
INSERT INTO position_transaction (account_uuid, quantity, ticker, date, price) VALUES ('3d23e8c1-71f1-48f8-a323-60fd159f3c37', 2, 'AAPL', '2022-3-15', 183.24);
INSERT INTO 
position_transaction (account_uuid, quantity, ticker, date, price) 
VALUES ('3d23e8c1-71f1-48f8-a323-60fd159f3c37', 1, 'AAPL', '2022-3-11', 183.24)
RETURNING account_uuid, ticker, extract(epoch from date) * 1000 as date, date as date_text;


-- MAYBE USEFUL QUERIES, NOT! THESE WILL NOT WORK, NEED A SCAN FUNCTION:
-- INVESTED VALUE IN STOCK...?
SELECT ticker, SUM(price * quantity) FROM position_transaction WHERE
	account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
	GROUP BY ticker;

-- AVERAGE STOCK PRICE -> Can't just look at all...
SELECT ticker, SUM(price * quantity) /  NULLIF(SUM(quantity),0) AS avg_price FROM position_transaction WHERE
	account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
	GROUP BY ticker;

-- GET TRANSACTION INFO:
SELECT ticker, quantity, price, date FROM position_transaction ORDER BY ticker, date;

-- GET AGGREGATED TRANSACTION INFO:
SELECT 
    ticker, 
    jsonb_agg(to_jsonb(position_transaction.*) - '{ticker, uuid, account_uuid}'::text[] 
        ORDER BY date)
FROM position_transaction
GROUP BY ticker;

-- SAMPLE GET FOR AAPL, gets all information needed to calculate quantity + 
SELECT quantity, extract(epoch from date) * 1000 as date_mili, price 
FROM position_transaction
WHERE
	ticker = 'AAPL'
ORDER BY date;

-- GET THE TIMES FOR QUANTITY CALCULATION:
SELECT 
	extract(epoch from date)*1000 as date,
	quantity
FROM position_transaction
WHERE 
	ticker = 'AAPL'
ORDER BY date;