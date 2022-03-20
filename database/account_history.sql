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
SELECT jsonb_agg(json_build_object) FROM (SELECT json_build_object('name',date, 'value' , sum(pl)::Numeric) FROM position_transaction_history WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' GROUP BY date, account_uuid ORDER BY date ) as x;


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

SELECT jsonb_agg(json_build_object) FROM 
(SELECT json_build_object('name', date, 'value', sum(tot_value)::Numeric)
FROM position_transaction_history
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
GROUP BY account_uuid, date
ORDER BY date) as x;


-- Cash balance over time dependent on account transactions and position purchases:
SELECT value, name FROM(
SELECT account_uuid, amount as value, date as name
FROM account_transaction
UNION
SELECT account_uuid, -1 * (price*quantity) as value, date as name FROM 
position_transaction) as a
WHERE a.account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
ORDER BY name

SELECT jsonb_agg(json_build_object) FROM 
(SELECT json_build_object ('value', value::Numeric, 'name', name) FROM(
SELECT account_uuid, amount as value, date as name
FROM account_transaction
UNION
SELECT account_uuid, -1 * (price*quantity) as value, date as name FROM 
position_transaction) as a
WHERE a.account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
ORDER BY name) as x;


-- Deposit history:
SELECT date as name, amount as value
FROM account_transaction 
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
ORDER BY date;

SELECT jsonb_agg(json_build_object) FROM
(SELECT json_build_object('name', date, 'value', amount::Numeric)
FROM account_transaction 
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
ORDER BY date) as x;

SELECT jsonb_agg((
	SELECT x FROM (SELECT date as name, amount::Numeric as value ORDER BY date) as x)
)
FROM account_transaction
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37';