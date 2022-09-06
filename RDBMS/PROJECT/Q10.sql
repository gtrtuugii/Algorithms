DELIMITER ++
CREATE PROCEDURE createMonthlyWinners()
BEGIN

DROP TABLE IF EXISTS storeNumPurchases;
DROP TABLE IF EXISTS MonthlyWinners;

CREATE TABLE MonthlyWinners(
month VARCHAR(32),
winning_store ENUM('Cottesloe','Fremantle','City Beach'),
Sales INT);

CREATE TABLE storeNumPurchase(
month VARCHAR(32),
store ENUM('Cottesloe','Fremantle','City Beach'),
Sales INT);

INSERT INTO storeNumPurchase(
month,
store,
Sales)
SELECT  concat_ws(' ',monthname(buydate),year(buydate)) as month, store, count(*) as Sales
FROM Purchase
GROUP BY month, store;

INSERT INTO MonthlyWinners(
month,
winning_store,
Sales)
SELECT month,store, Sales
FROM storeNumPurchase
WHERE Sales = 
(SELECT MAX(Sales) 
FROM storeNumPurchase N
WHERE N.month = storeNumPurchase.month)
GROUP BY month,store,Sales;

END++
DELIMITER ;