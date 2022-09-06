SELECT customerId, COUNT(*) AS numCones
FROM customerPurchases P, conesInPurchase C
WHERE C.purchaseId = P.purchaseId
GROUP BY customerId
ORDER BY numCones DESC;