SELECT MONTHNAME(buyDate) AS month, COUNT(*) AS numPurchases
FROM Purchase
GROUP BY month;