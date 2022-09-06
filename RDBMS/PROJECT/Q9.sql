CREATE FUNCTION numScoops(coneNumber INT)
RETURNS INT DETERMINISTIC
RETURN(
SELECT COUNT(SC.scoopId) AS numScoop
FROM ScoopsInCone SC 
WHERE SC.coneId = coneNumber
GROUP BY SC.coneId);

DELIMITER ++
CREATE PROCEDURE purchaseSummary(purchaseNum INT,
OUT oneScoop INT,
OUT twoScoop INT,
OUT threeScoop INT)
BEGIN
CREATE TABLE table_1
(
purchaseID INT
, coneId INT
, num INT
);

INSERT INTO table_1
(
purchaseID
, coneId
, num
)
SELECT C.purchaseID,C.coneId, numScoops(C.coneId) AS num
   FROM conesInPurchase C
   WHERE C.purchaseID = purchaseNum;
   
SELECT COUNT(*) INTO oneScoop
FROM table_1
WHERE num = 1;

SELECT COUNT(*) INTO twoScoop
FROM table_1
WHERE num = 2;

SELECT COUNT(*) INTO threeScoop
FROM table_1
WHERE num = 3;


DROP TABLE IF EXISTS table_1;

END ++
DELIMITER ;