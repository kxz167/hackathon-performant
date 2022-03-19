-- Invested balance:
SELECT * FROM account_transaction
CREATE TABLE account_transaction_history(
	account_uuid UUID,
	date DATE,
	invested_balance MONEY,
	invested_value MONEY,
	available_funds MONEY,
	performance MONEY,
	PRIMARY KEY (account_uuid, date),
	FOREIGN KEY (account_uuid)
		REFERENCES (account)
)
-- P/L agg:
SELECT date, account_uuid, sum(pl) FROM position_transaction_history WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' GROUP BY date, account_uuid

--Paid for stocks:
SELECT ticker, sum(price * quantity) FROM position_transaction WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' GROUP BY ticker;

-- FREE CASH FLOW:
SELECT account_uuid,  funds-expense AS free_cash FROM 
(SELECT account_uuid, SUM(price * quantity) as expense FROM position_transaction WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' GROUP BY account_uuid) as a
NATURAL JOIN
(SELECT account_uuid, SUM(amount) as funds from account_transaction WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' GROUP BY account_uuid) as b

-- Account investment value.
SELECT date AS name, sum(tot_value) AS value FROM position_transaction_history 
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
GROUP BY account_uuid, date
ORDER BY date;