DROP FUNCTION IF EXISTS isNutFreex;
DELIMITER ++
CREATE FUNCTION isNutFreex(coneNumber INT)
RETURNS BOOLEAN DETERMINISTIC
BEGIN
DECLARE tf BOOLEAN;

read_loop:LOOP
IF coneNumber IN(SELECT C.id
FROM  ScoopsInCone SC, Cone C, Scoop S
WHERE C.id = SC.coneId AND S.id = SC.scoopId 
AND coneNumber = C.id
AND S.name <> 'Coconut' AND C.conetype = 'Waffle')
THEN RETURN 1;
END IF;
IF coneNumber IN(SELECT C.id
FROM  ScoopsInCone SC, Cone C, Scoop S
WHERE C.id = SC.coneId AND S.id = SC.scoopId 
AND coneNumber = C.id
AND C.conetype = 'Waffle' AND s.name <> 'Macadamia')
THEN RETURN 1;

END IF;

END LOOP;




RETURN tf;

END++
DELIMITER ;


SELECT isNutFreex(id) AS nutFree, COUNT(*)
FROM Cone WHERE id < 100
GROUP BY nutFree; ##Should return 58 (1) and 41 (0)