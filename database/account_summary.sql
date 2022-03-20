-- FREE CASH
SELECT sum::Numeric AS cash_balance FROM (with data as (SELECT value, date FROM(
SELECT account_uuid, amount as value, date
FROM account_transaction
UNION
SELECT account_uuid, -1 * (price*quantity) as value, date FROM 
position_transaction) as a
WHERE a.account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
ORDER BY date)
SELECT date, sum (value) over (order by date asc rows between unbounded preceding and current row)
FROM data) as x ORDER BY date DESC LIMIT 1

--TOTAL DEPOSITS
SELECT sum as deposit_balance FROM (with data as (SELECT date, amount::Numeric
FROM account_transaction 
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
ORDER BY date)
SELECT date, sum (amount) over (order by date asc rows between unbounded preceding and current row)
from data) as x ORDER BY date DESC LIMIT 1

-- CURRENT PL
SELECT sum(pl) 
FROM position_transaction_history 
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' 
GROUP BY date, account_uuid
ORDER BY date DESC
LIMIT 1

-- Investments Value:
SELECT sum(tot_value) AS value FROM position_transaction_history 
WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37'
GROUP BY account_uuid, date
ORDER BY date DESC
LIMIT 1;