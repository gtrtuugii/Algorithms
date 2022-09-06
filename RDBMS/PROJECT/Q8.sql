SELECT c1.email , p1.store, COUNT(p1.id) as tp
FROM Customer c1  
	LEFT JOIN customerPurchases cp on c1.id = CP.customerId
	LEFT JOIN Purchase p1 on p1.id = CP.purchaseId
GROUP BY c1.email, p1.store
WITH rollup;