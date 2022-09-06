DELIMITER ++
CREATE FUNCTION costOfPurchase(purchaseNumber INT)
RETURNS INT DETERMINISTIC
BEGIN
DECLARE basecost INT;
DECLARE coneprice INT;
DECLARE scoopprice INT;
DECLARE scoopnumb INT;
DECLARE discountamount INT;
DECLARE price INT;
DECLARE finalprice INT;
DECLARE DayofWeek VARCHAR(16);
DECLARE customerdiscount INT;

DECLARE Weekday CURSOR FOR
SELECT dayname(buyDate)
FROM purchase
WHERE purchase.id = purchaseNumber;

DECLARE conecost CURSOR FOR
SELECT SUM(conecost)
FROM conesInPurchase SC JOIN Cone C ON SC.coneid = C.id
WHERE SC.purchaseId = purchaseNumber
GROUP BY SC.purchaseId;

DECLARE scoopcost CURSOR FOR
SELECT SUM(K.totalscoopcost)
FROM(
SELECT SUM(S.costincents) AS totalscoopcost
FROM Scoop S, ScoopsInCone SC, conesInPurchase CP
WHERE SC.scoopid = S.id AND CP.coneId = SC.coneId
AND CP.purchaseId = purchaseNumber
GROUP BY SC.coneId) AS K;

DECLARE multiscoop CURSOR FOR
SELECT COUNT(S.id) AS numScoop
FROM Scoop S, ScoopsInCone SC, conesInPurchase CP
WHERE SC.scoopid = S.id AND CP.coneId = SC.coneId
AND CP.purchaseID = purchaseNumber;

DECLARE custdisc CURSOR FOR
SELECT CP.discountapplied
from customerpurchases CP, purchase P
WHERE P.id = CP.purchaseid AND P.id = purchaseNumber;

OPEN conecost;
OPEN scoopcost;
OPEN multiscoop;
OPEN Weekday;
OPEN custdisc;

FETCH Weekday INTO dayOfWeek;
FETCH conecost INTO coneprice;
FETCH scoopcost INTO scoopprice;
FETCH multiscoop INTO scoopnumb;
FETCH custdisc INTO customerdiscount;

IF dayOfWeek LIKE 'Saturday' THEN
SET basecost = 100;
END IF;
IF dayOfWeek LIKE 'Sunday' THEN
SET basecost = 150;
ELSE SET basecost = 50;
END IF;

IF scoopnumb = 2 THEN 
SET discountamount = 50;
ELSEIF scoopnumb >= 3
THEN SET discountamount = 150;
ELSE SET discountamount = 0;
END IF;

SET price = basecost + coneprice + scoopprice - discountamount;
SET finalprice = price - (price * customerdiscount / 100);

CLOSE Weekday;
CLOSE conecost;
CLOSE scoopcost;
CLOSE multiscoop;
CLOSE custdisc;

RETURN finalprice;

END++
DELIMITER ;
