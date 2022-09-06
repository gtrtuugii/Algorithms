CREATE FUNCTION numFlavours(coneNumber INT)
RETURNS INT DETERMINISTIC
RETURN(
SELECT flavour.numF
FROM(
SELECT C.id, COUNT(S.name) as numF
FROM Cone C, Scoop S, ScoopsInCone SC
WHERE C.id = SC.coneId AND S.id = SC.scoopId 
AND C.id = coneNumber
GROUP BY C.id) AS flavour);